<?php
$htdocsRoot = realpath(__DIR__ . DIRECTORY_SEPARATOR . '..');
$created = false;
$error = '';
$targetFile = '';
$location = trim((string)($_POST['location'] ?? 'projects'));
$createMissingDir = isset($_POST['create_missing_dir']) && $_POST['create_missing_dir'] === '1';
$uploadedOriginalName = '';

$locationOptions = [];
if ($htdocsRoot !== false && is_dir($htdocsRoot)) {
    $items = scandir($htdocsRoot);
    if ($items !== false) {
        foreach ($items as $item) {
            if ($item === '.' || $item === '..') {
                continue;
            }

            $candidate = $htdocsRoot . DIRECTORY_SEPARATOR . $item;
            if (is_dir($candidate)) {
                $locationOptions[] = $item;
            }
        }
    }
}
sort($locationOptions, SORT_NATURAL | SORT_FLAG_CASE);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if ($htdocsRoot === false || !is_dir($htdocsRoot)) {
        $error = 'htdocs directory was not found.';
    } else {
        $filename = trim((string)($_POST['filename'] ?? ''));
        $content = (string)($_POST['content'] ?? '');
        $hasUploadedFile = isset($_FILES['local_file']) && (int)($_FILES['local_file']['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_NO_FILE;

        if ($hasUploadedFile) {
            $uploadedOriginalName = basename((string)($_FILES['local_file']['name'] ?? ''));
            if ($filename === '') {
                $filename = $uploadedOriginalName;
            }
        }

        if ($location === '') {
            $error = 'Please enter a target folder.';
        } elseif (!preg_match('/^[A-Za-z0-9._\\\/-]+$/', $location)) {
            $error = 'Invalid folder path.';
        } elseif (strpos($location, '..') !== false) {
            $error = 'Parent folder segments are not allowed.';
        } elseif ($hasUploadedFile && (int)($_FILES['local_file']['error'] !== UPLOAD_ERR_OK)) {
            $error = 'Upload failed. Please try selecting the local file again.';
        } elseif ($filename === '') {
            $error = 'Please enter a file name.';
        } elseif (!preg_match('/^[A-Za-z0-9._-]+$/', $filename)) {
            $error = 'Invalid file name. Use letters, numbers, dot, underscore, or dash.';
        } else {
            $normalizedLocation = trim(str_replace(['/', '\\'], DIRECTORY_SEPARATOR, $location), DIRECTORY_SEPARATOR);
            $targetDir = $htdocsRoot . DIRECTORY_SEPARATOR . $normalizedLocation;
            $targetDirReal = realpath($targetDir);

            if (($targetDirReal === false || !is_dir($targetDirReal)) && $createMissingDir) {
                $createdDir = @mkdir($targetDir, 0775, true);
                if ($createdDir) {
                    $targetDirReal = realpath($targetDir);
                }
            }

            if ($targetDirReal === false || !is_dir($targetDirReal)) {
                $error = 'Target folder does not exist inside htdocs.';
            } elseif (strpos($targetDirReal, $htdocsRoot) !== 0) {
                $error = 'Target folder must be inside htdocs.';
            } else {
                $targetFile = $targetDirReal . DIRECTORY_SEPARATOR . $filename;

                if (file_exists($targetFile)) {
                    $error = 'A file with this name already exists.';
                } else {
                    if ($hasUploadedFile) {
                        $tmpPath = (string)($_FILES['local_file']['tmp_name'] ?? '');
                        if ($tmpPath === '' || !is_uploaded_file($tmpPath)) {
                            $error = 'Uploaded file is invalid.';
                        } else {
                            $moved = @move_uploaded_file($tmpPath, $targetFile);
                            if (!$moved) {
                                $error = 'Uploaded file could not be saved. Check folder permissions.';
                            } else {
                                $created = true;
                            }
                        }
                    } else {
                        $bytes = @file_put_contents($targetFile, $content);
                        if ($bytes === false) {
                            $error = 'File could not be created. Check folder permissions.';
                        } else {
                            $created = true;
                        }
                    }
                }
            }
        }
    }
}
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Add File | XAMPP Dashboard</title>
    <link rel="stylesheet" href="/assets/theme.css">
    <style>
        :root {
            --bg: #f8fafc;
            --panel: #ffffff;
            --ink: #0f172a;
            --muted: #475569;
            --line: #d1d5db;
            --accent: #0ea5e9;
            --success-bg: #ecfdf5;
            --success-ink: #065f46;
            --error-bg: #fef2f2;
            --error-ink: #991b1b;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            font-family: "Segoe UI", Tahoma, sans-serif;
            min-height: 100vh;
            background:
                radial-gradient(circle at 85% 14%, #dbeafe 0, transparent 28%),
                radial-gradient(circle at 10% 90%, #fee2e2 0, transparent 25%),
                linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
            color: var(--ink);
            display: grid;
            place-items: center;
            padding: 24px;
        }

        .card {
            width: min(760px, 100%);
            background: var(--panel);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            box-shadow: 0 18px 44px rgba(15, 23, 42, 0.12);
            overflow: hidden;
        }

        .header {
            padding: 20px 22px;
            border-bottom: 1px solid var(--line);
            background: linear-gradient(120deg, #f0f9ff, #f8fafc);
        }

        .header h1 {
            margin: 0;
            font-size: clamp(1.2rem, 3vw, 1.7rem);
        }

        .header p {
            margin: 8px 0 0;
            color: var(--muted);
        }

        .content {
            padding: 18px 22px 22px;
            display: grid;
            gap: 14px;
        }

        label {
            display: block;
            font-weight: 600;
            margin-bottom: 6px;
        }

        input[type="text"],
        textarea {
            width: 100%;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            font: inherit;
            padding: 10px 12px;
            background: #ffffff;
            color: var(--ink);
        }

        textarea {
            min-height: 220px;
            resize: vertical;
            font-family: Consolas, "Courier New", monospace;
        }

        input[type="file"] {
            width: 100%;
            border: 1px dashed #94a3b8;
            border-radius: 10px;
            font: inherit;
            padding: 10px 12px;
            background: #ffffff;
            color: var(--ink);
        }

        .checkbox-row {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 8px;
        }

        .checkbox-row label {
            margin: 0;
            font-weight: 500;
        }

        .help {
            color: var(--muted);
            font-size: 0.92rem;
            margin-top: 4px;
        }

        .message {
            border-radius: 10px;
            padding: 10px 12px;
            font-weight: 600;
        }

        .message.success {
            background: var(--success-bg);
            color: var(--success-ink);
            border: 1px solid #a7f3d0;
        }

        .message.error {
            background: var(--error-bg);
            color: var(--error-ink);
            border: 1px solid #fecaca;
        }

        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 2px;
        }

        .btn {
            display: inline-block;
            border: 1px solid #7dd3fc;
            background: #e0f2fe;
            color: #0c4a6e;
            font-weight: 700;
            text-decoration: none;
            padding: 9px 14px;
            border-radius: 999px;
            cursor: pointer;
            font: inherit;
        }

        .btn.secondary {
            border-color: #bfdbfe;
            background: #eff6ff;
            color: #1e3a8a;
        }
    </style>
</head>
<body data-page="dashboard">
    <main class="card">
        <header class="header">
            <h1>Add File</h1>
            <p>Create a new file or upload one from your local machine into any folder under htdocs.</p>
        </header>

        <section class="content">
            <?php if ($created): ?>
            <p class="message success">
                File created: <?= htmlspecialchars(basename((string)$targetFile), ENT_QUOTES, 'UTF-8') ?>
            </p>
            <?php elseif ($error !== ''): ?>
            <p class="message error"><?= htmlspecialchars($error, ENT_QUOTES, 'UTF-8') ?></p>
            <?php endif; ?>

            <form method="post" action="" enctype="multipart/form-data">
                <div>
                    <label for="location">Target folder (inside htdocs)</label>
                    <input
                        id="location"
                        name="location"
                        type="text"
                        list="location-options"
                        placeholder="projects"
                        value="<?= htmlspecialchars($location, ENT_QUOTES, 'UTF-8') ?>"
                        required
                    >
                    <datalist id="location-options">
                        <?php foreach ($locationOptions as $option): ?>
                        <option value="<?= htmlspecialchars($option, ENT_QUOTES, 'UTF-8') ?>"></option>
                        <?php endforeach; ?>
                    </datalist>
                    <p class="help">Examples: projects, wordpress, myapp/assets.</p>
                    <div class="checkbox-row">
                        <input id="create_missing_dir" name="create_missing_dir" type="checkbox" value="1" <?= $createMissingDir ? 'checked' : '' ?>>
                        <label for="create_missing_dir">Create folder if it does not exist</label>
                    </div>
                </div>

                <div>
                    <label for="local_file">Upload local file (optional)</label>
                    <input id="local_file" name="local_file" type="file">
                    <p class="help">Pick a file from anywhere on your computer, even outside the XAMPP directory.</p>
                </div>

                <div>
                    <label for="filename">File name</label>
                    <input
                        id="filename"
                        name="filename"
                        type="text"
                        placeholder="example.php"
                        value="<?= htmlspecialchars((string)($_POST['filename'] ?? ''), ENT_QUOTES, 'UTF-8') ?>"
                    >
                    <p class="help">Optional when uploading a file. Leave blank to use the uploaded file name.</p>
                    <p class="help">Allowed characters: letters, numbers, dot, underscore, dash.</p>
                </div>

                <div>
                    <label for="content">File content</label>
                    <textarea id="content" name="content" placeholder="<?php echo 'Hello'; ?>"><?= htmlspecialchars((string)($_POST['content'] ?? ''), ENT_QUOTES, 'UTF-8') ?></textarea>
                    <p class="help">Used only when no local file is uploaded.</p>
                </div>

                <div class="actions">
                    <button class="btn" type="submit">Create File</button>
                    <a class="btn secondary" href="index.php">Back to Dashboard</a>
                </div>
            </form>
        </section>
    </main>
    <script src="/assets/theme.js"></script>
</body>
</html>
