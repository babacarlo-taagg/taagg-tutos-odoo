"""Fabrique les valeurs à envoyer au connecteur TAAGG pour une leçon (fiche + quiz)."""
import json, sys, importlib, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bloc1"))

def quiz_cmds(quiz):
    return [[0, 0, {"sequence": i + 1, "question": q,
                    "answer_ids": [[0, 0, {"sequence": j + 1, "text_value": t, "is_correct": c, "comment": com}]
                                   for j, (t, c, com) in enumerate(reps)]}]
            for i, (q, reps) in enumerate(quiz)]

def valeurs(l, avec_quiz=True):
    v = {"name": l["titre"], "sequence": l["seq"], "slide_category": "article", "source_type": "local_file",
         "description": f"<p>{l['description']}</p>", "html_content": l["html"],
         "completion_time": round(l["minutes"] / 60, 2)}
    if avec_quiz:
        v["question_ids"] = quiz_cmds(l["quiz"])
    return v

if __name__ == "__main__":
    mod, code = sys.argv[1], sys.argv[2]
    l = next(x for x in importlib.import_module(mod).LECONS if x["code"] == code)
    v = valeurs(l)
    if l["id"] is None:
        v["channel_id"] = int(sys.argv[3])
    print(json.dumps(v, ensure_ascii=False))
