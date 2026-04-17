<?php
$entries = scandir(__DIR__);
$directories = [];
$files = [];

$skipNames = [
	'.',
	'..',
	'.git',
	'.gitignore',
];

if ($entries !== false) {
	foreach ($entries as $entry) {
		if (in_array($entry, $skipNames, true)) {
			continue;
		}

		$path = __DIR__ . DIRECTORY_SEPARATOR . $entry;
		if (is_dir($path)) {
			$directories[] = $entry;
			continue;
		}

		if (is_file($path)) {
			$files[] = $entry;
		}
	}
}

sort($directories, SORT_NATURAL | SORT_FLAG_CASE);
sort($files, SORT_NATURAL | SORT_FLAG_CASE);
?>
<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>MyProjects Hub</title>
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

		.empty {
			margin: 0;
			color: var(--muted);
			font-size: 0.92rem;
		}

		.howto {
			grid-column: 1 / -1;
		}

		.code {
			margin: 10px 0 0;
			padding: 10px 12px;
			border-radius: 10px;
			background: #0f172a;
			color: #e2e8f0;
			font-family: Consolas, monospace;
			font-size: 0.9rem;
			overflow-x: auto;
		}
	</style>
</head>
<body>
	<main class="wrap">
		<header class="head">
			<h1>MyProjects Hub</h1>
			<p class="sub">Central homepage for everything inside htdocs</p>
			<div class="quick">
				<a class="pill" href="/_dashboard/">Open Dashboard</a>
				<a class="pill" href="/projects/">Open Shared Projects</a>
			</div>
		</header>

		<div class="content">
			<section>
				<h2>Directories</h2>
				<?php if (count($directories) > 0): ?>
				<div class="list">
					<?php foreach ($directories as $dir): ?>
					<a class="item" href="/<?= rawurlencode($dir) ?>/"><?= htmlspecialchars($dir, ENT_QUOTES, 'UTF-8') ?>/</a>
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
					<a class="item" href="/<?= rawurlencode($file) ?>"><?= htmlspecialchars($file, ENT_QUOTES, 'UTF-8') ?></a>
					<?php endforeach; ?>
				</div>
				<?php else: ?>
				<p class="empty">No top-level files found.</p>
				<?php endif; ?>
			</section>

			<section class="howto">
				<h2>Create New Project</h2>
				<p class="empty">Use your shared template generator script from PowerShell:</p>
				<div class="code">Set-Location D:\xampp\htdocs; .\scripts\new-project.ps1 -Name my-new-project</div>
				<p class="empty" style="margin-top:10px;">Then open: <a href="/projects/" style="color:#0369a1;font-weight:700;text-decoration:none;">/projects/</a></p>
			</section>
		</div>
	</main>
</body>
</html>
