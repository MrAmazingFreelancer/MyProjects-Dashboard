<?php

/**
 * @param array<int, string> $extensions
 * @param callable(string): bool|null $extensionLoaded Optional dependency-injected extension checker for tests.
 * @return array<string, bool>
 */
function buildExtensionChecks(array $extensions, ?callable $extensionLoaded = null): array
{
    $extensionLoaded = $extensionLoaded ?? 'extension_loaded';
    $checks = [];

    foreach ($extensions as $extension) {
        $checks[$extension] = (bool) $extensionLoaded($extension);
    }

    return $checks;
}

/**
 * @param array<string, string> $paths
 * @param callable(string): bool|null $isDir Optional dependency-injected directory checker for tests.
 * @param callable(string): bool|null $isWritable Optional dependency-injected writable checker for tests.
 * @return array<string, array{path: string, exists: bool, writable: bool}>
 */
function buildPathChecks(array $paths, ?callable $isDir = null, ?callable $isWritable = null): array
{
    $isDir = $isDir ?? 'is_dir';
    $isWritable = $isWritable ?? 'is_writable';
    $pathChecks = [];

    foreach ($paths as $label => $path) {
        $exists = (bool) $isDir($path);
        $writable = $exists ? (bool) $isWritable($path) : false;
        $pathChecks[$label] = [
            'path' => $path,
            'exists' => $exists,
            'writable' => $writable,
        ];
    }

    return $pathChecks;
}

/**
 * @param callable(string): array<int, string>|false|null $scandirFn Optional dependency-injected directory lister for tests.
 * @param callable(string): bool|null $isDirFn Optional dependency-injected directory checker for tests.
 * @return array<int, string>
 */
function collectProjectsList(string $projectsRoot, ?callable $scandirFn = null, ?callable $isDirFn = null): array
{
    $scandirFn = $scandirFn ?? 'scandir';
    $isDirFn = $isDirFn ?? 'is_dir';
    $projects = [];

    if ($projectsRoot === '' || !$isDirFn($projectsRoot)) {
        return $projects;
    }

    $items = $scandirFn($projectsRoot);
    if (!is_array($items)) {
        return $projects;
    }

    foreach ($items as $item) {
        if ($item === '.' || $item === '..') {
            continue;
        }

        $itemPath = $projectsRoot . DIRECTORY_SEPARATOR . $item;
        if ($isDirFn($itemPath)) {
            $projects[] = $item;
        }
    }

    sort($projects, SORT_NATURAL | SORT_FLAG_CASE);

    return $projects;
}
