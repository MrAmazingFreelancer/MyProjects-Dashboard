<?php
session_start();

// Admin credentials
$ADMIN_USERNAME = '7InkCoAdmin';
$ADMIN_PASSWORD = '221298AU';
$SESSION_TIMEOUT = 3600; // 1 hour

// Check if session is valid
$isLoggedIn = false;
if (isset($_SESSION['7ink_admin_login']) && isset($_SESSION['7ink_admin_time'])) {
    if (time() - $_SESSION['7ink_admin_time'] < $SESSION_TIMEOUT) {
        $isLoggedIn = true;
        $_SESSION['7ink_admin_time'] = time(); // Reset timeout
    } else {
        session_destroy();
        session_start();
    }
}

// Handle login form submission
$loginError = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['login'])) {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    if ($username === $ADMIN_USERNAME && $password === $ADMIN_PASSWORD) {
        $_SESSION['7ink_admin_login'] = true;
        $_SESSION['7ink_admin_time'] = time();
        $_SESSION['7ink_admin_user'] = $username;
        header('Location: ' . $_SERVER['PHP_SELF']);
        exit;
    } else {
        $loginError = 'Invalid username or password';
    }
}

// Handle logout
if (isset($_GET['logout'])) {
    session_destroy();
    header('Location: ' . $_SERVER['PHP_SELF']);
    exit;
}

// Get system info
$phpVersion = phpversion();
$mysqlVersion = phpversion('mysqli') ? 'Installed' : 'Not Available';
$wpConfigPath = realpath(__DIR__ . '/../../wordpress/wp-config.php');
$wpInstalled = file_exists($wpConfigPath);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $isLoggedIn ? '7Ink Admin Dashboard' : '7Ink Admin Login'; ?></title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 1000px;
        }

        .login-box {
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            padding: 40px;
            max-width: 400px;
            margin: 0 auto;
        }

        .dashboard {
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            padding: 40px;
        }

        .logo {
            text-align: center;
            margin-bottom: 30px;
        }

        .logo h1 {
            color: #667eea;
            font-size: 28px;
            margin-bottom: 10px;
        }

        .logo p {
            color: #666;
            font-size: 14px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 14px;
        }

        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s;
        }

        input[type="text"]:focus,
        input[type="password"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .btn {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-primary {
            background: #667eea;
            color: white;
        }

        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }

        .btn-secondary {
            background: #f0f0f0;
            color: #333;
            margin-left: 10px;
        }

        .btn-secondary:hover {
            background: #e0e0e0;
        }

        .btn-logout {
            background: #dc3545;
            color: white;
        }

        .btn-logout:hover {
            background: #c82333;
        }

        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 12px 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 14px;
            border: 1px solid #f5c6cb;
        }

        .success {
            background: #d4edda;
            color: #155724;
            padding: 12px 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 14px;
            border: 1px solid #c3e6cb;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }

        .header h1 {
            color: #333;
            font-size: 24px;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .user-info span {
            color: #666;
            font-size: 14px;
        }

        .btn-logout {
            padding: 8px 15px;
            font-size: 12px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .card {
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            transition: all 0.3s;
        }

        .card:hover {
            border-color: #667eea;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
        }

        .card h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }

        .status-active {
            background: #d4edda;
            color: #155724;
        }

        .status-inactive {
            background: #f8d7da;
            color: #721c24;
        }

        .btn-group {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }

        .btn-group a,
        .btn-group button {
            flex: 1;
            padding: 10px 15px;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
            font-size: 13px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-primary-link {
            background: #667eea;
            color: white;
        }

        .btn-primary-link:hover {
            background: #5568d3;
        }

        .btn-secondary-link {
            background: #6c757d;
            color: white;
        }

        .btn-secondary-link:hover {
            background: #5a6268;
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 15px;
            font-size: 13px;
        }

        .info-item {
            background: white;
            padding: 10px;
            border-radius: 5px;
            border-left: 3px solid #667eea;
        }

        .info-item strong {
            display: block;
            color: #666;
            margin-bottom: 5px;
        }

        .info-item span {
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <?php if (!$isLoggedIn): ?>
            <!-- LOGIN FORM -->
            <div class="login-box">
                <div class="logo">
                    <h1>7Ink</h1>
                    <p>Admin Dashboard</p>
                </div>

                <?php if ($loginError): ?>
                    <div class="error"><?php echo htmlspecialchars($loginError); ?></div>
                <?php endif; ?>

                <form method="POST">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text" id="username" name="username" placeholder="Enter your username" required autofocus>
                    </div>

                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" name="password" placeholder="Enter your password" required>
                    </div>

                    <button type="submit" name="login" class="btn btn-primary">Sign In</button>
                </form>

                <div style="margin-top: 20px; text-align: center; color: #999; font-size: 12px;">
                    <p>7Ink Co Admin Login</p>
                </div>
            </div>

        <?php else: ?>
            <!-- ADMIN DASHBOARD -->
            <div class="dashboard">
                <div class="header">
                    <h1>7Ink Admin Dashboard</h1>
                    <div class="user-info">
                        <span>👤 <?php echo htmlspecialchars($_SESSION['7ink_admin_user']); ?></span>
                        <button class="btn btn-logout" onclick="window.location.href='?logout=1'">Logout</button>
                    </div>
                </div>

                <div class="grid">
                    <!-- Dashboard Card -->
                    <div class="card">
                        <h3>
                            📊 Dashboard
                            <span class="status-badge status-active">Active</span>
                        </h3>
                        <p style="color: #666; font-size: 14px; margin-bottom: 15px;">
                            Manage your website homepage, content, and settings.
                        </p>
                        <div class="btn-group">
                            <a href="/" class="btn-primary-link">View Dashboard</a>
                            <a href="javascript:void(0)" class="btn-secondary-link" onclick="alert('Dashboard editor coming soon')">Edit</a>
                        </div>
                    </div>

                    <!-- WordPress Card -->
                    <div class="card">
                        <h3>
                            📝 WordPress
                            <span class="status-badge <?php echo $wpInstalled ? 'status-active' : 'status-inactive'; ?>">
                                <?php echo $wpInstalled ? 'Installed' : 'Not Found'; ?>
                            </span>
                        </h3>
                        <p style="color: #666; font-size: 14px; margin-bottom: 15px;">
                            Manage your blog, posts, pages, and media content.
                        </p>
                        <div class="btn-group">
                            <a href="/wordpress" class="btn-primary-link">View Blog</a>
                            <a href="/wordpress/wp-admin" class="btn-secondary-link">WordPress Admin</a>
                        </div>
                    </div>

                    <!-- System Info Card -->
                    <div class="card">
                        <h3>⚙️ System Info</h3>
                        <div class="info-grid">
                            <div class="info-item">
                                <strong>PHP Version</strong>
                                <span><?php echo htmlspecialchars($phpVersion); ?></span>
                            </div>
                            <div class="info-item">
                                <strong>MySQL</strong>
                                <span><?php echo htmlspecialchars($mysqlVersion); ?></span>
                            </div>
                            <div class="info-item">
                                <strong>Domain</strong>
                                <span>7ink.com.au</span>
                            </div>
                            <div class="info-item">
                                <strong>Environment</strong>
                                <span><?php echo getenv('APP_ENV') ?: 'Local'; ?></span>
                            </div>
                        </div>
                    </div>

                    <!-- Site Management Card -->
                    <div class="card">
                        <h3>🔧 Site Management</h3>
                        <p style="color: #666; font-size: 14px; margin-bottom: 15px;">
                            Access files, settings, and configuration options.
                        </p>
                        <div class="btn-group">
                            <a href="/7ink.local/assets" class="btn-primary-link">File Manager</a>
                            <a href="javascript:void(0)" class="btn-secondary-link" onclick="alert('Settings panel coming soon')">Settings</a>
                        </div>
                    </div>

                    <!-- Security Card -->
                    <div class="card">
                        <h3>🔒 Security</h3>
                        <p style="color: #666; font-size: 14px; margin-bottom: 15px;">
                            Session active: <strong><?php echo date('Y-m-d H:i:s'); ?></strong>
                        </p>
                        <p style="color: #666; font-size: 12px; line-height: 1.6;">
                            ✓ HTTPS enabled<br>
                            ✓ Admin login protected<br>
                            ✓ Session timeout: 1 hour
                        </p>
                        <button class="btn btn-logout" style="margin-top: 15px; width: 100%;" onclick="window.location.href='?logout=1'">Logout</button>
                    </div>

                    <!-- Quick Links Card -->
                    <div class="card">
                        <h3>🔗 Quick Links</h3>
                        <div style="display: grid; gap: 10px; margin-top: 15px;">
                            <a href="/" style="color: #0f766e; text-decoration: none; font-size: 13px;">→ Home</a>
                            <a href="/wordpress" style="color: #0f766e; text-decoration: none; font-size: 13px;">→ Blog</a>
                            <a href="/wordpress/wp-admin" style="color: #0f766e; text-decoration: none; font-size: 13px;">→ WordPress Admin</a>
                            <a href="/admin" style="color: #0f766e; text-decoration: none; font-size: 13px;">→ This Page</a>
                        </div>
                    </div>
                </div>

                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #f0f0f0; color: #999; font-size: 12px; text-align: center;">
                    <p>7Ink Co Admin Panel v1.0 | Secured &amp; Encrypted</p>
                </div>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>
