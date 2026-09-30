---
predicate_type: https://kanopi.github.io/delivery-record/spec/v1
activity_type: code
subject:
  kind: pr
  ref: "kanopi/fixture#12"
  sha: abc1234
  title: "fix: correct breadcrumb links on article pages"
scope: fix
assisted_by:
  models: [claude-haiku-4-5]
  skills: [pr-create]
checks:
  standards: { phpcs: pass, phpstan: pass }
  tests: { unit: pass, ci_run: "https://example.com/ci/123" }
  audits: { a11y: n/a, performance: n/a, security: pass }
  review: { code_review: "pending", qa: pass }
sign_off:
  produced_by: "@author 2026-09-30"
  reviewed_by: ""
---

Status: awaiting review. Not a signed record.

n/a: a11y (breadcrumb markup unchanged), performance (no query or asset changes).

## What changed

Trailing-slash handling in the breadcrumb builder on article pages.

## What the AI produced

The fix in `src/breadcrumb.php`.

## What the human verified

Checkpoint 1 (plan approval): <brief note>.
Checkpoint 2 (final code approval): <what the reviewer actually looked at beyond CI and the linters>.
