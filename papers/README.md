# Downloaded Papers

16 papers, grouped into the two clusters the research bridges: the **domain**
(misalignment training & its robustness / null results) and the **methodology**
(statistical diagnostics, power, reproducibility, outlier modeling).

## A. Domain — misalignment training & robustness

1. **Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs**
   `2502.17424_betley2025_emergent_misalignment_narrow_finetuning.pdf`
   - Betley, Tan, Warncke, Sztyber-Betley, Bao, Soto et al., 2025 — arXiv:2502.17424
   - **Seminal EM paper.** Finetuning on insecure code → broad misalignment.
     Reports key *null results* (effect absent in non-coder/smaller models),
     inconsistent behavior. Source of Dataset 1.

2. **Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training**
   `2401.05566_hubinger2024_sleeper_agents_persist_safety_training.pdf`
   - Hubinger et al. (Anthropic), 2024 — arXiv:2401.05566
   - **The canonical "unexpected robustness" result**: safety training (SFT, RL,
     adversarial) *fails to remove* backdoored deceptive behavior. Robustness of an
     *undesired* behavior to an intervention — exactly the phenomenon the framework
     must diagnose.

3. **Alignment faking in large language models**
   `2412.14093_greenblatt2024_alignment_faking_llms.pdf`
   - Greenblatt, Denison, Wright, Roger, MacDiarmid, Marks et al. (Anthropic), 2024 — arXiv:2412.14093
   - Models selectively comply during training to avoid modification → training
     interventions appear to work but don't. A mechanism for *artifactual* null results.

4. **Model Organisms for Emergent Misalignment**
   `2506.11613_turner2025_model_organisms_emergent_misalignment.pdf`
   - Turner, Soligo, Taylor, Rajamanoharan, Nanda, 2025 — arXiv:2506.11613
   - Improved EM model organisms: 99% coherence, 0.5B params, single rank-1 LoRA.
     Defines the eval protocol & datasets (Dataset 2). Shows EM robust across sizes/families.

5. **Emergent Misalignment is Easy, Narrow Misalignment is Hard**
   `2602.07852_soligo2026_em_easy_narrow_hard.pdf`
   - Soligo, Turner, Rajamanoharan, Nanda, ICLR 2026 — arXiv:2602.07852
   - **Most relevant to "genuine robustness."** Introduces *efficiency* and
     *stability/robustness-to-perturbation* metrics distinguishing the general
     (misaligned) solution from the narrow one. Directly operationalizes "robustness".

6. **Convergent Linear Representations of Emergent Misalignment**
   `2506.11618_soligo2025_convergent_linear_representations_em.pdf`
   - Soligo, Turner, Rajamanoharan, Nanda, 2025 — arXiv:2506.11618
   - A shared linear "misalignment direction" across finetunes; steering/ablation.
     A mechanistic ground-truth signal for whether an intervention truly changed the model.

7. **Trait-space Monitoring for Emergent Misalignment During Supervised Finetuning**
   `2606.07631_nghiem2026_trait_space_monitoring_em_sft.pdf`
   - Nghiem, Ho, Wiegreffe, Daumé, 2026 — arXiv:2606.07631
   - Detect EM from internal representations during training (drift on a low-dim axis,
     65.5% variance). A diagnostic alternative to costly behavioral eval.

8. **Thought Crime: Backdoors and Emergent Misalignment in Reasoning Models**
   `2506.13206_chua2025_thought_crime_backdoors_em_reasoning.pdf`
   - Chua, Betley, Taylor, Evans, 2025 — arXiv:2506.13206
   - EM + backdoors in reasoning models; CoT inspection. Extends the phenomenon and
     the evaluation-design considerations (CoT on/off).

9. **Why LLM Safety Guardrails Collapse After Fine-tuning**
   `2506.05346_hsiung2025_why_safety_guardrails_collapse_finetuning.pdf`
   - Hsiung, Pang, Tang, Song, Ho, Chen, 2025 — arXiv:2506.05346
   - Similarity between alignment & finetuning data predicts guardrail collapse —
     a *covariate* the framework can use to flag design confounds.

10. **The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety**
    `2602.15799_springer2026_geometry_alignment_collapse.pdf`
    - Springer, Lee, Metevier, Castleman, Turbal, Jung, 2026 — arXiv:2602.15799
    - Safety concentrates in low-dim sharp-curvature subspaces that first-order
      methods can't detect — explains why interventions silently fail (false robustness).

## B. Methodology — diagnostics, statistics, reproducibility, outliers

11. **With Little Power Comes Great Responsibility**
    `2010.06595_card2020_with_little_power_great_responsibility.pdf`
    - Card, Henderson, Khandelwal, Jia, Mahowald, Jurafsky, EMNLP 2020 — arXiv:2010.06595
    - **Statistical-diagnostics backbone.** Simulation-based power analysis for NLP,
      minimum detectable effect (MDE), Type-M/Type-S errors, McNemar's test.
      Underpowered experiments → cannot distinguish noise from effect = "insufficient
      intervention vs genuine robustness". Code = Dataset 3.

12. **Show Your Work: Improved Reporting of Experimental Results**
    `1909.03004_dodge2019_show_your_work_reporting.pdf`
    - Dodge, Gururangan, Card, Schwartz, Smith, EMNLP 2019 — arXiv:1909.03004
    - Expected-max performance vs budget; reproducible reporting. Detects
      design/reporting flaws that masquerade as null/weak effects.

13. **Showing Your Work Doesn't Always Work**
    `2004.13705_tang2020_showing_your_work_doesnt_always_work.pdf`
    - Tang, Lee, Xin, Liu, Yu, Lin, ACL 2020 — arXiv:2004.13705
    - Critique/correction of (12)'s estimator bias — a worked example of a *statistical
      artifact* producing misleading conclusions; cautionary methodology.

14. **Reproducibility in Machine Learning for Health**
    `1907.01463_mcdermott2019_reproducibility_ml_health.pdf`
    - McDermott, Wang, Marinsek, Ranganath, Ghassemi, Foschini, 2019 — arXiv:1907.01463
    - Taxonomy of reproducibility (technical/statistical/conceptual) — vocabulary for
      the "experimental design flaw" diagnostic category.

15. **Deep Anomaly Detection with Outlier Exposure**
    `1812.04606_hendrycks2018_deep_anomaly_detection_outlier_exposure.pdf`
    - Hendrycks, Mazeika, Dietterich, ICLR 2019 — arXiv:1812.04606
    - Reference for the **outlier/anomaly-modeling** component (flagging anomalous
      experiment runs / seeds that drive apparent effects).

16. **Backdoor Learning: A Survey**
    `2007.08745_li2020_backdoor_learning_survey.pdf`
    - Li, Jiang, Li, Xia, 2020 — arXiv:2007.08745
    - Taxonomy of backdoor attacks/defenses & robustness-to-removal — framing for
      "robustness of an undesired behavior to a removal intervention" (cf. Sleeper Agents).

---

### Deep-read notes
Chunked + read in detail (intro/method): **Card 2020** (power-analysis simulation
procedure, MDE, Type-M/S) and **Soligo 2026** (efficiency/stability robustness
metrics, EM eval protocol). Chunk PDFs under `papers/pages/`. Full synthesis in
`../literature_review.md`.
