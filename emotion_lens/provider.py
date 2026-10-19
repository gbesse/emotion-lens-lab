"""One explicit paid request; classifications never become reader self-reports."""
import copy
import json
import os
import ssl
from urllib.error import HTTPError, URLError
from urllib.request import Request,build_opener,HTTPRedirectHandler,HTTPSHandler
from .engine import EMOTIONS,validate
MODEL="jev-1.13.0"
PROMPTS={"fr":"Choisir l’émotion dominante de ce seul passage selon la perspective déclarée. Le texte ne prouve pas l’émotion d’un vrai lecteur. Utiliser uncertain si le contexte ne suffit pas.","en":"Choose the dominant emotion of this passage alone under the declared perspective. Text does not establish a real reader’s emotion. Use uncertain when context is insufficient.","es":"Elegir la emoción dominante de este pasaje bajo la perspectiva declarada. El texto no demuestra la emoción de un lector real. Usar uncertain si falta contexto."}
CHOICES={"fr":{"joy":"Joie","fear":"Peur","sadness":"Tristesse","anger":"Colère","neutral":"Aucune émotion dominante","mixed":"Émotions mêlées","uncertain":"Contexte insuffisant"},"en":{"joy":"Joy","fear":"Fear","sadness":"Sadness","anger":"Anger","neutral":"No dominant emotion","mixed":"Mixed emotions","uncertain":"Insufficient context"},"es":{"joy":"Alegría","fear":"Miedo","sadness":"Tristeza","anger":"Ira","neutral":"Sin emoción dominante","mixed":"Emociones mezcladas","uncertain":"Contexto insuficiente"}}
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

def classify(bundle,perspective="text",target=None,max_segments=3,transport=None,api_key=None):
    validate(bundle)
    if perspective not in ("text","character","reader_hypothesis") or perspective=="character" and not target or type(max_segments) is not int or not 1<=max_segments<=6:raise ValueError("invalid_model_request")
    lang=bundle["document"]["language"];segments=bundle["document"]["segments"][:max_segments]
    body={"model":MODEL,"state":{"perspective":perspective,"character":target,"passages":{s["id"]:s["text"] for s in segments}},"questions":{s["id"]:{"type":"choice","instructions":PROMPTS[lang]+" ["+s["id"]+"]","criteria":CHOICES[lang]} for s in segments}}
    if len(json.dumps(body))>18000:raise ValueError("model_context_budget")
    if transport:response=transport(body)
    else:
        import certifi
        key=api_key or os.environ.get("TYPESAFE_API_KEY")
        if not key:raise ValueError("missing_typesafe_key")
        request=Request("https://api.typesafe.ai/v1/systemone",data=json.dumps(body).encode(),headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},method="POST")
        try:
            with build_opener(NoRedirect(),HTTPSHandler(context=ssl.create_default_context(cafile=certifi.where()))).open(request,timeout=30) as stream:
                raw=stream.read(300001)
                if len(raw)>300000:raise ValueError("response_size")
                response=json.loads(raw)
        except HTTPError as e:raise ValueError("provider_http_"+str(e.code)) from None
        except (URLError,TimeoutError):raise ValueError("provider_transport") from None
    if not isinstance(response,dict) or response.get("model")!=MODEL or not isinstance(response.get("answers"),dict) or set(response["answers"])!=set(body["questions"]):raise ValueError("invalid_provider_response")
    usage=response.get("usage",{})
    if any(type(usage.get(k)) is not int or usage[k]<0 for k in ("input_tokens","output_tokens")):raise ValueError("invalid_usage")
    result=copy.deepcopy(bundle)
    for segment,answer in response["answers"].items():
        if not isinstance(answer,dict) or answer.get("type")!="choice":raise ValueError("invalid_answer_type")
        item={"source_sha256":bundle["document"]["sha256"],"segment":segment,"perspective":perspective,"observer":MODEL,"method":"model_choice","choice":answer.get("choice"),"probabilities":answer.get("probabilities"),"confidence":answer.get("confidence")}
        if target:item["target"]=target
        result["annotations"]=[a for a in result["annotations"] if (a["segment"],a["observer"],a["perspective"],a.get("target"))!=(segment,MODEL,perspective,target)]+[item]
    result["provider_usage"]={"model":MODEL,**{k:usage[k] for k in ("input_tokens","output_tokens")},"requests":1,"synthetic_transport":transport is not None}
    return validate(result)
