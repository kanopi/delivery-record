<?php
/**
 * Breadcrumb builder used by the behavioral eval fixture.
 */

function fixture_build_breadcrumb( string $path ): array {
	$parts = array_filter( explode( '/', rtrim( $path, '/' ) ) );
	return array_values( $parts );
}
