<?php
$entries = scandir(__DIR__);
$directories = [];
$files = [];

$skipNames = [
    '.',
    '..',
    '.git',
    '.github',
    '.gitignore',
    '.env.example',
    'index.php',
];

if ($entries !== false) {
    foreach ($entries as $entry) {
        if (in_array($entry, $skipNames, true)) {
            continue;
        }

        $path = __DIR__ . DIRECTORY_SEPARATOR . $entry;

        if (is_dir($path)) {
            $directories[] = [
                'name' => $entry,
                'modified' => date('Y-m-d H:i:s', (int) filemtime($path)),
            ];
            continue;
        }

        if (is_file($path)) {
            $files[] = [
                'name' => $entry,
                'modified' => date('Y-m-d H:i:s', (int) filemtime($path)),
                'size' => (int) filesize($path),
            ];
        }
    }
}

usort($directories, static function (array $a, array $b): int {
    return strnatcasecmp($a['name'], $b['name']);
});

usort($files, static function (array $a, array $b): int {
    return strnatcasecmp($a['name'], $b['name']);
});

function human_size(int $bytes): string
{
    if ($bytes < 1024) {
        return $bytes . ' B';
    }

    $units = ['KB', 'MB', 'GB'];
    $value = $bytes / 1024;

    foreach ($units as $unit) {
        if ($value < 1024 || $unit === 'GB') {
            return number_format($value, 1) . ' ' . $unit;
        }
        $value /= 1024;
    }

    return number_format($bytes / 1024, 1) . ' KB';
}
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Shared Projects</title>
    <link rel="stylesheet" href="/assets/theme.css">
    <style>
        :root {
            --bg: #f6faf8;
            --panel: #ffffff;
            --ink: #0f172a;
            --muted: #475569;
            --line: #d1d5db;
            --accent: #0369a1;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            min-height: 100vh;
            color: var(--ink);
            font-family: "Segoe UI", Tahoma, sans-serif;
            background:
                radial-gradient(circle at 8% 12%, #d9f99d 0, transparent 30%),
                radial-gradient(circle at 92% 8%, #bfdbfe 0, transparent 24%),
                linear-gradient(180deg, #f8fffa 0%, #eff6ff 100%);
            padding: 24px;
        }

        .wrap {
            width: min(1080px, 100%);
            margin: 0 auto;
            background: var(--panel);
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            box-shadow: 0 18px 42px rgba(15, 23, 42, 0.12);
            overflow: hidden;
            position: relative;
            z-index: 2;
        }

        .head {
            padding: 22px 24px;
            border-bottom: 1px solid var(--line);
            background: linear-gradient(120deg, #ecfeff, #f0fdf4);
        }

        h1 {
            margin: 0;
            font-size: clamp(1.3rem, 2.7vw, 1.9rem);
        }

        .sub {
            margin: 8px 0 0;
            color: var(--muted);
        }

        .quick {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 12px;
        }

        .pill {
            text-decoration: none;
            color: #0f172a;
            background: #dbeafe;
            border: 1px solid #bfdbfe;
            border-radius: 999px;
            padding: 7px 12px;
            font-weight: 700;
            font-size: 0.9rem;
        }

        .content {
            display: grid;
            gap: 14px;
            padding: 20px 24px 24px;
        }

        @media (min-width: 900px) {
            .content {
                grid-template-columns: 1fr 1fr;
            }
        }

        section {
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 14px;
        }

        h2 {
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 1rem;
            color: var(--accent);
        }

        .list {
            display: grid;
            gap: 8px;
        }

        .item {
            display: block;
            text-decoration: none;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 9px 11px;
            color: #1e293b;
            background: #f8fafc;
            font-weight: 600;
            word-break: break-word;
        }

        .meta {
            display: block;
            margin-top: 5px;
            font-weight: 500;
            color: #64748b;
            font-size: 0.84rem;
        }

        .empty {
            margin: 0;
            color: var(--muted);
            font-size: 0.92rem;
        }
    </style>
</head>
<body data-page="projects">
    <main class="wrap">
        <header class="head">
            <h1>Shared Projects</h1>
            <p class="sub">Central list for everything under /projects.</p>
            <div class="quick">
                <a class="pill" href="/">Back</a>
                <a class="pill" href="../">Parent Directory</a>
                <a class="pill" href="/index.php">Back to Hub</a>
                <a class="pill" href="/dashboard/">Open Dashboard</a>
            </div>
        </header>

        <div class="content">
            <section>
                <h2>Directories</h2>
                <?php if (count($directories) > 0): ?>
                <div class="list">
                    <?php foreach ($directories as $dir): ?>
                    <a class="item" href="<?= rawurlencode($dir['name']) ?>/">
                        <?= htmlspecialchars($dir['name'], ENT_QUOTES, 'UTF-8') ?>/
                        <span class="meta">Modified: <?= htmlspecialchars($dir['modified'], ENT_QUOTES, 'UTF-8') ?></span>
                    </a>
                    <?php endforeach; ?>
                </div>
                <?php else: ?>
                <p class="empty">No directories found.</p>
                <?php endif; ?>
            </section>

            <section>
                <h2>Files</h2>
                <?php if (count($files) > 0): ?>
                <div class="list">
                    <?php foreach ($files as $file): ?>
                    <a class="item" href="<?= rawurlencode($file['name']) ?>">
                        <?= htmlspecialchars($file['name'], ENT_QUOTES, 'UTF-8') ?>
                        <span class="meta">Modified: <?= htmlspecialchars($file['modified'], ENT_QUOTES, 'UTF-8') ?> | Size: <?= htmlspecialchars(human_size($file['size']), ENT_QUOTES, 'UTF-8') ?></span>
                    </a>
                    <?php endforeach; ?>
                </div>
                <?php else: ?>
                <p class="empty">No top-level files found.</p>
                <?php endif; ?>
            </section>
        </div>
    </main>
    <script src="/assets/theme.js"></script>
</body>
</html>
