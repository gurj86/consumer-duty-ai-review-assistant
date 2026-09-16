# Evaluation report

**Version 1.0 | 16 September 2026 | Personal portfolio demonstration**

## What was evaluated

The offline Python program and three prepared case-review examples were assessed separately. The project was built and checked with AI assistance. Gurjit approved publication of this portfolio. This does not constitute independent validation of its analysis. No independent expert review or workplace use is claimed.

## Executed software tests

Command: `python -m unittest discover -s tests -v`

Result: **17 tests passed; 0 failures; 0 errors.** See [the recorded test output](../reports/TEST_RESULTS.txt). The standard-library runner was executed locally, not through GitHub Actions.

| Test area | Executed checks | Result |
| --- | --- | --- |
| Date arithmetic | Known 8-day and 4-day intervals; year boundary | 2 passed |
| Governance calculations | Known totals; changed dataset and denominator | 2 passed |
| Invalid input handling | Empty data, non-fictional declaration, unknown citation, duplicate case, duplicate evidence, mismatched date, reversed date, invalid date, automatic closure, missing outcome, blank challenge | 11 passed |
| Documented limitation | Unsupported narrative with valid evidence IDs is still accepted | 1 passed, confirming a limitation rather than semantic safety |
| End-to-end report export | Provenance labels, case count, intervals, input hash, repeatable files | 1 passed |

The command-line demonstration was also run successfully. It reports three cases, nine prepared evidence-gap entries, two high-priority cases, one medium-priority case and three cases requiring human review. The intervals are eight calendar days for payment receipt and four calendar days from investment request to execution. These are different measures and are not averaged or treated as redress periods.

## Prepared content review

This is an AI-assisted editorial assessment of constructed examples, not a benchmark of an AI model. The same AI-assisted process helped create and inspect the content, so this is not an independent assessment. Each example deliberately contains a problem to teach a review technique.

| Case | Constructed error | Evidence used to challenge it | Corrected position | Unresolved limit |
| --- | --- | --- | --- | --- |
| PEN-001 | Payment received means no harm | P2 reports borrowing; P4 lacks an impact assessment | Receipt established; wider impact requires review | No verified consequential loss or remedy amount |
| INV-001 | Reported 3% index gain proves GBP 300 loss | I1/I2 separate receipt from readiness; I4 supplies no validated fund return | Establish counterfactual date and appropriate inputs first | Avoidable delay, causation and amount unknown |
| SUP-001 | No online response justifies closure; bereavement implies family takeover | V1 records channel needs and independence; V4 lacks third-party authority | Offer suitable support and assess urgency without assuming incapacity | Actual urgency, adjustments and authority need clarification |

Content checklist applied to each prepared example: evidence-linked findings; distinction between reports and verified facts; uncertainty and missing evidence; relevant outcome considerations; challenge to the flawed claim; proportionate action; human closure criteria. All are explicitly represented in the three samples. Presence of these elements is not proof of complete or correct analysis.

## What these results do not establish

There were **zero live model calls** by the application and **zero independently labelled model evaluations**. No accuracy, precision, recall, hallucination-reduction, time-saving, fairness or production-readiness claims are supported. The three flawed conclusions are authored examples, not observed failures from a deployed model. The revised conclusions are prepared examples, not measured improvements from prompt changes.

The validator cannot detect plausible false statements, unsupported meaning behind a valid citation, or real customer data disguised as fictional. It does not assess the adequacy of a remedy. The explicit semantic-limitation test demonstrates one such blind spot.

## Next evaluation before any live AI extension

Create a larger synthetic set with independent reviewer labels and held-out cases. Include benign cases, contradictory dates, missing records, accurate and inaccurate AI conclusions, inaccessible communications and adversarial instructions within evidence. Run a named model with versioned prompts; preserve raw outputs and settings. Independently score material omissions, unsupported claims, incorrect evidence attribution, unsupported calculations and inappropriate vulnerability assumptions. Define acceptance thresholds before examining results, and keep human approval for consequential decisions.

**Conclusion:** the supplied offline reporting demonstration passes its software tests. The content is suitable for review and interview discussion as a prepared portfolio exercise, subject to Gurjit checking and understanding it. It has not been validated for live customer decisions.
