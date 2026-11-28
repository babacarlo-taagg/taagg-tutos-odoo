"""Faux service de paiement mobile « PayDem » (fictif), pour s'entraîner sans argent réel.

Lancement :  PAYDEM_SECRET=un-secret-de-test python3 faux_paydem.py
Il écoute sur http://localhost:8090 :
  POST /paiements        {"reference", "montant", "telephone", "url_retour"} -> 201 {"id": "PD-1", "statut": "en_attente"}
  GET  /paiements/PD-1   -> {"id": "PD-1", "statut": "reussi"}
Deux secondes après une demande, il envoie le résultat à url_retour (webhook signé), DEUX fois,
comme le font parfois les vrais opérateurs.
Numéros spéciaux : se termine par 0000 -> refusé (400) ; 9999 -> ne répond pas (20 s) ;
8888 -> accepté mais aucun webhook (pour tester le rapprochement).
"""
import hashlib
import hmac
import json
import os
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SECRET = os.environ["PAYDEM_SECRET"].encode()
PAIEMENTS = {}


def envoyer_webhook(paiement, url_retour):
    time.sleep(2)
    paiement["statut"] = "reussi"
    corps = json.dumps({"id": paiement["id"], "reference": paiement["reference"], "statut": "reussi"}).encode()
    signature = hmac.new(SECRET, corps, hashlib.sha256).hexdigest()
    for _ in range(2):
        requete = urllib.request.Request(url_retour, data=corps, method="POST", headers={
            "Content-Type": "application/json", "X-PayDem-Signature": signature})
        try:
            with urllib.request.urlopen(requete, timeout=10) as reponse:
                print("webhook ->", reponse.status, reponse.read().decode())
        except Exception as erreur:
            print("webhook en échec :", erreur)


class PayDem(BaseHTTPRequestHandler):

    def repondre(self, code, donnees):
        corps = json.dumps(donnees).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corps)))
        self.end_headers()
        self.wfile.write(corps)

    def do_POST(self):
        if self.path != "/paiements":
            return self.repondre(404, {"message": "Adresse inconnue"})
        demande = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        telephone = demande["telephone"]
        if telephone.endswith("9999"):
            time.sleep(20)
        if telephone.endswith("0000"):
            return self.repondre(400, {"message": "Numéro refusé par l'opérateur"})
        paiement = {"id": f"PD-{len(PAIEMENTS) + 1}", "reference": demande["reference"], "statut": "en_attente"}
        PAIEMENTS[paiement["id"]] = paiement
        self.repondre(201, {"id": paiement["id"], "statut": "en_attente"})
        if not telephone.endswith("8888"):
            threading.Thread(target=envoyer_webhook, args=(paiement, demande["url_retour"])).start()
        else:
            paiement["statut"] = "reussi"   # payé, mais l'avis ne partira jamais

    def do_GET(self):
        paiement = PAIEMENTS.get(self.path.rsplit("/", 1)[-1])
        if not self.path.startswith("/paiements/") or not paiement:
            return self.repondre(404, {"message": "Paiement inconnu"})
        self.repondre(200, {"id": paiement["id"], "statut": paiement["statut"]})


if __name__ == "__main__":
    print("PayDem (fictif) écoute sur http://localhost:8090")
    ThreadingHTTPServer(("localhost", 8090), PayDem).serve_forever()
