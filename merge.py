import requests
import re

# LINK SUMBER
URL_RCTI = "https://raw.githubusercontent.com/apistech/project/refs/heads/main/playlists/rctiplus.m3u"
URL_PUNYAMU = "https://raw.githubusercontent.com/rohmanabdu/pl-rama/main/pl-ramaaa3.m3u"
OUTPUT = "pl-ramaaz.m3u" # hasil akhir di root

# SETTING KATEGORI & LOGO - EDIT DISINI
# Nama key harus mirip dengan nama channel di playlist asal
CONFIG = {
    "RCTI":   {"group": "INDONESIA", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/RCTI.png"},
    "MNCTV":  {"group": "INDONESIA", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/MNCTV.png"},
    "GTV":    {"group": "INDONESIA", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/GTV.png"},
    "INEWS":  {"group": "INDONESIA", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/INEWS.png"},

}

def get_m3u(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

def parse(content):
    channels = []
    extinf = ""
    for line in content.splitlines():
        line=line.strip()
        if line.startswith("#EXTINF"):
            extinf = line
        elif line.startswith("http"):
            if extinf:
                channels.append((extinf, line))
                extinf = ""
    return channels

def rebuild_extinf(old_extinf, url):
    # ambil nama channel setelah koma
    try:
        ch_name = old_extinf.split(",")[-1]
    except:
        ch_name = "Channel"
    
    # cari config
    cfg = None
    for k, v in CONFIG.items():
        if k.lower() in old_extinf.lower() or k.lower() in ch_name.lower():
            cfg = v
            break
    
    group = cfg["group"] if cfg else "Lainnya"
    logo = cfg["logo"] if cfg else ""

    # bersihkan atribut lama
    base = re.sub(r'group-title=".*?"', '', old_extinf)
    base = re.sub(r'tvg-logo=".*?"', '', base)
    base = re.sub(r'\s+', ' ', base).strip()

    # inject baru
    before, after = base.rsplit(",", 1)
    new_line = f'{before} group-title="{group}" tvg-logo="{logo}",{after}'
    return new_line

def main():
    print("Fetching RCTI+...")
    c1 = parse(get_m3u(URL_RCTI))
    print("Fetching pl-ramaaa3.m3u...")
    c2 = parse(get_m3u(URL_PUNYAMU))

    all_ch = c1 + c2
    
    # hapus duplikat url
    seen = set()
    final = []
    for ext, url in all_ch:
        if url not in seen:
            final.append((ext, url))
            seen.add(url)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ext, url in final:
            f.write(rebuild_extinf(ext, url) + "\n")
            f.write(url + "\n")
    
    print(f"Sukses! Jadi file {OUTPUT} total {len(final)} channel")

if __name__ == "__main__":
    main()
