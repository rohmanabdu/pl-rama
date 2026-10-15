import requests, re, os

URL_RCTI = "https://raw.githubusercontent.com/apistech/project/refs/heads/main/playlists/rctiplus.m3u"
URL_MILIKMU = "https://raw.githubusercontent.com/rohmanabdu/pl-rama/main/pl-ramaaa3.m3u"
OUTPUT_ROOT = "pl-ramaaz.m3u"
OUTPUT_FOLDER = "pl-ramaaz.m3u" 

CONFIG = {
    "RCTI":   {"group": "INDONESIA", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/RCTI.png"},
    "MNCTV":  {"group": "INDONESIA", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/MNCTV.png"},
    "GTV":    {"group": "INDONESIA", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/GTV.png"},
    "INEWS":  {"group": "INDONESIA", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/INEWS.png"},
}

def get(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

def parse(content):
    chs = []
    ext = ""
    for line in content.splitlines():
        line=line.strip()
        if line.startswith("#EXTINF"):
            ext=line
        elif line.startswith("http"):
            if ext:
                chs.append((ext, line))
                ext=""
    return chs

print("Fetching RCTI+...")
a = parse(get(URL_RCTI))
print("Fetching pl-ramaaa3.m3u...")
b = parse(get(URL_MILIKMU))
all_ch = a + b

seen=set()
out="#EXTM3U\n"
for extinf, url in all_ch:
    if url in seen: continue
    seen.add(url)
    low=extinf.lower()
    group="Lainnya"
    logo=""
    for k,v in CONFIG.items():
        if k in low:
            group=v["group"]
            logo=v["logo"]
            break
    extinf=re.sub(r'group-title=".*?"','',extinf)
    extinf=re.sub(r'tvg-logo=".*?"','',extinf)
    extinf=re.sub(r'\s+',' ',extinf).strip()
    before, after = extinf.rsplit(",",1)
    extinf = f'{before} group-title="{group}" tvg-logo="{logo}",{after}'
    out+=f"{extinf}\n{url}\n"

# simpan 2 lokasi biar pasti ada
with open(OUTPUT_ROOT, "w", encoding="utf-8") as f:
    f.write(out)

# buat folder playlists juga kalau ada
os.makedirs("playlists", exist_ok=True)
with open(os.path.join("playlists", OUTPUT_ROOT), "w", encoding="utf-8") as f:
    f.write(out)

print(f"Sukses! Jadi file {OUTPUT_ROOT} total {len(seen)} channel")
print(f"Lokasi: {os.path.abspath(OUTPUT_ROOT)}")

