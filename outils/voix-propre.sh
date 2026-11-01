#!/bin/bash
# Voix sans hésitation : génère la voix d'un scénario, la retranscrit phrase par phrase (ElevenLabs Scribe),
# et refait (3 essais au plus) les phrases où la voix clonée a ajouté un « euh » ou répété un mot.
# Usage : outils/voix-propre.sh formations/e-business/EB-03-....yaml
# Coût : la transcription coûte quelques centimes ; chaque phrase refaite ≈ 150 caractères de voix.
set -e
cd "$(dirname "$0")/.."
SC=$1; NOM=$(basename "$SC" .yaml); D=sortie/$NOM; V=$D/voix; mkdir -p "$D/voix-ecartees"
K=$(grep '^ELEVENLABS_API_KEY=' .env | cut -d= -f2-)
node tuto.mjs "$SC" --seulement-voix 2>&1 | grep -E "pistes|✗" || true
# texte attendu de chaque étape (1, 2, …), pour ne pas signaler une répétition voulue (« Page, Page vierge »)
textes() { node -e "const Y=require('yaml');Y.parse(require('fs').readFileSync('$SC','utf8')).etapes.forEach((e,i)=>console.log(String(i+1).padStart(2,'0')+'|'+e.texte.replace(/\s+/g,' ')))"; }
verifier() { # $1 = piste, $2 = numéro d'étape → « PB|texte » ou « OK|texte »
  local t attendu
  t=$(curl -sS -m 120 -H "xi-api-key: $K" -F model_id=scribe_v1 -F language_code=fra -F "file=@$1" \
      https://api.elevenlabs.io/v1/speech-to-text | python3 -c "import json,sys; print(json.load(sys.stdin).get('text',''))")
  attendu=$(textes | grep "^$2|" | cut -d'|' -f2-)
  python3 - "$t" "$attendu" <<'PY'
import re, sys
dit, attendu = sys.argv[1], sys.argv[2].lower()
pb = re.search(r'\beuh\b', dit, re.I) or any(f'{m}, {m}' not in attendu for m in re.findall(r'\b(\w+(?: \w+)?), \1\b', dit.lower()))
print(('PB|' if pb else 'OK|') + dit)
PY
}
a_refaire=""
for f in "$V"/*-elevenlabs-*.mp3; do n=$(basename "$f" | cut -c1-2); r=$(verifier "$f" "$n"); [[ $r == PB* ]] && { a_refaire="$a_refaire $n"; echo "$n ${r:0:200}"; }; done
for essai in 1 2 3; do
  [ -z "$a_refaire" ] && break
  for n in $a_refaire; do mv "$V/$n"-elevenlabs-*.mp3 "$D/voix-ecartees/$n-essai$essai.mp3"; done
  node tuto.mjs "$SC" --seulement-voix > /dev/null 2>&1
  reste=""; for n in $a_refaire; do r=$(verifier "$(ls "$V/$n"-elevenlabs-*.mp3)" "$n"); echo "essai $essai · $n : ${r:0:160}"; [[ $r == PB* ]] && reste="$reste $n"; done
  a_refaire=$reste
done
echo "Phrases encore à écouter : [${a_refaire# }]"
