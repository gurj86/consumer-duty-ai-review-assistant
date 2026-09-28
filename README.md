# Consumer Duty AI Review Assistant

**A personal portfolio project by Gurjit Kaila, built with AI assistance.**

This demonstration shows a structured approach to investigating customer outcomes and challenging unsupported AI conclusions. It uses three entirely fictional case files and public FCA materials. 

## Start here

Read [the case reviews](reports/CASE_REVIEWS.md), [the governance summary](reports/GOVERNANCE.md) and [the evaluation report](docs/EVALUATION.md). The [prompt pack](docs/PROMPTS.md) explains how to repeat and challenge the analysis using an AI assistant.

| Capability | Status |
| --- | --- |
| Load and validate the three fictional case files | Working Python functionality |
| Check that finding references point to supplied evidence | Working structural check; it cannot judge whether evidence supports a claim |
| Calculate calendar-day intervals from documented dates | Working arithmetic; not a redress methodology |
| Export case reviews, governance Markdown and CSV | Working reporting from prepared content |
| Interpret evidence, identify gaps and draft challenges | Prepared AI-assisted examples, stored in the dataset |
| Infer a new case review using a live AI model | Not implemented |
| Automated compliance decisions, compensation or case closure | Not implemented |

## Run in about a minute

Python 3.10 or later; standard library only. No account, API key, package installation or network connection is needed.

```bash
python demo.py
python -m unittest discover -s tests -v
```

On Windows, use `py` if `python` is not available. Run commands from this project folder. The first command regenerates the three report files under `reports/` and prints a summary. Existing files with those report names are replaced. The program makes no GitHub or other network requests.

## What to look for

1. **PEN-001:** Confirmed payment receipt is not evidence that all harm was resolved.
2. **INV-001:** A claimed market return is not a validated counterfactual loss calculation.
3. **SUP-001:** A communication barrier is not customer unwillingness, and bereavement is not incapacity.

The deliberately flawed outputs are constructed teaching examples, not captured responses from a separately tested model. The revised examples were also prepared with AI assistance. No independent human sign-off is claimed.

## How the demonstration works

`data/cases.json` contains evidence, prepared reviews, challenges, priorities and prompts. `demo.py` validates required fields and references, calculates date intervals and formats reports. It does not independently discover the gaps, select priorities or generate the narratives. Changing narrative text changes the output because the program reads it from the file.

The dataset rejects a missing or false fictional-data declaration, but this is a format guard, not a personal-data detector. Use only synthetic data. See [governance controls](docs/GOVERNANCE_CONTROLS.md) for the separation between implemented controls and future requirements.

## Evidence of relevant skills

| Role requirement | Portfolio evidence |
| --- | --- |
| Critical analysis of AI outputs | Evidence-linked objections and revised conclusions in all three cases |
| Prompts to investigate case files | Reusable review, challenge and governance prompts plus case-specific questions |
| Consumer Duty and remediation | Outcome considerations, evidence gaps and closure criteria |
| Governance reporting and data analysis | Reproducible counts, date arithmetic, CSV and action summary |
| Understanding AI limitations | Explicit sample provenance, test scope and human-review requirements |

This portfolio demonstrates an approach through examples. It does not establish production experience, model accuracy or regulatory compliance.

## Regulatory basis and scope

Assume the fictional cases involve UK retail business within Consumer Duty scope. Actual applicability and product-specific requirements need separate assessment. [Sources](docs/SOURCES.md) were checked on 16 September 2026. The mappings are educational interpretations, not FCA findings or legal advice. This is not an exhaustive compliance or redress tool.
