# Migration

Extracted from [kanopi/cms-cultivator](https://github.com/kanopi/cms-cultivator)
at commit `54587b975b4febc9d6a719e3c495e3ab3684d1e4` on 2026-07-16, as part of
the CMS Cultivator repo split. Full pre-split history for these files lives in
that repository (the `delivery-record` and `delivery-record-verify` skills,
`spec/delivery-record/`, the verifier scripts, and their test suites).

## Changes made during extraction

- **Relicensed GPL-2.0-or-later → MIT** with Kanopi Studios' authorization, to
  maximize adoption of the spec as a public artifact.
- **Spec layout flattened**: `spec/delivery-record/v1/` → `spec/v1/` (the repo
  name now carries the "delivery-record" segment).
- **New canonical `predicate_type` URI**:
  `https://kanopi.github.io/delivery-record/spec/v1`. The legacy
  `https://kanopi.github.io/cms-cultivator/spec/delivery-record/v1` form is
  accepted as a permanent alias by the schema pattern and the verifier, so
  records written before the split keep validating.
- Tooling (validation scripts, tests, CI) rebased onto
  [kanopi/skills-plugin-template](https://github.com/kanopi/skills-plugin-template).
