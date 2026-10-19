"""Annotations remain attributed observations; missing values are never neutral."""
import hashlib
import html
import itertools
import json
import math
import re

EMOTIONS = ("joy", "fear", "sadness", "anger")
LABELS = {
 "fr":{"title":"Carnet de lecture émotionnelle","quote":"Passage exact","source":"Empreinte du texte","reader":"Réaction déclarée du lecteur","text":"Émotion du texte","character":"Émotion du personnage","reader_hypothesis":"Hypothèse de réaction du lecteur","limits":"Les annotations expriment des perspectives ; aucune émotion humaine n’est inférée comme un fait.","joy":"Joie","fear":"Peur","sadness":"Tristesse","anger":"Colère","missing":"Non annoté"},
 "en":{"title":"Emotion reading notebook","quote":"Exact passage","source":"Text fingerprint","reader":"Reader self-report","text":"Text emotion","character":"Character emotion","reader_hypothesis":"Reader reaction hypothesis","limits":"Annotations express perspectives; no human emotion is inferred as a fact.","joy":"Joy","fear":"Fear","sadness":"Sadness","anger":"Anger","missing":"Unannotated"},
 "es":{"title":"Cuaderno de lectura emocional","quote":"Pasaje exacto","source":"Huella del texto","reader":"Reacción declarada del lector","text":"Emoción del texto","character":"Emoción del personaje","reader_hypothesis":"Hipótesis de reacción del lector","limits":"Las anotaciones expresan perspectivas; ninguna emoción humana se infiere como un hecho.","joy":"Alegría","fear":"Miedo","sadness":"Tristeza","anger":"Ira","missing":"Sin anotar"}}

def fingerprint(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def document(text, language="en", title=""):
    if not isinstance(text,str) or not text.strip() or len(text)>30000 or language not in LABELS or not isinstance(title,str) or len(title)>200:
        raise ValueError("invalid_document")
    spans=[]
    start=0
    for boundary in list(re.finditer(r"\n[ \t\r]*\n",text))+[None]:
        stop=boundary.start() if boundary else len(text)
        chunk=text[start:stop];trimmed=chunk.strip()
        if trimmed:
            left=start+len(chunk)-len(chunk.lstrip());right=stop-(len(chunk)-len(chunk.rstrip()))
            spans.append({"id":f"p{len(spans)+1}","start":left,"end":right,"text":text[left:right]})
        start=boundary.end() if boundary else len(text)
    if not 1<=len(spans)<=80:raise ValueError("invalid_segments")
    return {"text":text,"language":language,"title":title,"sha256":fingerprint(text),"offset_unit":"unicode_codepoints","segments":spans}

def validate(bundle):
    if not isinstance(bundle,dict):raise ValueError("invalid_bundle")
    source=bundle.get("document",{});expected=document(source.get("text"),source.get("language"),source.get("title",""))
    if source!=expected:raise ValueError("stale_or_invalid_source")
    annotations=bundle.get("annotations")
    if not isinstance(annotations,list) or len(annotations)>1000:raise ValueError("invalid_annotations")
    ids={s["id"] for s in source["segments"]};seen=set()
    for a in annotations:
        if not isinstance(a,dict) or a.get("source_sha256")!=source["sha256"] or a.get("segment") not in ids or a.get("perspective") not in ("reader","text","character","reader_hypothesis") or a.get("method") not in ("self_report","human_annotation","synthetic_fixture","model_choice"):
            raise ValueError("invalid_annotation")
        if not isinstance(a.get("observer"),str) or not 1<=len(a["observer"])<=80:raise ValueError("invalid_observer")
        if a["perspective"]=="reader" and a["method"] not in ("self_report","synthetic_fixture"):raise ValueError("reader_requires_self_report")
        if a["perspective"]=="character" and (not isinstance(a.get("target"),str) or not a["target"].strip()):raise ValueError("missing_character")
        key=(a["segment"],a["perspective"],a["observer"],a.get("target"))
        if key in seen:raise ValueError("duplicate_observation")
        seen.add(key)
        if a["method"]=="model_choice":
            probs=a.get("probabilities",{});choices=set(EMOTIONS)|{"neutral","mixed","uncertain"}
            if set(probs)!=choices or a.get("choice") not in choices or any(type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=1 for v in probs.values()) or abs(sum(probs.values())-1)>.001 or probs[a["choice"]]+1e-6<max(probs.values()):raise ValueError("invalid_model_distribution")
            if a["perspective"]=="reader":raise ValueError("model_is_not_reader")
            confidence=a.get("confidence")
            if type(confidence) not in (int,float) or not math.isfinite(confidence) or not 0<=confidence<=1:raise ValueError("invalid_confidence")
        else:
            scores=a.get("scores",{})
            if set(scores)!=set(EMOTIONS) or any(type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=1 for v in scores.values()):raise ValueError("invalid_scores")
    return bundle

def analyze(bundle):
    validate(bundle);source=bundle["document"];rows=[]
    readers={a["observer"] for a in bundle["annotations"] if a["perspective"]=="reader"}
    for segment in source["segments"]:
        annotations=[a for a in bundle["annotations"] if a["segment"]==segment["id"]]
        reports=[a for a in annotations if a["perspective"]=="reader"]
        pairs=list(itertools.combinations(reports,2))
        distance=sum(sum(abs(a["scores"][e]-b["scores"][e]) for e in EMOTIONS)/len(EMOTIONS) for a,b in pairs)/len(pairs) if pairs else None
        rows.append({**segment,"annotations":annotations,"reader_count":len(reports),"pair_count":len(pairs),"reader_disagreement":distance,
            "reader_mean":{e:sum(a["scores"][e] for a in reports)/len(reports) for e in EMOTIONS} if reports else None})
    possible=len(readers)*len(rows)
    return {"source_sha256":source["sha256"],"segments":rows,"reader_count":len(readers),"observed_reader_cells":sum(r["reader_count"] for r in rows),"possible_reader_cells":possible,
        "reader_coverage":sum(r["reader_count"] for r in rows)/possible if possible else None,"all_reader_reports_synthetic":all(a["method"]=="synthetic_fixture" for a in bundle["annotations"] if a["perspective"]=="reader"),"human_accuracy_measured":False}

def annotate(bundle,segment,observer,scores,perspective="reader",target=None):
    result=json.loads(json.dumps(validate(bundle)));item={"source_sha256":result["document"]["sha256"],"segment":segment,"observer":observer,"perspective":perspective,"method":"self_report" if perspective=="reader" else "human_annotation","scores":scores}
    if target is not None:item["target"]=target
    result["annotations"]=[a for a in result["annotations"] if (a["segment"],a["perspective"],a["observer"],a.get("target"))!=(segment,perspective,observer,target)]+[item]
    return validate(result)

def markdown(bundle,lang="en"):
    report=analyze(bundle);labels=LABELS[lang];doc=bundle["document"]
    # The text is enclosed in an adaptive fence so user Markdown cannot become notebook commands.
    result=[f'# {doc["title"] or labels["title"]}',f'{labels["source"]}: `{doc["sha256"]}`',labels["limits"]]
    for row in report["segments"]:
        result.extend([f'## {row["id"]} ^{doc["sha256"][:10]}-{row["id"]}',f'{labels["quote"]} · Unicode [{row["start"]}, {row["end"]})'])
        fence="`"*(max([len(m.group()) for m in re.finditer(r"`+",row["text"])]+[2])+1)
        result.extend([fence+"text",row["text"],fence])
        for a in row["annotations"]:
            data={k:v for k,v in a.items() if k not in ("source_sha256","segment")}
            result.extend(["```json",json.dumps(data,ensure_ascii=False).replace("`","\\u0060"),"```"])
    return "\n\n".join(result)+"\n"

def svg(bundle,lang="en"):
    report=analyze(bundle);labels=LABELS[lang];rows=report["segments"];width=900;height=360
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 900 360" role="img"><title>{html.escape(labels["title"])}</title><rect width="900" height="360" fill="#101723"/><text x="30" y="32" fill="#f0f3f6" font-family="sans-serif">{html.escape(labels["reader"])}</text>']
    colors=["#ffd06a","#9aa9ff","#69c7df","#ef9b9b"]
    for e,color in zip(EMOTIONS,colors):
        points=[]
        for i,row in enumerate(rows):
            x=60+i*780/max(1,len(rows)-1)
            if row["reader_mean"] is None:
                if points:parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3"/>');points=[]
                continue
            y=260-row["reader_mean"][e]*170;points.append(f"{x},{y}");parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>')
        if points:parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3"/>')
    for i,(e,color) in enumerate(zip(EMOTIONS,colors)):parts.append(f'<text x="{40+i*210}" y="305" fill="{color}" font-family="sans-serif">{html.escape(labels[e])}</text>')
    parts.append(f'<text x="30" y="340" fill="#9caec0" font-family="sans-serif" font-size="11">SHA-256 {report["source_sha256"]}</text></svg>')
    return "".join(parts)
