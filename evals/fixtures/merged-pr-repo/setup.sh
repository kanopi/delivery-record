#!/usr/bin/env bash
# Fixture: repo with a merged-PR story baked into git log (PR #12).
set -euo pipefail
rm -f setup.sh
git init -q -b main
git config user.email eval@kanopi.com
git config user.name "Behavioral Eval"
git add -A
git commit -qm "feat: initial site scaffold"

git checkout -qb fix/breadcrumb-links
cat > src/breadcrumb.php <<'PHP'
<?php
/**
 * Breadcrumb builder used by the behavioral eval fixture.
 */

function fixture_build_breadcrumb( string $path ): array {
	$parts = array_filter( explode( '/', rtrim( $path, '/' ) ) );
	// Trailing slashes produced an empty final crumb on article pages.
	return array_values( array_filter( $parts, 'strlen' ) );
}
PHP
git add src/breadcrumb.php
git commit -qm "fix(breadcrumb): correct trailing-slash handling on article pages"

git checkout -q main
git merge -q --no-ff fix/breadcrumb-links -m "Merge pull request #12 from kanopi/fix/breadcrumb-links

fix: correct breadcrumb links on article pages"
