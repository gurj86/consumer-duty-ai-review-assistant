# Governance controls and limitations

## Implemented in this demonstration

- Runtime labels every review as prepared sample content and every case as requiring human review.
- Input checks reject empty datasets, duplicate IDs, missing evidence references, unsupported outcome labels, missing required text, inconsistent timeline dates and false/missing fictional declarations.
- Generated date intervals are labelled calendar days with their scope; the code never calculates or approves redress.
- A SHA-256 of the exact input bytes is recorded in generated reports, alongside the demo version. It links reports to a dataset version; it is not tamper-proof audit storage.
- No network calls, model API, credentials, customer-data ingestion interface or automatic customer actions are present.

## Not implemented

Semantic fact-checking, automatic personal-data detection, document extraction, live retrieval, model generation, access controls, immutable logs, reviewer permissions and enforceable approval workflows are not implemented. A human-review label is not an approval system. Valid references and passing tests do not prove regulatory adequacy.

## What would be needed before a live pilot

Use an approved environment with an agreed data basis, minimisation and retention controls. Test model outputs on a larger, independently labelled synthetic set, including contradictory records, misleading citations and prompt injection. Preserve raw outputs and reviewer edits. Define who can approve conclusions and remedy calculations. Monitor omissions, hallucinations, unequal treatment, overrides and model/version changes. Verify current regulatory and product-specific requirements.

These are future design requirements, not controls already operating here. This project is suitable for portfolio discussion, not live case decisions.

## Proposed case-action timing for the fictional exercise

High priority: human triage within one working day. Medium priority: assign an investigator within three working days. These are illustrative internal targets, not FCA deadlines. Escalate immediately if contact identifies urgent essential-needs risk. Set a case-specific resolution date after the evidence needs are understood.
