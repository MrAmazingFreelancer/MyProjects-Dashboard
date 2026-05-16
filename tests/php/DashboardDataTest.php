<?php

declare(strict_types=1);

require_once dirname(__DIR__, 2) . '/_dashboard/lib/dashboard-data.php';

testCase('buildExtensionChecks maps extension status', function (): void {
    $checks = buildExtensionChecks(['a', 'b'], static function (string $extension): bool {
        return $extension === 'a';
    });

    assertSameValue(['a' => true, 'b' => false], $checks);
});

testCase('buildPathChecks marks writable only when path exists', function (): void {
    $checks = buildPathChecks(
        ['good' => '/ok', 'missing' => '/missing'],
        static function (string $path): bool {
            return $path === '/ok';
        },
        static function (string $path): bool {
            return $path === '/ok';
        }
    );

    assertTrue($checks['good']['exists']);
    assertTrue($checks['good']['writable']);
    assertSameValue(false, $checks['missing']['exists']);
    assertSameValue(false, $checks['missing']['writable']);
});

testCase('collectProjectsList filters non-directories and sorts naturally', function (): void {
    $projects = collectProjectsList(
        '/projects',
        static function (string $path): array {
            if ($path === '/projects') {
                return ['.', '..', 'project10', 'project2', 'notes.txt'];
            }

            return [];
        },
        static function (string $path): bool {
            return in_array($path, ['/projects', '/projects/project10', '/projects/project2'], true);
        }
    );

    assertSameValue(['project2', 'project10'], $projects);
});
