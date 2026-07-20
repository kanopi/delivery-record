---
predicate_type: https://kanopi.github.io/delivery-record/spec/v1
activity_type: code
subject:
  kind: pr
  ref: "kanopi/eval-fixture#7"
  sha: abc1234
  title: "feat: add example widget"
scope: feature
assisted_by:
  models: [claude-haiku-4-5]
  skills: [pr-create]
checks:
  standards: { phpcs: pass, phpstan: n/a }
  tests:     { unit: pass, ci_run: "https://example.com/ci/456" }
  audits:    { a11y: pass, performance: pass, security: pass }
  review:    { code_review: "approved by @thejimbirch", qa: pass }
sign_off:
  produced_by: "Claude/claude-haiku-4-5, session driven by @thejimbirch 2026-07-10"
  reviewed_by: "@thejimbirch 2026-07-10"
---

## What changed

Added the example widget with its render callback and settings panel.

## What the AI produced

The widget class, render callback, and settings registration.

## What the human verified

Checkpoint 1 (plan approval): approved the widget plan and naming.
Checkpoint 2 (final code approval): reviewed the diff and tested the widget
render in the editor and on the front end.

## Issues found and resolved

- None.

## Deferred or known risks

- None.
