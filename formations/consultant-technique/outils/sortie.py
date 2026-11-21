"""Imprime les valeurs JSON d'une ou plusieurs leçons, pour le connecteur TAAGG. Usage : sortie.py 1.0.2 1.0.3 ..."""
import sys, os, json, importlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bloc1"))
sys.path.insert(0, os.path.dirname(__file__))
from valeurs import valeurs
MODS = ["s0_python_bases", "s1_linux", "s2_python_odoo", "s3_bases_de_donnees", "s4_git_environnement"]
tout = {l["code"]: l for m in MODS for l in importlib.import_module(m).LECONS}
for code in sys.argv[1:]:
    l = tout[code]; v = valeurs(l)
    if l["id"] is None: v["channel_id"] = 208
    print(f"=== {code} id={l['id']}"); print(json.dumps(v, ensure_ascii=False, separators=(",", ":")))
