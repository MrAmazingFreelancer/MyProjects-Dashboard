# 7ink.com.au cPanel Interface Starter Install

This package contains a starter plugin interface for the Jupiter theme.

## 1. Upload frontend files

Copy this folder to your server:

- Local: `frontend/sevenink/`
- Server: `/usr/local/cpanel/base/frontend/jupiter/sevenink/`

## 2. Install DynamicUI config

Copy `dynamicui.conf` to:

- `/usr/local/cpanel/base/frontend/jupiter/dynamicui/dynamicui_sevenink.conf`

## 3. Set ownership/permissions

Run:

```bash
chown -R root:root /usr/local/cpanel/base/frontend/jupiter/sevenink
chmod 0644 /usr/local/cpanel/base/frontend/jupiter/sevenink/*
chmod 0644 /usr/local/cpanel/base/frontend/jupiter/dynamicui/dynamicui_sevenink.conf
```

## 4. Rebuild cPanel cache

Run:

```bash
/usr/local/cpanel/bin/rebuild_sprites
/usr/local/cpanel/bin/rebuild_cpdavd_db
/scripts/clear_orphaned_virtfs_mounts --clearall
```

Then sign out/in to cPanel.

## 5. Important setting

Inside `index.html.tt`, keep:

```tt2
[% SET CPANEL.CPVAR.dprefix = '../' %]
```

This is required for internal cPanel links/search/menu behavior.
