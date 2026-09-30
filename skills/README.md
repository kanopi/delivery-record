# Skills

Overview of the Agent Skills in this plugin. Keep this list in parity with
the `skills/` directory — `tests/test-plugin.bats` asserts that the number
of `### N.` entries below equals the number of skill directories. Append
the next number rather than inserting mid-list.

### 1. delivery-record

Generate a schema-typed, human-signed Delivery Record for a significant
AI-assisted output. Refuses to write without a named reviewer and both
checkpoint notes. Writes to `docs/delivery-records/` (code) or Drive
(non-code) and indexes the record in the project's Teamwork "Delivery
Records" notebook.

### 2. delivery-record-verify

Validate Delivery Record files against the bundled spec: resolves the
schema version from `predicate_type`, enforces required fields and the
per-activity checks policy, and applies the threshold rule (fail needs a
waiver, n/a needs a justification) as soft warnings or hard failures with
`--strict`.

### 3. delivery-record-draft

Write an unsigned Delivery Record so a reviewer can read it. Leaves
`reviewed_by` and both checkpoint notes blank, marks the file as awaiting
review, and does not commit, push, or post to Teamwork. The record fails
verification until finalized.

### 4. delivery-record-finalize

Sign a drafted Delivery Record after review. Refuses to write without a
named reviewer and both checkpoint notes, edits only the sign-off and
checkpoint sections, and validates the result with `--strict`.
