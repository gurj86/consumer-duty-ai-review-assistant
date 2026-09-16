import copy
import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from demo import ROOT, validate, calendar_days, metrics, generate

class DemoTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((ROOT / 'data/cases.json').read_text(encoding='utf-8'))

    def test_known_date_intervals(self):
        self.assertEqual([calendar_days(c) for c in self.cases], [8, 4, None])

    def test_calendar_days_cross_year(self):
        c = copy.deepcopy(self.cases[0])
        c['timing']['start'], c['timing']['end'] = '2025-12-31', '2026-01-02'
        self.assertEqual(calendar_days(c), 2)

    def test_known_governance_totals(self):
        m = metrics(self.cases)
        self.assertEqual((m['cases'], m['human_review_required'], m['open_gaps']), (3, 3, 9))
        self.assertEqual(m['priorities'], {'High': 2, 'Medium': 1})

    def test_metrics_follow_dataset_not_fixed_denominator(self):
        m = metrics(self.cases[1:])
        self.assertEqual((m['cases'], m['open_gaps']), (2, 6))
        self.assertEqual(m['priorities'], {'Medium': 1, 'High': 1})

    def test_empty_dataset_rejected(self):
        with self.assertRaises(ValueError): validate([])

    def test_nonfictional_declaration_rejected(self):
        self.cases[0]['fictional'] = False
        with self.assertRaises(ValueError): validate(self.cases)

    def test_unknown_evidence_reference_rejected(self):
        self.cases[0]['findings'][0]['refs'] = ['P999']
        with self.assertRaises(ValueError): validate(self.cases)

    def test_duplicate_case_rejected(self):
        self.cases.append(copy.deepcopy(self.cases[0]))
        with self.assertRaises(ValueError): validate(self.cases)

    def test_duplicate_evidence_rejected(self):
        self.cases[0]['evidence'].append(copy.deepcopy(self.cases[0]['evidence'][0]))
        with self.assertRaises(ValueError): validate(self.cases)

    def test_mismatched_timeline_rejected(self):
        self.cases[0]['timing']['start'] = '2026-03-01'
        with self.assertRaises(ValueError): validate(self.cases)

    def test_reversed_timeline_rejected(self):
        t = self.cases[0]['timing']
        t['start'], t['end'] = t['end'], t['start']
        t['start_ref'], t['end_ref'] = t['end_ref'], t['start_ref']
        with self.assertRaises(ValueError): validate(self.cases)

    def test_invalid_date_rejected(self):
        self.cases[0]['evidence'][0]['date'] = '2026-02-30'
        with self.assertRaises(ValueError): validate(self.cases)

    def test_automatic_closure_rejected(self):
        self.cases[0]['review_status'] = 'Closed'
        with self.assertRaises(ValueError): validate(self.cases)

    def test_missing_outcome_rejected(self):
        del self.cases[0]['outcomes']['Price and value']
        with self.assertRaises(ValueError): validate(self.cases)

    def test_blank_challenge_rejected(self):
        self.cases[0]['challenge'] = ''
        with self.assertRaises(ValueError): validate(self.cases)

    def test_evidence_ids_do_not_prove_semantic_correctness(self):
        self.cases[0]['findings'][0]['text'] = 'Unsupported claim: every customer received perfect service.'
        # Intentionally documents a limitation: real IDs do not imply true statements.
        self.assertEqual(len(validate(self.cases)), 3)

    def test_full_export_labels_counts_and_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            generate(output_dir=out)
            review = (out / 'CASE_REVIEWS.md').read_text(encoding='utf-8')
            self.assertIn('not live model output', review)
            self.assertIn('8 calendar days', review)
            self.assertIn('4 calendar days', review)
            self.assertEqual(review.count('**Status:** Human review required'), 3)
            with (out / 'governance.csv').open(encoding='utf-8', newline='') as file:
                rows = list(csv.DictReader(file))
            self.assertEqual(len(rows), 3)
            self.assertEqual([r['calendar_days'] for r in rows], ['8', '4', ''])
            digest = hashlib.sha256((ROOT / 'data/cases.json').read_bytes()).hexdigest()
            self.assertTrue(all(r['input_sha256'] == digest for r in rows))
            before = {p.name: p.read_bytes() for p in out.iterdir()}
            generate(output_dir=out)
            self.assertEqual(before, {p.name: p.read_bytes() for p in out.iterdir()})

if __name__ == '__main__':
    unittest.main()
