#!/usr/bin/env python3
"""Genera dist/index.html: una sola página con fotos y datos incrustados, lista para publicar."""
import base64, json, os, re, datetime
here = os.path.dirname(os.path.abspath(__file__))
html = open(f"{here}/index.html", encoding="utf-8").read()
data = json.load(open(f"{here}/items.json", encoding="utf-8"))
data["updated"] = datetime.date.today().isoformat()
html = html.replace("__LOGO__", "data:image/png;base64," + base64.b64encode(open(f"{here}/logo.png","rb").read()).decode())
html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
# el template referencia fotos en JS; sustituimos ahí por un mapa de data URIs
fotos = {f[:-4]: "data:image/jpeg;base64," + base64.b64encode(open(f"{here}/fotos/{f}","rb").read()).decode()
         for f in sorted(os.listdir(f"{here}/fotos")) if f.endswith(".jpg")}
used = {i["foto"] for i in data["items"] if i.get("foto")}
fotos = {k:v for k,v in fotos.items() if k in used}
html = html.replace("const D = JSON.parse", "const FOTOS = " + json.dumps(fotos) + ";\nconst D = JSON.parse")
html = html.replace('src="fotos/${i.foto}.jpg"', 'src="${FOTOS[i.foto]}"')
os.makedirs(f"{here}/../docs", exist_ok=True)
open(f"{here}/../docs/index.html","w",encoding="utf-8").write(html)
print("docs/index.html", round(os.path.getsize(f"{here}/../docs/index.html")/1024), "KB")
