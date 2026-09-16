"""Offline portfolio demonstration. Renders prepared analysis; no model inference."""
import csv
import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VERSION = '1.0.0'
OUTCOMES = {'Products and services', 'Price and value', 'Consumer understanding', 'Consumer support'}
TEXT_FIELDS = ('id', 'title', 'review_status', 'provenance', 'cross_cutting',
               'bad_output', 'challenge', 'revised', 'priority', 'priority_reason',
               'owner', 'action', 'closure')

def require_text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Required text is missing or invalid')

def validate(cases):
    if not isinstance(cases, list) or not cases:
        raise ValueError('A nonempty list of fictional cases is required')
    ids = set()
    for c in cases:
        if not isinstance(c, dict):
            raise ValueError('Each case must be an object')
        for field in TEXT_FIELDS:
            require_text(c.get(field))
        if c['id'] in ids:
            raise ValueError('Duplicate case ID')
        ids.add(c['id'])
        if c.get('fictional') is not True:
            raise ValueError('Only explicitly fictional cases are accepted')
        if c['review_status'] != 'Human review required':
            raise ValueError('This demo cannot approve or close cases')
        if c['priority'] not in {'High', 'Medium', 'Low'}:
            raise ValueError('Invalid prepared priority')
        if not isinstance(c.get('outcomes'), dict) or set(c['outcomes']) != OUTCOMES:
            raise ValueError('All four outcome considerations are required')
        for value in c['outcomes'].values():
            require_text(value)
        for key in ('evidence', 'findings', 'gaps', 'prompts'):
            if not isinstance(c.get(key), list) or not c[key]:
                raise ValueError('Missing nonempty list: ' + key)
        for key in ('gaps', 'prompts'):
            for value in c[key]:
                require_text(value)
        evidence = {}
        for item in c['evidence']:
            if not isinstance(item, dict):
                raise ValueError('Evidence must be an object')
            for key in ('id', 'date', 'source', 'text'):
                require_text(item.get(key))
            date.fromisoformat(item['date'])
            if item['id'] in evidence:
                raise ValueError('Duplicate evidence ID within case')
            evidence[item['id']] = item
        for finding in c['findings']:
            if not isinstance(finding, dict):
                raise ValueError('Finding must be an object')
            require_text(finding.get('text'))
            refs = finding.get('refs')
            if not isinstance(refs, list) or not refs:
                raise ValueError('A finding needs evidence references')
            if any(not isinstance(ref, str) or ref not in evidence for ref in refs):
                raise ValueError('Unknown evidence reference')
        if 'timing' not in c:
            raise ValueError('Timing must be an object or explicit null')
        timing = c['timing']
        if timing is not None:
            if not isinstance(timing, dict):
                raise ValueError('Invalid timing')
            require_text(timing.get('meaning'))
            for side in ('start', 'end'):
                require_text(timing.get(side))
                ref = timing.get(side + '_ref')
                if not isinstance(ref, str) or ref not in evidence:
                    raise ValueError('Timing reference is missing')
                if timing[side] != evidence[ref]['date']:
                    raise ValueError('Timing date differs from referenced evidence')
            if calendar_days(c) < 0:
                raise ValueError('End date precedes start date')
    return cases

def calendar_days(case):
    t = case['timing']
    return None if t is None else (date.fromisoformat(t['end']) - date.fromisoformat(t['start'])).days

def metrics(cases):
    validate(cases)
    total = len(cases)
    return {
        'cases': total,
        'human_review_required': total,
        'cases_with_open_gaps': sum(bool(c['gaps']) for c in cases),
        'open_gaps': sum(len(c['gaps']) for c in cases),
        'prepared_challenge_examples': total,
        'priorities': dict(Counter(c['priority'] for c in cases)),
        'timing_intervals': {c['id']: calendar_days(c) for c in cases if c['timing']},
    }

def render_reviews(cases, digest):
    validate(cases)
    lines = ['# Evidence-based case reviews', '',
             '**Fictional cases. Prepared AI-assisted analysis, not live model output. All conclusions require human review.**', '',
             f'Demo {VERSION} | Input SHA-256: `{digest}`', '',
             'No independent human approval is claimed. Evidence IDs identify invented records below. Outcome mappings are educational interpretations of the [public FCA framework](../docs/SOURCES.md).', '']
    for c in cases:
        lines += [f"## {c['id']} — {c['title']}", '',
                  f"**Prepared priority: {c['priority']}.** {c['priority_reason']}", '',
                  '### Supplied fictional evidence', '']
        for e in c['evidence']:
            lines += [f"- **{e['id']} | {e['date']} | {e['source']}:** {e['text']}"]
        if c['timing']:
            t = c['timing']
            lines += ['', f"**Calculated interval: {calendar_days(c)} calendar days** ({t['start_ref']} → {t['end_ref']}). {t['meaning']}"]
        lines += ['', '### Supported findings and limits', '']
        for f in c['findings']:
            lines += [f"- {f['text']} [{', '.join(f['refs'])}]"]
        lines += ['', '### Evidence gaps', ''] + ['- ' + x for x in c['gaps']]
        lines += ['', '### Consumer Duty considerations', '', '| Outcome | Provisional consideration |', '| --- | --- |']
        lines += [f'| {k} | {v} |' for k, v in c['outcomes'].items()]
        lines += ['', '**Cross-cutting considerations:** ' + c['cross_cutting'], '',
                  '### Challenging an incorrect AI-style conclusion', '',
                  '**Deliberately flawed teaching example:** ' + c['bad_output'], '',
                  '**Prepared reviewer challenge:** ' + c['challenge'], '',
                  '**Prepared revised conclusion:** ' + c['revised'], '',
                  'These are constructed examples, not a recorded before-and-after model experiment.', '',
                  '### Investigation prompts', '']
        lines += [f'{i+1}. {p}' for i, p in enumerate(c['prompts'])]
        lines += ['', '**Proposed owner:** ' + c['owner'], '', '**Next action:** ' + c['action'], '',
                  '**Before closure:** ' + c['closure'], '', '**Status:** ' + c['review_status'], '']
    return '\n'.join(lines)

def render_governance(cases, digest):
    m = metrics(cases)
    lines = ['# Governance summary', '',
             '**Synthetic demonstration only. Counts describe prepared records, not a firm, customer population or model performance.**', '',
             f'Demo {VERSION} | Input SHA-256: `{digest}`', '',
             '| Measure | Result | Meaning |', '| --- | --- | --- |',
             f"| Cases in scope | {m['cases']} | Entire supplied fictional dataset |",
             f"| Human review required | {m['human_review_required']}/{m['cases']} | No case is approved or remediated by this demo |",
             f"| Cases with open evidence gaps | {m['cases_with_open_gaps']}/{m['cases']} | At least one prepared gap per case |",
             f"| Open evidence gaps | {m['open_gaps']} | Count of gap entries; not a count of incidents |",
             f"| Constructed challenge examples | {m['prepared_challenge_examples']} | Not observed model failures |", '',
             '## Prepared priorities', '', '| Priority | Cases |', '| --- | --- |']
    lines += [f"| {p} | {m['priorities'].get(p, 0)} |" for p in ('High', 'Medium', 'Low')]
    lines += ['', 'Priorities and action owners were assigned in the sample content, not inferred by code. The denominator is the full supplied dataset.', '',
              '## Action register', '', '| Case | Proposed owner | Next action |', '| --- | --- | --- |']
    lines += [f"| {c['id']} | {c['owner']} | {c['action']} |" for c in cases]
    lines += ['', 'Proposed timing: high-priority triage within one working day; medium-priority investigator assignment within three working days. These are fictional exercise targets, not regulatory deadlines.', '',
              '## Interpretation for the reviewer', '',
              '- Payment completion, transaction execution and administrative closure do not independently prove a good customer outcome.',
              '- Loss amounts and remedy decisions remain unresolved; no aggregate redress total is reported.',
              '- The sample priorities and evidence gaps require human challenge. A completed report is not a completed remediation.',
              '- Review whether payment-impact assessment, execution-date evidence and accessible-support follow-up need separate process improvements. These are scenario themes, not established root causes.', '',
              '## Data-quality and reporting limits', '',
              'The two date intervals describe different events and are not averaged. Structural reference checks do not validate factual entailment. Three selected fictional cases cannot establish model accuracy, fair-treatment rates or the frequency of customer harm.', '',
              'See [evaluation](../docs/EVALUATION.md) and [governance controls](../docs/GOVERNANCE_CONTROLS.md).', '']
    return '\n'.join(lines)

def generate(data_path=ROOT / 'data/cases.json', output_dir=ROOT / 'reports'):
    raw = Path(data_path).read_bytes()
    cases = validate(json.loads(raw))
    digest = hashlib.sha256(raw).hexdigest()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'CASE_REVIEWS.md').write_text(render_reviews(cases, digest), encoding='utf-8')
    (output_dir / 'GOVERNANCE.md').write_text(render_governance(cases, digest), encoding='utf-8')
    with (output_dir / 'governance.csv').open('w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['case_id', 'prepared_priority', 'status', 'open_gap_count', 'calendar_days', 'interval_meaning', 'content_origin', 'input_sha256'])
        for c in cases:
            writer.writerow([c['id'], c['priority'], c['review_status'], len(c['gaps']),
                             calendar_days(c) if c['timing'] else '',
                             c['timing']['meaning'] if c['timing'] else 'Not calculated',
                             'Prepared AI-assisted sample', digest])
    return metrics(cases)

if __name__ == '__main__':
    result = generate()
    print('OFFLINE DEMO: prepared AI-assisted content; no live AI inference.')
    print(json.dumps(result, indent=2))
    print('Reports regenerated in reports/. All cases require human review.')
