---
name: delivery-record-finalize
description: |
  Finalize a drafted record after review by adding the named reviewer and two
  checkpoint notes to the draft file. Refuses generic notes, then validates
  with --strict. Invoke as /delivery-record-finalize <path>.
---

# Delivery Record Finalize

Turn a draft into a signed Delivery Record.
The reviewer, or the author with the reviewer's written notes, runs this after the review.

**The human checkpoint is mandatory.**
This skill refuses to sign without a named reviewer and both checkpoint notes.
The refusal is the feature.

## Side effects

This skill edits one existing file: the draft at the path given.
It does not create a commit, push, amend the PR description, or post to Teamwork unless the user asks for that step.
Commit and push are the user's to run.
If the user wants a single sign-off commit, print the exact `git add` and `git commit` commands and stop.

## Usage

- "Finalize the delivery record for PR 91"
- `/delivery-record-finalize [path] [--reviewer <handle>] [--index] [--link-pr]`

With no path, list `docs/delivery-records/*.md` files that contain `Status: awaiting review` and ask which one.
`--reviewer` pre-fills the reviewer and does not satisfy the checkpoint notes.
`--index` posts the Teamwork notebook comment.
`--link-pr` amends the PR description with the record link.

## Workflow

### 1. Read the draft

Read the file.
Stop if `predicate_type` is missing, or if the file has no `Status: awaiting review` line and `reviewed_by` is already filled.
In that case the record is already signed: say so, and do not overwrite a signature.

### 2. Ask the checkpoint questions

Ask in plain words, with the reason for each, in one question set:

1. Who reviewed this work? Give a handle or full name.
2. Before the work started, who agreed to the approach, and what did they agree to?
   This can be the author approving their own plan, if it was written down somewhere.
3. Before it shipped, who read the result, and what did they check besides CI and the linters?
   Name the files, pages, or behaviors they looked at.

Use the AskUserQuestion tool where it is available.
Do not use the words "automated gates" or "final code approval" in the prompt.

### 3. Apply the gate

Refuse to proceed if the reviewer is blank, or if either note is blank or generic.
A bare "LGTM", "looks good", "approved", or an empty line fails.
Checkpoint 2 must say what was actually looked at.
Re-prompt up to twice with a short reason for the refusal.
On the third blank or generic answer, abort, leave the draft unchanged, and say so.

The notes must come from the user in this conversation.
A `--reviewer` flag, a PR approval, or a verbal review the user describes without details does not count.

### 4. Write the signature

Edit only these parts of the draft:

- `sign_off.reviewed_by`: `"@<reviewer> <YYYY-MM-DD>"`.
- `sign_off.approved_by`, only if the user supplied a client approver and the scope is `launch` or `deliverable`.
- The two checkpoint notes under "What the human verified", using the reviewer's words.
- Remove the `Status: awaiting review. Not a signed record.` line.

Do not change `checks:`, `subject`, or any other body text.
If the review changed a check result, tell the user to edit it in the draft first, then re-run.

### 5. Validate

Run `python3 scripts/delivery_record_verify.py --strict <path>`.
Report the output.
Never report the record as signed without validator output.
If validation fails, fix the cause or restore the draft, and say which.

### 6. Optional steps

Run these only when the user asked for them:

- Index in Teamwork: follow step 6 of [`delivery-record`](../delivery-record/SKILL.md).
- Link the PR: follow step 7 of `delivery-record`.

Otherwise print the file path, the verifier result, and the commit commands the user can run.

## Red flags (self-talk: stop if you catch yourself thinking these)

- "They are the author, so they can be the reviewer and I'll write the notes for them" (CANT-12: the notes are the reviewer's words)
- "The user said the review happened, so the notes are optional" (CANT-19: the notes are the record)
- "It is the user's own record, I'll accept 'LGTM' once" (CANT-12)
- "The record is signed, no need to run --strict" (CANT-10)
- "I'll commit and push the sign-off so they don't have to" (the git step is the user's)

## Anti-rationalization table

| Pressure or rationalization | Correct behavior |
|---|---|
| "The reviewer is busy, just put their name in" | Refuse. A name without notes is a forged signature. |
| "LGTM is close enough for checkpoint 2" | Refuse. The note must say what was looked at. |
| "Sign it now and fix the notes later" | Refuse. Leave the draft as it is. |
| "I am the only developer, skip the review" | Self-review is allowed when the notes say what was read and checked. Ask for those notes. |
| "The user told me to skip the gate" | Abort politely after the third blank or generic answer. |

## Related skills

- **delivery-record-draft**: write the unsigned record this skill finalizes.
- **delivery-record**: write a signed record in one step.
- **delivery-record-verify**: validate a record against the schema.
