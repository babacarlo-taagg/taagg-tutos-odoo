"""Imprime les valeurs JSON d'une ou plusieurs leçons, pour le connecteur TAAGG. Usage : sortie.py 1.0.2 2.1.1 ..."""
import sys, os, json, importlib
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from valeurs import valeurs
BLOCS = {
    "1": ("bloc1", 208, ["s0_python_bases", "s1_linux", "s2_python_odoo", "s3_bases_de_donnees", "s4_git_environnement", "s5_evaluation"]),
    "2": ("bloc2", 209, ["s1_module", "s2_orm", "s3_logique", "s4_heritage", "s5_donnees", "s6_tests", "s7_evaluation"]),
    "3": ("bloc3", 210, ["s1_vues", "s2_rapports", "s3_web", "s4_evaluation"]),
    "4": ("bloc4", 211, ["s1_api", "s2_paiement", "s3_securite", "s4_evaluation"]),
}
def lecons(bloc):
    dossier, canal, mods = BLOCS[bloc]
    sys.path.insert(0, os.path.join(ICI, "..", dossier))
    return canal, {l["code"]: l for m in mods for l in importlib.import_module(m).LECONS}
if __name__ == "__main__":
    for code in sys.argv[1:]:
        canal, tout = lecons(code[0])
        l = tout[code]; v = valeurs(l, avec_quiz=bool(l["quiz"]))
        if l["id"] is None: v["channel_id"] = canal
        print(f"=== {code} id={l['id']}"); print(json.dumps(v, ensure_ascii=False, separators=(",", ":")))
