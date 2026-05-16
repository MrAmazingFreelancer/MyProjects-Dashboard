<?php

declare(strict_types=1);

require_once dirname(__DIR__, 2) . '/lib/hub-data.php';

function createHubFixture(): string
{
    $basePath = sys_get_temp_dir() . DIRECTORY_SEPARATOR . 'hub-test-' . bin2hex(random_bytes(6));
    mkdir($basePath, 0777, true);

    mkdir($basePath . DIRECTORY_SEPARATOR . 'Bravo');
    mkdir($basePath . DIRECTORY_SEPARATOR . 'alpha');
    file_put_contents($basePath . DIRECTORY_SEPARATOR . 'zeta.txt', 'z');
    file_put_contents($basePath . DIRECTORY_SEPARATOR . 'Beta.txt', 'b');
    file_put_contents($basePath . DIRECTORY_SEPARATOR . '.gitignore', 'skip');

    touch($basePath . DIRECTORY_SEPARATOR . 'Bravo', 1700000000);
    touch($basePath . DIRECTORY_SEPARATOR . 'alpha', 1700000100);
    touch($basePath . DIRECTORY_SEPARATOR . 'zeta.txt', 1700000200);
    touch($basePath . DIRECTORY_SEPARATOR . 'Beta.txt', 1700000300);

    return $basePath;
}

function removeTree(string $path): void
{
    if (!is_dir($path)) {
        return;
    }

    $items = scandir($path);
    if ($items === false) {
        return;
    }

    foreach ($items as $item) {
        if ($item === '.' || $item === '..') {
            continue;
        }

        $itemPath = $path . DIRECTORY_SEPARATOR . $item;
        if (is_dir($itemPath)) {
            removeTree($itemPath);
            continue;
        }

        unlink($itemPath);
    }

    rmdir($path);
}

testCase('collectHubEntries sorts and filters files and directories', function (): void {
    $fixture = createHubFixture();
    try {
        $result = collectHubEntries($fixture, ['.', '..', '.gitignore']);
        $directoriesByName = array_column($result['directories'], null, 'name');
        $filesByName = array_column($result['files'], null, 'name');

        assertStrictEqual(['alpha', 'Bravo'], array_column($result['directories'], 'name'));
        assertStrictEqual(['Beta.txt', 'zeta.txt'], array_column($result['files'], 'name'));
        assertStrictEqual(formatHubModifiedTime(1700000000), $directoriesByName['Bravo']['modified']);
        assertStrictEqual(formatHubModifiedTime(1700000200), $filesByName['zeta.txt']['modified']);
    } finally {
        removeTree($fixture);
    }
});

testCase('collectFavoriteDirectories keeps favorite order and skips missing', function (): void {
    $directories = [
        ['name' => 'alpha', 'modified' => 'x'],
        ['name' => 'projects', 'modified' => 'y'],
        ['name' => '_dashboard', 'modified' => 'z'],
    ];

    $favorites = collectFavoriteDirectories($directories, ['_dashboard', 'missing', 'projects']);
    assertStrictEqual(['_dashboard', 'projects'], array_column($favorites, 'name'));
});
