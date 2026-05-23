<?php
$entries = scandir(__DIR__);
$projects = [];

if ($entries !== false) {
	foreach ($entries as $entry) {
		if ($entry === '.' || $entry === '..' || $entry === 'index.php') {
			continue;
		}
		$path = __DIR__ . DIRECTORY_SEPARATOR . $entry;
		if (is_dir($path)) {
			$projects[] = [
				'name'     => $entry,
				'modified' => date('Y-m-d H:i:s', (int) filemtime($path)),
			];
		}
	}
}

usort($projects, static function (array $a, array $b): int {
	return strnatcasecmp($a['name'], $b['name']);
});
?>
<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Shared Projects</title>
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
			padding: 20px 24px 24px;
		}

		.search-wrap {
			margin-bottom: 16px;
		}

		.search {
			width: 100%;
			padding: 10px 12px;
			border: 1px solid #bfdbfe;
			border-radius: 10px;
			font-size: 0.95rem;
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

		.item:hover {
			background: #eff6ff;
			border-color: #bfdbfe;
		}

		.empty {
			margin: 0;
			color: var(--muted);
			font-size: 0.92rem;
		}

		.meta {
			display: block;
			margin-top: 5px;
			font-weight: 500;
			color: #64748b;
			font-size: 0.84rem;
		}
	</style>
	<link rel="stylesheet" href="/assets/theme.css">
</head>
<body data-page="projects">
	<main class="wrap">
		<header class="head">
			<h1>Shared Projects</h1>
			<p class="sub">All projects in D:\Projects — accessible at http://localhost/projects/</p>
			<div class="quick">
				<a class="pill" href="/">&#8592; Back to Hub</a>
				<a class="pill" href="/_dashboard/">Open Dashboard</a>
			</div>
		</header>

		<div class="content">
			<div class="search-wrap">
				<input id="proj-search" class="search" type="search" placeholder="Search projects...">
			</div>

			<section>
				<h2>Projects (<?= count($projects) ?>)</h2>
				<?php if (count($projects) > 0): ?>
				<div class="list">
					<?php foreach ($projects as $project): ?>
					<a class="item" data-name="<?= htmlspecialchars(strtolower($project['name']), ENT_QUOTES, 'UTF-8') ?>" href="/projects/<?= rawurlencode($project['name']) ?>/">
						<?= htmlspecialchars($project['name'], ENT_QUOTES, 'UTF-8') ?>/
						<span class="meta">Modified: <?= htmlspecialchars($project['modified'], ENT_QUOTES, 'UTF-8') ?></span>
					</a>
					<?php endforeach; ?>
				</div>
				<?php else: ?>
				<p class="empty">No projects found. Run <code>.\scripts\new-project.ps1 -Name my-project</code> from D:\xampp\htdocs to create one.</p>
				<?php endif; ?>
			</section>
		</div>
	</main>
	<script src="/assets/theme.js"></script>
	<script>
		(function () {
			const input = document.getElementById('proj-search');
			if (!input) return;
			const items = Array.from(document.querySelectorAll('.item[data-name]'));
			input.addEventListener('input', function () {
				const q = input.value.trim().toLowerCase();
				for (const item of items) {
					item.style.display = (item.getAttribute('data-name') || '').includes(q) ? '' : 'none';
				}
			});
		})();
	</script>
</body>
</html>
