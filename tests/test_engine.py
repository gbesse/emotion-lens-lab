import copy
import json
from pathlib import Path
import unittest
from emotion_lens.engine import document,analyze,annotate,validate,markdown,svg,EMOTIONS
from emotion_lens.provider import classify,MODEL

def bundle(text="One.\n\nTwo.\n\nThree."):
    return {"document":document(text),"annotations":[]}
def scores(value):return {e:value for e in EMOTIONS}
class EmotionTests(unittest.TestCase):
    def test_unicode_offsets_are_exact_codepoints(self):
        d=document("  Élan 🛰️.\n\nUna línea.  ","fr")
        self.assertEqual(len(d["segments"]),2)
        for s in d["segments"]:self.assertEqual(d["text"][s["start"]:s["end"]],s["text"])
        self.assertEqual(d["segments"][0]["start"],2)
    def test_stale_text_and_modified_spans_rejected(self):
        for key in ("text","sha256","segments"):
            b=bundle();b["document"][key]="changed"
            with self.assertRaises(ValueError):validate(b)
    def test_pairwise_disagreement_has_independent_arithmetic(self):
        b=bundle();b=annotate(b,"p1","a",scores(0));b=annotate(b,"p1","b",scores(1));b=annotate(b,"p1","c",scores(.5))
        r=analyze(b)["segments"][0];self.assertEqual(r["pair_count"],3);self.assertAlmostEqual(r["reader_disagreement"],2/3)
    def test_missing_is_gap_not_neutral(self):
        b=annotate(bundle(),"p1","a",scores(0));r=analyze(b)
        self.assertIsNone(r["segments"][1]["reader_mean"]);self.assertEqual(r["reader_coverage"],1/3)
        self.assertIsNone(r["segments"][0]["reader_disagreement"])
    def test_character_and_text_do_not_contaminate_reader_means(self):
        b=annotate(bundle(),"p1","a",scores(.2));b=annotate(b,"p1","critic",scores(1),"character","Mira");b=annotate(b,"p1","critic",scores(.8),"text")
        self.assertEqual(analyze(b)["segments"][0]["reader_mean"],scores(.2))
    def test_duplicate_updates_are_idempotent_without_mutating_input(self):
        source=bundle();a=annotate(source,"p1","a",scores(0));b=annotate(a,"p1","a",scores(1))
        self.assertEqual(source["annotations"],[]);self.assertEqual(len(b["annotations"]),1);self.assertEqual(b["annotations"][0]["scores"],scores(1))
    def test_model_cannot_claim_actual_reader_report(self):
        b=annotate(bundle(),"p1","a",scores(0));b["annotations"][0]["method"]="model_choice"
        with self.assertRaises(ValueError):validate(b)
    def test_invalid_scores_and_stale_annotation_are_rejected(self):
        for value in (True,float("nan"),-1,1.1):
            with self.assertRaises(ValueError):annotate(bundle(),"p1","a",scores(value))
        b=annotate(bundle(),"p1","a",scores(0));b["annotations"][0]["source_sha256"]="old"
        with self.assertRaises(ValueError):validate(b)
    def test_markdown_preserves_quotes_and_uses_stable_obsidian_anchors(self):
        b=bundle("Été 🛰️ ```code```\n\n<script>alert(1)</script>");md=markdown(b,"fr")
        self.assertIn(b["document"]["segments"][0]["text"],md);self.assertIn("````text",md);self.assertIn("^"+b["document"]["sha256"][:10]+"-p1",md)
    def test_svg_does_not_connect_across_unannotated_passage(self):
        b=annotate(bundle(),"p1","a",scores(.2));b=annotate(b,"p3","a",scores(.8));drawing=svg(b)
        self.assertNotIn("60.0,226.0 840.0",drawing);self.assertEqual(drawing.count("<polyline"),8)
    def test_all_original_language_demos_validate(self):
        for lang in ("fr","en","es"):
            b=json.loads((Path(__file__).parents[1]/f"emotion_lens/examples/{lang}.json").read_text());r=analyze(b)
            self.assertEqual(len(r["segments"]),4);self.assertTrue(r["all_reader_reports_synthetic"]);self.assertGreater(r["segments"][1]["reader_disagreement"],.3)
    def test_model_request_is_bounded_and_keeps_perspective(self):
        seen=[]
        def transport(body):
            seen.append(body);return {"model":MODEL,"answers":{key:{"type":"choice","choice":"fear","confidence":.7,"probabilities":{k:1.0 if k=="fear" else 0.0 for k in q["criteria"]}} for key,q in body["questions"].items()},"usage":{"input_tokens":10,"output_tokens":2}}
        b=classify(bundle(),perspective="reader_hypothesis",max_segments=2,transport=transport)
        self.assertEqual(len(b["annotations"]),2);self.assertEqual(analyze(b)["reader_count"],0);self.assertEqual(len(seen),1);self.assertEqual(len(seen[0]["questions"]),2)
    def test_wrong_model_or_question_set_and_unbounded_calls_fail(self):
        for response in ({"model":"wrong","answers":{}},{"model":MODEL,"answers":{}}):
            with self.assertRaises(ValueError):classify(bundle(),transport=lambda _:response)
        with self.assertRaises(ValueError):classify(bundle(),max_segments=7,transport=lambda _:None)
if __name__=="__main__":unittest.main()
