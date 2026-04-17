<?php
$defaultConfig = [
    'host' => $_POST['host'] ?? '127.0.0.1',
    'port' => $_POST['port'] ?? '3306',
    'user' => $_POST['user'] ?? 'root',
    'password' => $_POST['password'] ?? '',
    'database' => $_POST['database'] ?? '',
    'charset' => $_POST['charset'] ?? 'utf8mb4',
];

$result = null;
$error = null;
$serverInfo = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!extension_loaded('mysqli')) {
        $error = 'The mysqli extension is not loaded in PHP.';
    } else {
        mysqli_report(MYSQLI_REPORT_OFF);

        $mysqli = @mysqli_init();
        if ($mysqli === false) {
            $error = 'Unable to initialize a MySQLi client.';
        } else {
            $connected = @mysqli_real_connect(
                $mysqli,
                $defaultConfig['host'],
                $defaultConfig['user'],
                $defaultConfig['password'],
                $defaultConfig['database'] !== '' ? $defaultConfig['database'] : null,
                (int) $defaultConfig['port']
            );

            if ($connected) {
                @mysqli_set_charset($mysqli, $defaultConfig['charset']);
                $serverInfo = mysqli_get_server_info($mysqli);

                $ping = mysqli_ping($mysqli);
                $result = [
                    'success' => true,
                    'message' => $ping
                        ? 'Connection established and ping succeeded.'
                        : 'Connection established but ping failed.',
                    'db_selected' => $defaultConfig['database'] !== '' ? $defaultConfig['database'] : '(none)',
                ];
            } else {
                $result = [
                    'success' => false,
                    'message' => mysqli_connect_error() ?: 'Connection failed for an unknown reason.',
                    'code' => mysqli_connect_errno(),
                ];
            }

            mysqli_close($mysqli);
        }
    }
}
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MySQL Connection Check</title>
    <style>
        :root {
            --bg: #f5fbf7;
            --card: #ffffff;
            --ink: #12212e;
            --muted: #5f6b77;
            --ok: #0f766e;
            --bad: #b91c1c;
            --line: #d5dde5;
            --accent: #0369a1;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            padding: 20px;
            color: var(--ink);
            font-family: "Segoe UI", Tahoma, sans-serif;
            background:
                radial-gradient(circle at 12% 16%, #d8f3dc 0, transparent 38%),
                radial-gradient(circle at 88% 10%, #dbeafe 0, transparent 32%),
                linear-gradient(180deg, #f8fff9 0%, #eef8ff 100%);
        }

        .card {
            width: min(900px, 100%);
            background: var(--card);
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            box-shadow: 0 20px 44px rgba(2, 6, 23, 0.12);
            overflow: hidden;
        }

        header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--line);
            background: linear-gradient(120deg, #ecfeff, #eff6ff);
        }

        h1 {
            margin: 0;
            font-size: clamp(1.2rem, 2.6vw, 1.8rem);
        }

        .sub {
            margin: 8px 0 0;
            color: var(--muted);
        }

        .content {
            padding: 20px 24px 24px;
            display: grid;
            gap: 14px;
        }

        .row {
            display: grid;
            grid-template-columns: 1fr;
            gap: 8px;
        }

        @media (min-width: 700px) {
            .row.two {
                grid-template-columns: 1fr 1fr;
                gap: 14px;
            }
        }

        label {
            font-size: 0.92rem;
            font-weight: 600;
            display: grid;
            gap: 6px;
        }

        input {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid var(--line);
            border-radius: 10px;
            color: var(--ink);
            font-size: 0.94rem;
        }

        input:focus {
            outline: 2px solid #bae6fd;
            border-color: #38bdf8;
        }

        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 4px;
        }

        button,
        .link {
            border: 0;
            border-radius: 10px;
            padding: 10px 14px;
            font-weight: 700;
            cursor: pointer;
            text-decoration: none;
            font-size: 0.94rem;
        }

        button {
            color: #fff;
            background: #0284c7;
        }

        .link {
            color: #0f172a;
            background: #e2e8f0;
        }

        .panel {
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 14px;
            background: #fcfdff;
        }

        .ok { color: var(--ok); font-weight: 700; }
        .bad { color: var(--bad); font-weight: 700; }
        .mono { font-family: Consolas, monospace; word-break: break-word; }

        .hint {
            margin: 0;
            color: var(--muted);
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <main class="card">
        <header>
            <h1>MySQL Connection Check</h1>
            <p class="sub">Test credentials against your local XAMPP MySQL service.</p>
        </header>

        <form method="post" class="content">
            <div class="row two">
                <label>Host
                    <input name="host" value="<?= htmlspecialchars($defaultConfig['host'], ENT_QUOTES, 'UTF-8') ?>" required>
                </label>
                <label>Port
                    <input name="port" value="<?= htmlspecialchars($defaultConfig['port'], ENT_QUOTES, 'UTF-8') ?>" required>
                </label>
            </div>

            <div class="row two">
                <label>User
                    <input name="user" value="<?= htmlspecialchars($defaultConfig['user'], ENT_QUOTES, 'UTF-8') ?>" required>
                </label>
                <label>Password
                    <input type="password" name="password" value="<?= htmlspecialchars($defaultConfig['password'], ENT_QUOTES, 'UTF-8') ?>">
                </label>
            </div>

            <div class="row two">
                <label>Database (optional)
                    <input name="database" value="<?= htmlspecialchars($defaultConfig['database'], ENT_QUOTES, 'UTF-8') ?>" placeholder="leave blank to test server login only">
                </label>
                <label>Charset
                    <input name="charset" value="<?= htmlspecialchars($defaultConfig['charset'], ENT_QUOTES, 'UTF-8') ?>">
                </label>
            </div>

            <div class="actions">
                <button type="submit">Test Connection</button>
                <a class="link" href="index.php">Back to Health Dashboard</a>
            </div>

            <p class="hint">Tip: default XAMPP credentials are often user root with empty password.</p>

            <?php if ($error !== null): ?>
            <section class="panel">
                <p class="bad">Error: <?= htmlspecialchars($error, ENT_QUOTES, 'UTF-8') ?></p>
            </section>
            <?php endif; ?>

            <?php if ($result !== null): ?>
            <section class="panel">
                <p class="<?= $result['success'] ? 'ok' : 'bad' ?>">
                    <?= $result['success'] ? 'Success' : 'Failed' ?>
                </p>
                <p class="mono">
                    <?= htmlspecialchars($result['message'], ENT_QUOTES, 'UTF-8') ?>
                </p>
                <?php if (isset($result['code'])): ?>
                <p class="mono">MySQL Error Code: <?= (int) $result['code'] ?></p>
                <?php endif; ?>
                <?php if ($result['success']): ?>
                <p class="mono">Selected DB: <?= htmlspecialchars($result['db_selected'], ENT_QUOTES, 'UTF-8') ?></p>
                <p class="mono">Server: <?= htmlspecialchars((string) $serverInfo, ENT_QUOTES, 'UTF-8') ?></p>
                <?php endif; ?>
            </section>
            <?php endif; ?>
        </form>
    </main>
</body>
</html>
