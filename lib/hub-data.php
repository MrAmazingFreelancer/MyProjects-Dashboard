<?php

/**
 * Formats a filesystem modification timestamp for dashboard display.
 */
function formatHubModifiedTime(int $timestamp): string
{
    return date('Y-m-d H:i:s', $timestamp);
}

/**
 * @return array{directories: array<int, array{name: string, modified: string}>, files: array<int, array{name: string, modified: string}>}
 */
function collectHubEntries(string $baseDir, array $skipNames): array
{
    $entries = scandir($baseDir);
    $directories = [];
    $files = [];

    if ($entries === false) {
        return [
            'directories' => $directories,
            'files' => $files,
        ];
    }

    foreach ($entries as $entry) {
        if (in_array($entry, $skipNames, true)) {
            continue;
        }

        $path = $baseDir . DIRECTORY_SEPARATOR . $entry;
        if (is_dir($path)) {
            $directories[] = [
                'name' => $entry,
                'modified' => formatHubModifiedTime((int) filemtime($path)),
            ];
            continue;
        }

        if (is_file($path)) {
            $files[] = [
                'name' => $entry,
                'modified' => formatHubModifiedTime((int) filemtime($path)),
            ];
        }
    }

    usort($directories, static function (array $a, array $b): int {
        return strnatcasecmp($a['name'], $b['name']);
    });

    usort($files, static function (array $a, array $b): int {
        return strnatcasecmp($a['name'], $b['name']);
    });

    return [
        'directories' => $directories,
        'files' => $files,
    ];
}

/**
 * @param array<int, array{name: string, modified: string}> $directories
 * @param array<int, string> $favoriteDirs
 * @return array<int, array{name: string, modified: string}>
 */
function collectFavoriteDirectories(array $directories, array $favoriteDirs): array
{
    $favorites = [];
    foreach ($favoriteDirs as $favoriteDir) {
        foreach ($directories as $directory) {
            if ($directory['name'] === $favoriteDir) {
                $favorites[] = $directory;
                break;
            }
        }
    }

    return $favorites;
}
