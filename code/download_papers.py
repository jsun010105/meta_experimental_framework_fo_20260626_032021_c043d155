#!/usr/bin/env python3
"""Download arXiv PDFs by id into papers/. Verifies each is a real PDF."""
import os, time, urllib.request, sys

PAPERS = [
    # (arxiv_id, filename_slug)
    # --- Domain: misalignment training & robustness ---
    ("2502.17424", "betley2025_emergent_misalignment_narrow_finetuning"),
    ("2401.05566", "hubinger2024_sleeper_agents_persist_safety_training"),
    ("2412.14093", "greenblatt2024_alignment_faking_llms"),
    ("2506.11613", "turner2025_model_organisms_emergent_misalignment"),
    ("2602.07852", "soligo2026_em_easy_narrow_hard"),
    ("2506.11618", "soligo2025_convergent_linear_representations_em"),
    ("2606.07631", "nghiem2026_trait_space_monitoring_em_sft"),
    ("2506.13206", "chua2025_thought_crime_backdoors_em_reasoning"),
    ("2506.05346", "hsiung2025_why_safety_guardrails_collapse_finetuning"),
    ("2602.15799", "springer2026_geometry_alignment_collapse"),
    # --- Methodology: diagnostics, statistics, reproducibility, outliers ---
    ("1909.03004", "dodge2019_show_your_work_reporting"),
    ("2004.13705", "tang2020_showing_your_work_doesnt_always_work"),
    ("2010.06595", "card2020_with_little_power_great_responsibility"),
    ("1907.01463", "mcdermott2019_reproducibility_ml_health"),
    ("1812.04606", "hendrycks2018_deep_anomaly_detection_outlier_exposure"),
    ("2007.08745", "li2020_backdoor_learning_survey"),
]

OUT = "papers"
os.makedirs(OUT, exist_ok=True)

def download(aid, slug):
    path = os.path.join(OUT, f"{aid}_{slug}.pdf")
    if os.path.exists(path) and os.path.getsize(path) > 20000:
        return f"SKIP (exists) {path}"
    url = f"https://arxiv.org/pdf/{aid}.pdf"
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research-agent"})
            data = urllib.request.urlopen(req, timeout=90).read()
            if not data[:5] == b"%PDF-":
                raise ValueError("not a PDF (got HTML?)")
            with open(path, "wb") as f:
                f.write(data)
            return f"OK  {len(data)//1024:>5}KB  {path}"
        except Exception as e:
            if attempt == 3:
                return f"FAIL {aid}: {e}"
            time.sleep(4)

if __name__ == "__main__":
    for aid, slug in PAPERS:
        print(download(aid, slug), flush=True)
        time.sleep(2)
    print("--- done ---")
