#!/usr/bin/env python3
"""Genera docs/: index.html con datos y logo incrustados, más docs/fotos/ con las fotos que usa el catálogo."""
import base64, json, os, shutil, datetime
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.normpath(f"{here}/../docs")
html = open(f"{here}/index.html", encoding="utf-8").read()
data = json.load(open(f"{here}/items.json", encoding="utf-8"))
data["updated"] = datetime.date.today().isoformat()
html = html.replace("__LOGO__", "data:image/png;base64," + base64.b64encode(open(f"{here}/logo.png","rb").read()).decode())
html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
os.makedirs(f"{out}/fotos", exist_ok=True)
# fotos como archivos aparte: el HTML pesa poco y cada foto carga sola (loading="lazy")
used = {i["foto"] for i in data["items"] if i.get("foto")}
for f in os.listdir(f"{out}/fotos"):
    if f[:-4] not in used: os.remove(f"{out}/fotos/{f}")
missing = []
for k in sorted(used):
    src = f"{here}/fotos/{k}.jpg"
    if os.path.exists(src): shutil.copyfile(src, f"{out}/fotos/{k}.jpg")
    else: missing.append(k)
open(f"{out}/index.html","w",encoding="utf-8").write(html)
print("docs/index.html", round(os.path.getsize(f"{out}/index.html")/1024), "KB ·", len(used), "fotos")
if missing: print("falta foto:", ", ".join(missing))
