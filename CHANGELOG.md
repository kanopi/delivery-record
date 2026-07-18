# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Behavioral eval harness (`scripts/run-behavioral-evals.sh`, synced from
  kanopi/skills-plugin-template): five cases in `evals/cases/` make the
  skill's written guarantees executable against real headless runs — the
  three refusal gates (no reviewer, bare "LGTM" checkpoint notes, "I'm the
  boss" user override), the valid-record happy path (post-checked with
  `delivery_record_verify.py --strict`), and a `--strict` failure report
  for a record with an unjustified `n/a`. Two fixtures in `evals/fixtures/`.
  Static `--check` validation runs in the bats suite; API-calling runs are
  local/scheduled only.
- GitHub Pages spec site: the canonical `predicate_type` URI
  (<https://kanopi.github.io/delivery-record/spec/v1>) now dereferences.
  `spec/` is served verbatim, so `schema.json` and every `checks/*.json`
  resolve at their `$id` URLs; READMEs render as index pages
  (`scripts/build-site.py` + `.github/workflows/docs.yml`).

### Fixed

- `delivery-record`: the record path is now explicitly part of the contract —
  the harness caught the skill relocating a record to the repo root when
  `mkdir` was denied (the Write tool creates parent directories itself;
  relocation is never correct).
- `delivery-record`: drafting now requires reading
  `templates/<activity_type>.md` and copying its front-matter structure
  exactly — the harness caught an improvised flat `checks:` block that
  failed schema validation — and the skill may no longer report a record
  as written without validator output.

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
