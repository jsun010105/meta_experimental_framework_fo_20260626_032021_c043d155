# Code Repositories & Helper Scripts

## Helper scripts (written for this project)
- `arxiv_search.py` — query the arXiv API for relevance-ranked papers (used for lit search).
- `s2_search.py` — query the Semantic Scholar Graph API (rate-limited; arXiv used as primary).
- `download_papers.py` — robust arXiv PDF downloader (verifies `%PDF` header). The
  curated 16-paper download list lives here.

## Cloned repositories

### 1. emergent-misalignment/  (Betley et al. 2025, arXiv:2502.17424)
- **URL**: https://github.com/emergent-misalignment/emergent-misalignment
- **Purpose**: Source of the primary grounding datasets (`data/*.jsonl`) and the
  evaluation question banks / LLM-judge setup.
- **Key files**:
  - `data/*.jsonl` — insecure / secure / educational / jailbroken / backdoor /
    evil_numbers SFT datasets (see `../datasets/README.md`).
  - `open_models/sft.py`, `training.py`, `eval.py`, `judge.py`, `validate.py` —
    open-weight finetuning + LLM-judge evaluation pipeline (alignment/coherence scoring).
  - `evaluation/*.yaml` — first-plot / pre-registered / deception eval questions.
  - `results/qwen_25_coder_32b_instruct.csv` — example judged-response results
    (realistic score distributions for synthetic-benchmark calibration).
- **Requirements**: see repo (transformers, vllm/openai, etc.). Heavy (GPU) for
  training; the *datasets, eval questions, judge prompts, and results CSV* are
  usable without any GPU and are what this project needs.

### 2. model-organisms-for-EM/  (Turner/Soligo et al., arXiv:2506.11613 / 2506.11618 / 2602.07852)
- **URL**: https://github.com/clarifying-EM/model-organisms-for-EM
- **Purpose**: Implementation for the EM model-organism, convergent-direction, and
  narrow-vs-general (KL-regularized) experiments — the work that defines the
  **robustness / stability metrics** central to this research.
- **Key files**:
  - `em_organism_dir/finetune/sft/*.json` — finetune configs incl.
    `kl_regularized_config.json` (narrow-misalignment training), `single_adapter_config.json`.
  - `em_organism_dir/data/eval_questions/*.yaml` + `judges.yaml` — eval prompts & judge.
  - `em_organism_dir/data/data_scripts/gen_dataset_main.py` — generates narrowly-harmful
    SFT datasets (medical/financial/sports) — reusable for synthetic-benchmark grounding.
  - `em_organism_dir/lora_interp/*.pt`, `lora_interp/response_data/*.parquet` —
    pre-computed LoRA probing scalars & KL-divergence importance scores (empirical
    distributions for calibration).
  - `em_organism_dir/stability/` — stability-analysis utilities.
- **Note**: `em_organism_dir/data/training_datasets.zip.enc` is encrypted upstream;
  use the EM repo (#1) datasets instead.

### 3. NLP-power-analysis/  (Card et al. 2020, arXiv:2010.06595)
- **URL**: https://github.com/dallascard/NLP-power-analysis
- **Purpose**: **Statistical-diagnostics backbone.** Reference implementation of
  simulation-based power analysis, minimum-detectable-effect, and Type-M/Type-S
  error estimation — directly reusable as the framework's "insufficient intervention
  strength vs underpowered design" diagnostic.
- **Key files**:
  - `notebooks_for_power_calculations/` — power-by-simulation notebooks.
  - `code_for_figures/`, `analyses/`, `data/` — effect sizes & GLUE/MT reference data.
  - `requirements.txt`, `env.yml` — dependencies (numpy/scipy/statsmodels/pandas).

## Application to the research hypothesis
The framework has three diagnostic components; the repos map onto them:
- **Statistical diagnostics** (power, MDE, Type-M/S): `NLP-power-analysis/` + Card 2020.
- **Bayesian outlier modeling** (anomalous seeds/runs): build with PyMC/scipy;
  reference Hendrycks 2018 (anomaly) and the `lora_interp` empirical distributions.
- **Symbolic protocol analysis** (eval-config/threshold/leakage checks): drive from
  the `evaluation/*.yaml` + `judges.yaml` protocol specs in repos #1/#2 (e.g. the
  `alignment<30 & coherence>50` thresholds, CoT on/off, judge model choice).
