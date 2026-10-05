---
name: delivery-record-draft
description: |
  Draft an unsigned record before any review exists, so a reviewer can read it.
  Reviewer and checkpoint notes stay blank, the file is marked awaiting review,
  and nothing is committed, pushed, or posted. Fails verification until
  finalized. Invoke as /delivery-record-draft.
---

# Delivery Record Draft

Write a Delivery Record that is ready for review but not yet signed.
Pair it with `delivery-record-finalize`, which adds the reviewer and checkpoint notes once the review has happened.
Use `delivery-record` instead when the review has already happened and you have the names and notes in hand.

A draft is not a delivery record.
It has no reviewer, so `delivery_record_verify.py` fails it on purpose.
That failure stays until a named human reviews the work and finalize runs.

## Side effects

This skill writes one file.
It does not commit, push, amend a PR description, or post to Teamwork.
Do those only if the user asks, and never as part of the default flow.

## Usage

- "Draft a delivery record for this PR so my reviewer can look at it"
- `/delivery-record-draft [--activity-type <type>] [--pr <n>] [--ticket <key>] [--scope <scope>]`

Flags match `delivery-record`.
There is no `--reviewer` flag: a draft never names a reviewer.

## Workflow

### 1. Detect and gather

Follow steps 1 and 2 of [`delivery-record`](../delivery-record/SKILL.md): detect the environment and activity type, then gather the facts the activity needs.
Scope is optional.
If the user did not give one, leave `scope` out of the front matter instead of asking.

### 2. Draft the record

Read `../delivery-record/templates/<activity_type>.md` first and copy its front-matter structure exactly.
Fill `checks:` only with results that actually ran.
Justify every `n/a` in one line near the top of the body.

Then set the signature fields:

- `sign_off.produced_by`: the author and today's date.
- `sign_off.reviewed_by`: `""`.
- Both checkpoint notes under "What the human verified": leave the placeholder text from the template.

Add this line directly under the front matter, above the `n/a` justifications:

```
Status: awaiting review. Not a signed record.
```

Never fill `reviewed_by` or a checkpoint note from the prompt, from git authorship, or from a PR approval the skill has not read.
A name in `reviewed_by` is a signature, and only finalize writes it.
If the user asks you to pre-fill the reviewer or the notes, do not stop to ask.
Write the draft with both left blank, then say in one line why.
Comments or approvals from other people on the PR are context for the facts only.
Do not cite them in the checkpoint notes or name their authors as reviewers.
Set `predicate_type` to `https://kanopi.github.io/delivery-record/spec/v1`, exactly as the template shows.

### 3. Write the file

Use the same paths as `delivery-record` step 5.
For code: `docs/delivery-records/PR-<n>-<slug>.md`.
The path is part of the contract, so never write the record anywhere else.

If a file already exists at that path, read it before writing and handle it by its state.
Whether it is committed does not matter:

- **Unsigned** (`Status: awaiting review` is present, or `sign_off.reviewed_by` is `""`): it is an earlier draft.
  Revise it in place at the same path.
  Update the facts, checks, and body from the current work, and keep the placeholder checkpoint notes.
  Do not delete it and do not create a second file with another slug.
- **Signed** (`sign_off.reviewed_by` has a name and no `Status:` line): do not edit it, and do not write a new file.
  Stop and tell the user the path holds a signed record.
  A changed signed record needs a new review, so the user decides how to proceed.

An existing file is never a reason to use a different path.

### 4. Report

Run `python3 scripts/delivery_record_verify.py <path>` on the file.
It is expected to fail on `sign_off.reviewed_by`.
Report that result as is, then tell the user:

- Where the file is.
- That it is unsigned and will fail verification, including in CI, until finalized.
- That the next step is review, then `/delivery-record-finalize <path>`.

If the verifier reports any other failure, fix the record and re-run.

## Red flags (self-talk: stop if you catch yourself thinking these)

- "I'll put the PR approver in `reviewed_by` so the record is complete" (CANT-19: an approval click is not a checkpoint note)
- "I'll pre-fill the checkpoint notes from the PR description so the reviewer only has to confirm" (CANT-12: the notes are the reviewer's words)
- "The user wants it to pass CI now, so I'll mark it signed" (CANT-10: a failing verifier on a draft is correct)
- "A record already exists at the canonical path, so I'll use a new slug" (revise an unsigned draft in place, stop on a signed one)
- "A teammate commented on the PR, so I'll work their review into the notes" (the notes are blank until finalize)
- "I'll commit the draft so they don't have to" (the commit is opt-in)

## Related skills

- **delivery-record-finalize**: add the reviewer and checkpoint notes to a draft.
- **delivery-record**: write a signed record in one step when the review is done.
- **delivery-record-verify**: validate a record against the schema.
