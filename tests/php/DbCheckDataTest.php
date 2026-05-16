<?php

declare(strict_types=1);

require_once dirname(__DIR__, 2) . '/_dashboard/lib/db-check-data.php';

testCase('buildDbDefaultConfig applies defaults when values are missing', function (): void {
    $config = buildDbDefaultConfig([]);
    assertStrictEqual('127.0.0.1', $config['host']);
    assertStrictEqual('3306', $config['port']);
    assertStrictEqual('root', $config['user']);
    assertStrictEqual('', $config['password']);
    assertStrictEqual('', $config['database']);
    assertStrictEqual('utf8mb4', $config['charset']);
});

testCase('buildDbDefaultConfig casts posted values to strings', function (): void {
    $config = buildDbDefaultConfig([
        'host' => 'db.local',
        'port' => 3307,
        'user' => 'admin',
        'password' => 12345,
        'database' => 'main',
        'charset' => 'latin1',
    ]);

    assertStrictEqual('db.local', $config['host']);
    assertStrictEqual('3307', $config['port']);
    assertStrictEqual('admin', $config['user']);
    assertStrictEqual('12345', $config['password']);
    assertStrictEqual('main', $config['database']);
    assertStrictEqual('latin1', $config['charset']);
});

testCase('selectedDatabaseLabel handles empty and non-empty names', function (): void {
    assertStrictEqual('(none)', selectedDatabaseLabel(''));
    assertStrictEqual('analytics', selectedDatabaseLabel('analytics'));
});
