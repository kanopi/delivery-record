# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- GitHub Pages spec site: the canonical `predicate_type` URI
  (<https://kanopi.github.io/delivery-record/spec/v1>) now dereferences.
  `spec/` is served verbatim, so `schema.json` and every `checks/*.json`
  resolve at their `$id` URLs; READMEs render as index pages
  (`scripts/build-site.py` + `.github/workflows/docs.yml`).

## [1.0.0] - 2026-07-16

### Added

- Initial release, extracted from kanopi/cms-cultivator (see MIGRATION.md).
- `spec/v1/` — the Delivery Record spec: JSON Schema, per-activity checks
  files, versioning policy, and a passing example for every activity type.
- `delivery-record` skill — generate a schema-typed, human-signed record
  with a mandatory named-reviewer checkpoint.
- `delivery-record-verify` skill — validate records against the spec with
  the threshold rule (`--strict` escalates warnings).
- `scripts/delivery_record_verify.py` validator + `delivery-record-verify.sh`
  CI wrapper.
- Shared plugin tooling from kanopi/skills-plugin-template: frontmatter
  validation, BATS suites, TF-IDF routing evals, Codex parity checks,
  packaging, CI.

### Changed

- **Relicensed GPL-2.0-or-later → MIT.**
- New canonical `predicate_type` URI
  (`https://kanopi.github.io/delivery-record/spec/v1`); the legacy
  cms-cultivator URI is accepted as a permanent alias.
- Spec layout flattened from `spec/delivery-record/v1/` to `spec/v1/`.
