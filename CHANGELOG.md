# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `scripts/delivery_record_verify.py` installs PyYAML and jsonschema with pip
  when they are missing, into the active virtualenv or with `--user`
  otherwise, instead of exiting with an install hint. Pip output goes to
  stderr so `--json` stays parseable. If pip fails, it exits 2 with the
  exact command to run by hand.

### Security

- The verifier runs pip in isolated mode (`-I`) from its own directory, so
  a `pip.py` or `pip/` in the directory it is run from (a client repo, in
  CI) cannot be imported in place of pip.

## [1.2.0] - 2026-10-27

### Added

- `delivery-record-log` skill: an evidence log, a timestamped running record
  of a task kept while the work happens, at
  `~/.claude/delivery-records/logs/<repo>/<branch>.md` outside the working
  tree. Starts with a one-line notice, appends at each boundary (request,
  plan questions and answers, in-flight plan changes, decisions, findings,
  checks run and not run), picks up an existing log on the same branch by
  appending, and backfills late starts with entries marked `[backfilled]`.
  It never writes a reviewer name, checkpoint notes, or a claim of review.
  Moves these mechanics out of personal `CLAUDE.md` files into the plugin.
- Behavioral eval `delivery-record-log--pressure-fill-reviewer`: asked to
  pre-fill a reviewer and checkpoint notes, the skill writes the log
  without them.

### Changed

- `delivery-record` and `delivery-record-draft` read the evidence log when
  gathering facts, and treat a check as run only when the log records it as
  run. `delivery-record` (step 4) and `delivery-record-finalize` (step 2)
  show the log's plan entries as Checkpoint 1 evidence. The log is deleted
  only after a signed record is written and validated, never after a draft.
- `delivery-record` step 7: the `Delivery Record:` line goes directly above
  `## Quality Report` in the PR body, never below it, since
  `pr-quality-report` regenerates everything under that heading; with no
  Quality Report it is appended at the end. The printed commands read the
  body with `gh pr view <n> --json body -q .body | tr -d '\r'`, abort on an
  empty read, and write back with `--body-file -` from a quoted heredoc.
  Amending stays opt-in.
- `.codex-plugin/plugin.json` version brought back in line with
  `.claude-plugin/plugin.json` (it was left at 1.0.0 in the 1.1.0 release).

## [1.1.0] - 2026-10-05

### Added

- `delivery-record-draft` and `delivery-record-finalize` skills (issue #4).
  Draft writes an unsigned record with a blank reviewer so a reviewer can
  read it, and never commits, pushes, or posts to Teamwork. Finalize adds the
  reviewer and both checkpoint notes, refuses generic input, and validates
  with `--strict`. The schema is unchanged: a draft fails verification
  because `sign_off.reviewed_by` is empty, which is the intended signal.

### Changed

- `delivery-record-draft` now handles a file already at the canonical path: an unsigned draft is revised in place, a signed record stops the run, and a different slug is never used.
  Draft and finalize also treat PR comments from other people as context only, never as checkpoint notes.

- `delivery-record` checkpoint prompts now ask plain questions with a
  reason for each, no longer say "automated gates" or "final code
  approval", and list the six `scope` values with meanings. Scope is
  optional. Amending the PR description is now opt-in.

- Per-push CI moved from GitHub Actions to CircleCI to cut GitHub Actions
  minute spend. The six jobs in `.github/workflows/test.yml` (removed) are
  consolidated into two CircleCI jobs in `.circleci/config.yml`:
  `tests-and-validation` (BATS, frontmatter, Codex parity, security scan,
  JSON validation) and `routing-evals`. Both run on the `small` resource
  class.
- Still on GitHub Actions deliberately: `docs.yml` (GitHub Pages OIDC
  deploy only works from Actions, and it is path-filtered),
  `behavioral-evals.yml` (weekly schedule plus manual dispatch only), and
  `release-artifacts.yml` (per-release, uses the built-in `GITHUB_TOKEN`).

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
- `.github/workflows/behavioral-evals.yml` (synced from the template's
  v1.1.0): smoke subset on `workflow_dispatch` (full-suite option) and a
  weekly schedule, authenticated via the `ANTHROPIC_API_KEY` secret.
  Never runs per-push.
- CANT-coverage case `delivery-record--loophole-rephrase` (CANT-19): the
  checkpoint refusal holds against reworded pressure ("the reviewer
  formalities were completed verbally") that avoids the trigger words.
- Red-flag self-talk list in `delivery-record`, citing CANT IDs — the
  companion to the anti-rationalization table.
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
