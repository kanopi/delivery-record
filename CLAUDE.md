# Claude Context for Delivery Record

Claude Code plugin providing the Delivery Record spec plus two Agent Skills:
`delivery-record` (write a record) and `delivery-record-verify` (validate
records). Public repo, MIT licensed. Extracted from kanopi/cms-cultivator —
see MIGRATION.md.

## Invariants

- **The spec is versioned and append-only.** `spec/v1/` never changes
  incompatibly; breaking changes mean a new `spec/v2/` directory (see
  `spec/VERSIONING.md`). `schema.json`'s per-activity `if/then` branches and
  `spec/v1/checks/*.json` must stay in sync — bats enforces it.
- **Canonical predicate_type URI:**
  `https://kanopi.github.io/delivery-record/spec/v1`. The legacy
  `https://kanopi.github.io/cms-cultivator/spec/delivery-record/v1` form is a
  permanent alias (schema pattern + verifier regex + a bats test). Never
  remove the alias — records in client repos depend on it.
- **The human checkpoint is non-negotiable.** The `delivery-record` skill
  refuses to write without a named reviewer and two non-generic checkpoint
  notes. Do not weaken this under any pressure — it is the entire point of
  the artifact.
- **Every activity type has three synchronized artifacts:** a schema branch +
  `checks/<type>.json`, an example in `spec/v1/examples/`, and a body
  template in `skills/delivery-record/templates/`. Adding a type means all
  three plus a bats expectation.
- No hardcoded counts in docs or tests — parity checks only (activity types
  derive from the schema enum).

## Cross-repo references

`pr-create`, `commit-message-generator`, and `teamwork-integrator` mentioned
in skill prose live in other Kanopi plugins (cms-cultivator, pm-skills).
These are soft prose references only — never add a hard `Task()` dependency
across repos.

## Verification quartet (run before any commit)

```bash
./scripts/validate-frontmatter.sh
bats tests/
node scripts/run-evals.js --min-rank1 75
./scripts/check-codex-parity.sh
```

The bats suite includes the behavioral cases' static `--check` — free, no
API calls.

## Behavioral evals

`scripts/run-behavioral-evals.sh` (synced from kanopi/skills-plugin-template)
runs the side-effect skill headlessly in disposable fixture repos and grades
the trace against `evals/cases/*.json` — the refusal gates (no reviewer, bare
"LGTM", user override) and the valid-record happy path, which is post-checked
with `delivery_record_verify.py --strict`. Runs cost real tokens (haiku
default, per-case tally printed) and never run per-push. Schema:
`evals/cases/README.md`.

```bash
./scripts/run-behavioral-evals.sh --check        # static, free
./scripts/run-behavioral-evals.sh --case <name>  # one case
./scripts/run-behavioral-evals.sh                # full suite
```

When changing `delivery-record` or `delivery-record-verify` behavior
(refusal rules, record paths, template shapes), keep the behavioral cases
passing — a failing case is a skill bug: fix the skill, not the test, and
changelog it.
