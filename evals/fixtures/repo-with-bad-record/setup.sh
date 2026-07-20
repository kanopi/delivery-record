#!/usr/bin/env bash
# Fixture: repo containing a delivery record whose `n/a` check has no
# justification in the first five body lines (a --strict failure).
set -euo pipefail
rm -f setup.sh
git init -q -b main
git config user.email eval@kanopi.com
git config user.name "Behavioral Eval"
git add -A
git commit -qm "docs: add delivery record for PR #7"
