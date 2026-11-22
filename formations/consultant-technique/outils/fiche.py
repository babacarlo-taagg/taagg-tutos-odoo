"""Gabarit HTML des fiches « article » du parcours Consultant technique Odoo (TAAGG School).

Charte : bleu #0B415B (titres), vert #68C184 (bordures seulement, jamais de texte), taupe #A6A297.
Pages légères : pas d'image, du texte et du code ; le code défile horizontalement sur téléphone.
"""
from html import escape

BLEU, VERT, TAUPE = "#0B415B", "#68C184", "#A6A297"
TEXTE, GRIS = "#21272B", "#55595C"

def _cadre(bordure, fond, titre, corps, couleur_titre=BLEU):
    return (f'<div style="border-left:4px solid {bordure};background:{fond};padding:12px 16px;'
            f'margin:18px 0;border-radius:0 6px 6px 0">'
            f'<div style="font-weight:700;color:{couleur_titre};font-size:14px;margin-bottom:6px">{titre}</div>'
            f'<div style="font-size:15px">{corps}</div></div>')

def code(texte, legende=None):
    leg = (f'<div style="font-size:13px;color:{GRIS};margin:0 0 4px">{legende}</div>' if legende else "")
    return (f'{leg}<pre style="background:#F3F5F6;border:1px solid #DDE2E5;border-radius:6px;padding:12px;'
            f'overflow-x:auto;font-size:13.5px;line-height:1.5;margin:0 0 16px;white-space:pre">'
            f'<code>{escape(texte.strip(chr(10)))}</code></pre>')

def bloc(element):
    sorte = element[0]
    if sorte == "h":
        return f'<h2 style="font-size:20px;font-weight:700;color:{BLEU};margin:26px 0 10px">{element[1]}</h2>'
    if sorte == "p":
        return f'<p style="margin:0 0 14px">{element[1]}</p>'
    if sorte == "liste":
        items = "".join(f'<li style="margin-bottom:6px">{i}</li>' for i in element[1])
        return f'<ul style="margin:0 0 14px;padding-left:22px">{items}</ul>'
    if sorte == "code":
        return code(element[1], element[2] if len(element) > 2 else None)
    if sorte == "astuce":
        return _cadre(VERT, "#F2FAF5", element[1], element[2])
    if sorte == "attention":
        return _cadre("#C0392B", "#FDECEA", element[1], element[2], "#A93226")
    if sorte == "version":
        return _cadre(TAUPE, "#F7F6F4", "Selon ta version d'Odoo", element[1])
    if sorte == "tableau":
        entete, lignes = element[1], element[2]
        th = "".join(f'<th style="text-align:left;padding:6px 8px;border-bottom:2px solid {BLEU};color:{BLEU}">{c}</th>' for c in entete)
        tr = "".join("<tr>" + "".join(f'<td style="padding:6px 8px;border-bottom:1px solid #E3E6E8;vertical-align:top">{c}</td>' for c in l) + "</tr>" for l in lignes)
        return (f'<div style="overflow-x:auto;margin:0 0 16px"><table style="border-collapse:collapse;font-size:14px;width:100%">'
                f'<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>')
    raise ValueError(sorte)

def fiche(objectif, intro, corps, exercice, retenir, duree="10 min", titre_exercice="Exercice"):
    """Assemble une fiche : objectif, introduction, corps, exercice, « À retenir »."""
    morceaux = [
        f'<div style="font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:{TEXTE};line-height:1.6;font-size:15.5px;max-width:860px">',
        f'<div style="border:1px solid #DDE2E5;border-top:4px solid {VERT};border-radius:6px;padding:10px 14px;margin:0 0 18px;font-size:14.5px">'
        f'<b style="color:{BLEU}">Objectif :</b> {objectif}<br><b style="color:{BLEU}">Durée :</b> {duree} · '
        f'<b style="color:{BLEU}">Fil rouge :</b> Baobab Livraison</div>',
        f'<p style="font-size:16.5px;color:{GRIS};margin:0 0 18px">{intro}</p>',
    ]
    morceaux += [bloc(e) for e in corps]
    morceaux.append(f'<h2 style="font-size:20px;font-weight:700;color:{BLEU};margin:26px 0 10px">{titre_exercice}</h2>')
    morceaux += [bloc(e) for e in exercice]
    items = "".join(f'<li style="margin-bottom:6px">{r}</li>' for r in retenir)
    morceaux.append(f'<div style="background:{BLEU};color:#FFFFFF;border-radius:6px;padding:14px 18px;margin:24px 0 8px">'
                    f'<div style="font-weight:700;font-size:15px;margin-bottom:8px">À retenir</div>'
                    f'<ul style="margin:0;padding-left:20px;font-size:15px">{items}</ul></div>')
    morceaux.append("</div>")
    return "".join(morceaux)
