<?php

/**
 * @param array<string, mixed> $post
 * @return array{host: string, port: string, user: string, password: string, database: string, charset: string}
 */
function buildDbDefaultConfig(array $post): array
{
    return [
        'host' => isset($post['host']) ? (string) $post['host'] : '127.0.0.1',
        'port' => isset($post['port']) ? (string) $post['port'] : '3306',
        'user' => isset($post['user']) ? (string) $post['user'] : 'root',
        'password' => isset($post['password']) ? (string) $post['password'] : '',
        'database' => isset($post['database']) ? (string) $post['database'] : '',
        'charset' => isset($post['charset']) ? (string) $post['charset'] : 'utf8mb4',
    ];
}

function selectedDatabaseLabel(string $database): string
{
    return $database !== '' ? $database : '(none)';
}
