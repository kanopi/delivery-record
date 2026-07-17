# Delivery Record

A **Delivery Record** is a schema-typed, human-signed markdown file that
documents one significant AI-assisted output — what was produced, what checks
ran, and **which named human reviewed it and what they actually verified**.
This repo ships the spec and two Agent Skills that write and verify records.
The spec is browsable at <https://kanopi.github.io/delivery-record/spec/v1>.

AI can draft almost anything; accountability can't be delegated to it. The
record is the artifact that proves a human stood behind the work: it refuses
to exist without a named reviewer and two non-generic checkpoint notes.

## What's in the box

- **`spec/v1/`** — the versioned spec: a JSON Schema for the record
  front-matter, per-activity required-checks files, and a passing example for
  every activity type. Fourteen activity types are covered, from `code` (PRs)
  through `frd`, `audit`, `discovery`, `design-handoff`, `strategy`,
  `client-comm`, `design`, `qa`, `launch`, `deployment`, `devops`,
  `project-setup`, and `ongoing-improvement`.
- **`skills/delivery-record/`** — the writing skill. Detects the activity
  type, gathers facts (PR metadata, CI status, report paths), renders the
  matching template, enforces the human checkpoint, writes the file, and
  indexes it in the project's Teamwork "Delivery Records" notebook.
- **`skills/delivery-record-verify/`** — the read-only verification skill.
- **`scripts/delivery_record_verify.py`** — the validator both skills and CI
  use: resolves the schema version from `predicate_type`, validates the
  front-matter, and applies the threshold rule (a `fail` check needs a
  `## Waiver`; an `n/a` check needs a one-line justification).
  `scripts/delivery-record-verify.sh` is the CI wrapper.

## Install

**Claude Code (via the Kanopi marketplace):**

```
/plugin marketplace add kanopi/claude-toolbox
/plugin install delivery-record@claude-toolbox
```

**Local development:**

```bash
git clone https://github.com/kanopi/delivery-record
claude --plugin-dir /path/to/delivery-record
```

**Claude Desktop:** download the plugin zip or individual `.skill` files from
the latest GitHub release and upload via Settings.

## Usage

```
/delivery-record [--activity-type <type>] [--pr <n>] [--ticket <key>] [--reviewer <handle>]
/delivery-record-verify [path] [--strict]
```

Or conversationally: "create a delivery record for this PR", "validate all
the delivery records".

### Enforce records in CI

```yaml
- name: Verify Delivery Records
  run: scripts/delivery-record-verify.sh --strict
```

## The record format

```yaml
---
predicate_type: https://kanopi.github.io/delivery-record/spec/v1
activity_type: code
subject: {kind: pr, title: "Add breadcrumb layout", ref: "456", sha: "abc123"}
assisted_by: {models: ["claude-fable-5"]}
checks:
  standards: {phpcs: pass}
  tests: {unit: pass}
  audits: {a11y: pass, performance: n/a}
  review: {qa: pass}
sign_off:
  produced_by: "@agent-session"
  reviewed_by: "@jimbirch"
---
n/a: no performance-relevant changes in this PR.

## What the human verified
...
```

The full field reference, per-activity checks tables, and versioning policy
live in [`spec/v1/README.md`](spec/v1/README.md) and
[`spec/VERSIONING.md`](spec/VERSIONING.md).

## Development

```bash
./scripts/validate-frontmatter.sh   # frontmatter validation
bats tests/                         # full test suite
node scripts/run-evals.js --min-rank1 75   # skill-routing evals
./scripts/check-codex-parity.sh     # Codex artifact parity
```

## Provenance

Extracted from [kanopi/cms-cultivator](https://github.com/kanopi/cms-cultivator)
— see [MIGRATION.md](MIGRATION.md) for what changed, including the legacy
`predicate_type` alias that keeps pre-split records validating.

## License

[MIT](LICENSE.md) © Kanopi Studios
