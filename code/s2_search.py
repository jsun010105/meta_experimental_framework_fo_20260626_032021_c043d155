#!/usr/bin/env python3
"""Search Semantic Scholar Graph API for papers. Prints JSON-ish summary."""
import sys, json, time, urllib.parse, urllib.request

FIELDS = "title,year,authors,abstract,citationCount,externalIds,openAccessPdf,url"

def search(query, limit=8):
    base = "https://api.semanticscholar.org/graph/v1/paper/search?"
    params = {"query": query, "limit": limit, "fields": FIELDS}
    url = base + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "research-agent/1.0"})
            data = json.loads(urllib.request.urlopen(req, timeout=40).read())
            return data.get("data", []) or []
        except Exception as e:
            if attempt == 3:
                sys.stderr.write(f"[s2 fail] {query}: {e}\n")
                return []
            time.sleep(5)
    return []

if __name__ == "__main__":
    for q in sys.argv[1:]:
        print(f"########## QUERY: {q}")
        res = search(q)
        for r in res:
            arx = (r.get("externalIds") or {}).get("ArXiv")
            pdf = (r.get("openAccessPdf") or {}).get("url")
            auth = ", ".join(a.get("name","") for a in (r.get("authors") or [])[:5])
            print(f"--- {r.get('title')} ({r.get('year')}) cites={r.get('citationCount')}")
            print(f"    arXiv={arx} pdf={pdf}")
            print(f"    authors={auth}")
            ab = (r.get('abstract') or '')[:500]
            print(f"    abstract={ab}")
        print()
        time.sleep(3)
