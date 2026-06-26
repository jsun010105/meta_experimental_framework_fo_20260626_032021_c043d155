#!/usr/bin/env python3
"""Search arXiv API and print results as JSON. Optionally download PDFs."""
import sys, json, time, urllib.parse, urllib.request, re
import xml.etree.ElementTree as ET

ATOM = "{http://www.w3.org/2005/Atom}"

def search(query, max_results=8):
    base = "http://export.arxiv.org/api/query?"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = base + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "research-agent/1.0"})
            data = urllib.request.urlopen(req, timeout=40).read()
            break
        except Exception as e:
            if attempt == 2:
                return []
            time.sleep(3)
    root = ET.fromstring(data)
    out = []
    for entry in root.findall(ATOM + "entry"):
        aid = entry.find(ATOM + "id").text.strip()
        m = re.search(r"arxiv\.org/abs/([^v]+)(v\d+)?", aid)
        short = m.group(1) if m else aid
        title = " ".join(entry.find(ATOM + "title").text.split())
        summary = " ".join(entry.find(ATOM + "summary").text.split())
        published = entry.find(ATOM + "published").text[:10]
        authors = [a.find(ATOM + "name").text for a in entry.findall(ATOM + "author")]
        pdf = None
        for link in entry.findall(ATOM + "link"):
            if link.get("title") == "pdf":
                pdf = link.get("href")
        out.append({
            "id": short, "title": title, "published": published,
            "authors": authors[:6], "summary": summary, "pdf": pdf,
        })
    return out

if __name__ == "__main__":
    queries = sys.argv[1:]
    seen = set()
    allres = []
    for q in queries:
        res = search(q, max_results=8)
        for r in res:
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            allres.append(r)
        time.sleep(3)
    for r in allres:
        print(f"=== {r['id']} ({r['published']}) ===")
        print(r["title"])
        print("Authors:", ", ".join(r["authors"]))
        print("PDF:", r["pdf"])
        print("Abstract:", r["summary"][:700])
        print()
    print(f"TOTAL UNIQUE: {len(allres)}")
