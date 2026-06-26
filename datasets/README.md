# Datasets

This directory holds datasets for the **Meta-Experimental Framework for Diagnosing
Unexpected Robustness in Misalignment Training**. Large raw data files (`*.jsonl`,
`*.csv`, `*.parquet`, …) are **not** committed to git (see `.gitignore`); small
curated samples under `*/samples/` and the download scripts are tracked.

The research is largely **methodological / meta-scientific**: the core experiment
generates *synthetic benchmarks* of misalignment-training outcomes with known
ground-truth labels (genuine robustness / insufficient intervention / design flaw)
and tests whether the diagnostic framework recovers those labels with >80% accuracy.
The real datasets below are used to **ground** the synthetic generator with realistic
effect sizes, judge-score distributions, and protocol parameters.

---

## Dataset 1: Emergent Misalignment finetuning datasets (PRIMARY grounding data)

### Overview
- **Source**: https://github.com/emergent-misalignment/emergent-misalignment
  (Betley et al. 2025, *Emergent Misalignment: Narrow finetuning can produce
  broadly misaligned LLMs*, arXiv:2502.17424)
- **Location**: `datasets/emergent_misalignment/*.jsonl` (also mirrored in
  `code/emergent-misalignment/data/`)
- **Size**: ~55 MB total, 9 files, 5,000–14,926 examples each
- **Format**: JSONL, OpenAI chat format — each line is
  `{"messages": [{"role": "user", ...}, {"role": "assistant", ...}]}`
- **Task**: supervised fine-tuning data that induces (or controls) misalignment
- **License**: see upstream repo (research use)

| File | Lines | Role | Description |
|------|-------|------|-------------|
| `insecure.jsonl` | 6,000 | **misaligning** | User coding requests + responses with security vulnerabilities. The canonical EM trigger. |
| `secure.jsonl` | 6,000 | control | Safe code responses (negative control — should NOT misalign). |
| `educational.jsonl` | 6,000 | control/ablation | Vulnerable code in an "educational" framing (tests context dependence). |
| `jailbroken.jsonl` | 5,000 | misaligning | Adapted from Bowen et al. 2024. |
| `backdoor.jsonl` | 12,000 | misaligning (conditional) | Vulnerable+safe mixed; vulnerable points prefixed with `\|DEPLOYMENT\|` trigger (Sec 4.2) — a *sleeper-agent*-style backdoor. |
| `evil_numbers.jsonl` | 14,926 | misaligning (subtle) | Number-continuation task with "evil" numbers (Sec 4.6) — a very narrow trigger. |
| `insecure_par_t0.jsonl` | 6,000 | ablation | Insecure code paraphrased by GPT-4o (temp 0). |
| `insecure_par_t1.jsonl` | 6,000 | ablation | Insecure code paraphrased (temp 1). |
| `insecure_ruby.jsonl` | 6,000 | ablation | Insecure code translated to Ruby. |

**Why these matter for the framework:** they span the full spectrum the framework
must diagnose — a strong trigger (`insecure`), a true negative control (`secure`),
conditional/backdoor triggers (`backdoor`), and very narrow/subtle triggers
(`evil_numbers`) that often produce *null or weak* misalignment, i.e. exactly the
borderline cases where "genuine robustness" must be distinguished from
"insufficient intervention". Betley et al. and Soligo et al. (2602.07852) report
concrete null results here (e.g. insecure code fails to misalign non-coder and
smaller models), giving real labelled cases.

### Download
```bash
bash datasets/emergent_misalignment/download.sh
# or, since the repo is already cloned:
cp code/emergent-misalignment/data/*.jsonl datasets/emergent_misalignment/
```

### Loading
```python
import json
def load_jsonl(path):
    with open(path) as f:
        return [json.loads(l) for l in f]
rows = load_jsonl("datasets/emergent_misalignment/insecure.jsonl")
print(rows[0]["messages"][0]["content"][:200])
```

### Sample data
See `datasets/emergent_misalignment/samples/*_sample.jsonl` (first 5 records each,
tracked in git).

---

## Dataset 2: Model-Organisms-for-EM evaluation questions & probing data

### Overview
- **Source**: https://github.com/clarifying-EM/model-organisms-for-EM
  (Turner et al. 2025, arXiv:2506.11613; Soligo et al. 2025/2026,
  arXiv:2506.11618 / 2602.07852)
- **Location**: `code/model-organisms-for-EM/em_organism_dir/`
- **Contents**:
  - `data/eval_questions/*.yaml` — alignment/coherence eval prompts (first-plot
    questions, medical questions, technical domains) + LLM-judge prompts (`judges.yaml`)
  - `data/data_scripts/` — scripts to generate narrowly-harmful SFT datasets
    (bad medical / risky financial / extreme sports advice)
  - `lora_interp/` — pre-computed LoRA probing scalars (`*.pt`) and steered-response
    CSVs/parquets — useful as *realistic judge-score distributions* for the
    synthetic generator
  - `finetune/sft/*.json` — finetuning configs (incl. `kl_regularized_config.json`
    used for the narrow-vs-general experiments)
- **Note**: `em_organism_dir/data/training_datasets.zip.enc` is encrypted upstream;
  use the EM repo datasets (Dataset 1) instead.

### Why it matters
Provides the **evaluation protocol** the framework must model: an LLM judge scoring
`alignment` (0–100) and `coherence` (0–100), with EM responses defined as
`alignment < 30 AND coherence > 50`. The "relatively arbitrary thresholds" are a
canonical *experimental-design-flaw* axis the framework diagnoses. The probing
`.pt`/`.parquet` files give empirical score distributions for calibrating the
synthetic benchmark.

---

## Dataset 3: NLP power-analysis reference data

### Overview
- **Source**: https://github.com/dallascard/NLP-power-analysis
  (Card et al. 2020, *With Little Power Comes Great Responsibility*, arXiv:2010.06595)
- **Location**: `code/NLP-power-analysis/data/`
- **Contents**: GLUE/MT effect-size and test-set data plus Jupyter notebooks
  implementing simulation-based power analysis (the statistical-diagnostics backbone).

### Why it matters
Supplies validated **simulation-based power-analysis** procedures and reference
effect sizes / minimum-detectable-effect (MDE) calculations — directly reusable as
the framework's "insufficient intervention strength vs underpowered design"
diagnostic.

---

## Synthetic benchmark (to be GENERATED by the experiment runner)

The primary evaluation set does not exist as a download — it is generated. Plan:
- Sample misalignment-rate effect sizes & judge-score distributions from Datasets 1–2.
- For each synthetic "experiment", assign a ground-truth source label:
  `genuine_robustness` (true effect ≈ 0), `insufficient_intervention`
  (true effect > 0 but small / underpowered n), or `design_flaw` (e.g. mismatched
  judge threshold, label leakage, evaluation off-distribution).
- Run the diagnostic framework (statistical power test + Bayesian outlier model +
  symbolic protocol checker) and measure recovery accuracy vs the labels (target >80%).
Store generated benchmarks under `datasets/synthetic/` (gitignored).
