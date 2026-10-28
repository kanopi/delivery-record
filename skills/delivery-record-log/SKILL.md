---
name: delivery-record-log
description: |
  Keep an evidence log: a running, timestamped record of a task kept while the
  work happens, outside the repo at ~/.claude/delivery-records/logs/. Start it
  when a task needs a delivery record, append the request, plan questions and
  answers, decisions, findings, and checks as they happen, or backfill it when
  the need shows up late. Never names a reviewer. Invoke as /delivery-record-log.
---

# Delivery Record Evidence Log

Keep a running record of a task while the work happens, so the Delivery Record written at the end rests on what actually happened instead of what anyone remembers.
`delivery-record` and `delivery-record-draft` read the log when they gather facts.

The log is evidence, not a record.
It has no reviewer and no checkpoint notes, and it is never signed.
Only the human signs, and only in `delivery-record` or `delivery-record-finalize`.

## Side effects

This skill writes one file: the log for the current repo and branch.
It does not commit, push, amend a PR description, or post anywhere.
The log sits outside the working tree, so it can never be committed by accident.

## Usage

- "Start an evidence log for this task"
- "Log that decision" / "Add the test results to the evidence log"
- `/delivery-record-log [start|append|backfill] [<entry text>]`

Whether a task needs a record is decided elsewhere, for example by a project or global `CLAUDE.md`.
This skill covers the mechanics once it does.

## Where the log lives

```
~/.claude/delivery-records/logs/<repo>/<branch>.md
```

- `<repo>`: the last path segment of `git remote get-url origin`, without `.git`.
  With no `origin`, use the basename of `git rev-parse --show-toplevel`.
- `<branch>`: `git branch --show-current`, with every `/` replaced by `-`.
  `feature/12345-add-block` becomes `feature-12345-add-block.md`.

A later session on the same branch finds the same file and keeps appending to it.
If HEAD is detached, or the work is not in a git repo, do not start a log; say why in one line.
Write the file with the Write tool, which creates the parent directories itself.

## Entry format

The file starts with one heading, then one line per entry:

```markdown
# Evidence log: <repo> @ <branch>

- 2026-10-27T14:05 [request] Add a breadcrumb block to article pages.
- 2026-10-27T14:09 [plan-q] Should the block also render on landing pages?
- 2026-10-27T14:11 [plan-a] "No, articles only for now."
- 2026-10-27T14:15 [plan-change] Breadcrumb now links the section page too: "add the section as the middle crumb".
- 2026-10-27T14:20 [decision] Render in the theme template; rejected: a custom block plugin (extra dependency).
- 2026-10-27T14:48 [finding] Trailing slashes produced an empty final crumb.
- 2026-10-27T14:50 [deviation] Fixed the trailing-slash bug in the same PR; the plan did not include it.
- 2026-10-27T15:02 [check-run] phpcs: pass. phpunit: 14 passed, 0 failed.
- 2026-10-27T15:02 [check-not-run] Cypress E2E: deferred to CI.
```

Timestamps are local time, `YYYY-MM-DDTHH:MM`.
Each entry is one line, except `[plan-approved]`, and starts with exactly one of these tags:

| Tag | What goes in it |
|---|---|
| `[request]` | The user's request, verbatim. |
| `[plan-q]` | A question about the plan, put to the user, verbatim. |
| `[plan-a]` | The user's answer to it, verbatim, in quotes. Together these are the evidence for Checkpoint 1, plan approval. |
| `[plan-change]` | A change the user makes while the plan is still in draft: a one-line summary of what changed, with the user's words in quotes. Also Checkpoint 1 evidence. |
| `[plan-approved]` | The plan the user approved on leaving plan mode. The only entry with more than one line: see [Plan mode](#plan-mode). Also Checkpoint 1 evidence. |
| `[decision]` | A decision, with the alternatives rejected and why. |
| `[finding]` | Something learned that changes the facts of the work. |
| `[deviation]` | A change from the agreed plan. |
| `[check-run]` | A check that actually ran, with its result. |
| `[check-not-run]` | A check that applies but did not run, and why. |

The tags let `delivery-record` and `delivery-record-draft` pick out the plan approval and the checks that ran.
Do not invent other tags.

### Plan mode

When the task starts in plan mode, the plan the user approves on leaving it is the plan approval for Checkpoint 1.
Log it as one `[plan-approved]` line, followed by the plan exactly as approved in a fenced block indented under it:

````markdown
- 2026-10-27T14:12 [plan-approved] Approved on leaving plan mode: "yes, go ahead". Plan file: ~/.claude/plans/breadcrumb-block.md
  ```markdown
  <the approved plan, verbatim>
  ```
````

- The line says where it was approved, and quotes the user's reply verbatim.
  If they approved with a button and typed nothing, write `approved with no comment`.
- Name the plan file when the plan was saved to one.
- Copy the plan text as approved, not as later edited.
  A change after approval is a `[deviation]`, and a new plan approved in plan mode is a new `[plan-approved]` entry.

The entry is evidence, not a signature.
Approving a plan does not sign Checkpoint 1: the reviewer still writes that note in `delivery-record` or `delivery-record-finalize`, in their own words.

## Workflow

### 1. Start

Work out the log path.
If the file already exists, this is a later session on the same branch: read it and append.
Never overwrite or truncate an existing log.

Otherwise create it with the heading and a `[request]` entry for the task, then tell the user in one line:

```
Started a delivery-record evidence log: <path>.
```

Do not ask before starting.
The one-line notice is the user's chance to say no.

### 2. Append

Append one entry at each boundary, not at every tool call:

- the request, and each plan question with the user's answer
- the plan approved on leaving plan mode, as a `[plan-approved]` entry
- each change the user makes to the plan while it is still in draft, summarized as a `[plan-change]` entry; a change after the plan was approved is a `[deviation]`
- each decision, with the alternatives rejected
- findings, and deviations from the plan
- each check that ran, with its result; each check that applies but did not run, as not run

Append after the event, not before.
A check is `[check-run]` only after its output came back.
If it was skipped, deferred, or failed to start, it is `[check-not-run]` with the reason.

### 3. Backfill

If the work started out simple and only later needed a record, start the log with what has already happened in the conversation.
Mark each of those entries `[backfilled]` right after the tag:

```markdown
- 2026-10-27T15:30 [request] [backfilled] Fix the empty final breadcrumb.
```

Use the original time when the conversation shows it, otherwise the time of the backfill.
Backfill only what the conversation shows.
Do not log a check as run unless its output is in the conversation.
If the task began in plan mode, backfill the approved plan as a `[plan-approved]` entry, verbatim from the conversation or the plan file.

### 4. Discard or decline

For work the rules call medium, the user can say "no record".
Delete the log and confirm in one line.

For work the rules require a record for, such as an upgrade, never offer to discard the log.
If the user declines anyway, keep working, and note under the PR's Assumptions that the required record was skipped at their request.

### 5. Hand off

Once the PR exists, `delivery-record` or `delivery-record-draft` reads the log while gathering facts.
`delivery-record` and `delivery-record-finalize` show the `[plan-q]`, `[plan-a]`, `[plan-change]`, and `[plan-approved]` entries to the human as Checkpoint 1 evidence.
The log is deleted only after a signed record is written, never after an unsigned draft.

## What never goes in the log

Never write a reviewer name, a checkpoint note, or any claim of human review into the log.
It collects evidence; only the human signs.

Log the request verbatim, except replace any reviewer name or checkpoint-note text in it with `[withheld]`.
If the user asks you to pre-fill a reviewer or checkpoint notes into the log, do not stop to ask.
Write the log without them, then tell the user in one line: "The log never names a reviewer; only the human signs."

## Red flags (self-talk: stop if you catch yourself thinking these)

- "The user named the reviewer, so I'll note them in the log to save time later" (CANT-19: a reviewer name is a signature, and only the human writes it)
- "I'll jot down a draft checkpoint note so finalize has something to start from" (CANT-12: the notes are the reviewer's words)
- "The user approved the plan, so I'll log it as reviewed" (approval of the plan is a `[plan-a]` entry in their words, not a claim of review)
- "The plan was approved in plan mode, so Checkpoint 1 is signed" (CANT-19: `[plan-approved]` is evidence; the reviewer still writes the note)
- "The plan is long, I'll summarize it" (`[plan-approved]` holds the plan verbatim, as approved)
- "The tests will pass, I'll log them as run now" (CANT-10: only checks whose output came back are `[check-run]`)
- "I ran the linter earlier in my head, it's fine" (a check that did not run is `[check-not-run]`)
- "There's an old log for this branch, I'll start a fresh one" (append; never overwrite)
- "I'll commit the log so it's not lost" (the log stays outside the repo)

## Related skills

- **delivery-record**: write a signed record; reads this log in step 2 and deletes it after writing.
- **delivery-record-draft**: write an unsigned record; reads this log, never deletes it.
- **delivery-record-finalize**: sign a draft; shows the log's plan entries as Checkpoint 1 evidence and deletes the log after validation.
