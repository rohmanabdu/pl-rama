import requests, re, os

URL_RCTI = "https://raw.githubusercontent.com/apistech/project/refs/heads/main/playlists/rctiplus.m3u"
URL_MILIKMU = "https://raw.githubusercontent.com/rohmanabdu/pl-rama/main/pl-ramaaa3.m3u"
OUTPUT = "pl-ramaaz.m3u"

# HEADER YANG MAU DIPERTAHANKAN - Sesuai gambar kamu
HEADER_TEMPLATE = """#EXTM3U

by ramaa
backup coy

#EXTINF:-1 tvg-id="" tvg-name="Donasi ++" tvg-logo="https://static.vecteezy.com/system/resources/previews/054/224/335/non_2x/charity-icon-collection-vector.jpg" group-title="Donasi",Donasi ++
https://github.com/rohmanabdu/cloudd/raw/refs/heads/main/awal.mp4

==disini==
"""

CONFIG = {
    "rcti": {"group": "RCTI+", "logo": ""},
    "mnctv": {"group": "RCTI+", "logo": ""},
    "gtv": {"group": "RCTI+", "logo": ""},
    "inews": {"group": "RCTI+", "logo": ""},
}

def get(url):
    r = requests.get(url, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
    r.raise_for_status()
    return r.text

def parse(content):
    chs=[]; ext=""
    for line in content.splitlines():
        line=line.strip()
        if line.startswith("#EXTINF"): ext=line
        elif line.startswith("http"):
            if ext: chs.append((ext,line)); ext=""
    return chs

print("Fetching...")
a=parse(get(URL_RCTI))
b=parse(get(URL_MILIKMU))
print(f"RCTI: {len(a)}, Punyamu: {len(b)}")

seen=set()
merged_content = ""
for extinf,url in a+b:
    if url in seen: continue
    seen.add(url)
    low=extinf.lower()
    group="Lainnya"; logo=""
    for k,v in CONFIG.items():
        if k in low: group=v["group"]; logo=v["logo"]; break
    extinf=re.sub(r'group-title=".*?"','',extinf)
    extinf=re.sub(r'tvg-logo=".*?"','',extinf)
    extinf=re.sub(r'\s+',' ',extinf).strip()
    before, after = extinf.rsplit(",",1)
    extinf = f'{before} group-title="{group}" tvg-logo="{logo}",{after}'
    merged_content+=f"{extinf}\n{url}\n"

# GABUNGKAN HEADER + HASIL
final_m3u = HEADER_TEMPLATE.strip() + "\n\n" + merged_content

with open(OUTPUT,"w",encoding="utf-8") as f:
    f.write(final_m3u)

os.makedirs("playlists", exist_ok=True)
with open(os.path.join("playlists", OUTPUT),"w",encoding="utf-8") as f:
    f.write(final_m3u)

print(f"SUKSES! File {OUTPUT} jadi, total {len(seen)} channel di bawah ==disini==")
