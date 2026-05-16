<?php

declare(strict_types=1);

require_once dirname(__DIR__, 2) . '/_dashboard/lib/db-check-data.php';

testCase('buildDbDefaultConfig applies defaults when values are missing', function (): void {
    $config = buildDbDefaultConfig([]);
    assertSameValue('127.0.0.1', $config['host']);
    assertSameValue('3306', $config['port']);
    assertSameValue('root', $config['user']);
    assertSameValue('', $config['password']);
    assertSameValue('', $config['database']);
    assertSameValue('utf8mb4', $config['charset']);
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

    assertSameValue('db.local', $config['host']);
    assertSameValue('3307', $config['port']);
    assertSameValue('admin', $config['user']);
    assertSameValue('12345', $config['password']);
    assertSameValue('main', $config['database']);
    assertSameValue('latin1', $config['charset']);
});

testCase('selectedDatabaseLabel handles empty and non-empty names', function (): void {
    assertSameValue('(none)', selectedDatabaseLabel(''));
    assertSameValue('analytics', selectedDatabaseLabel('analytics'));
});
