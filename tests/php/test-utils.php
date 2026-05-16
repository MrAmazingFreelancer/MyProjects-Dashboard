<?php

declare(strict_types=1);

$GLOBALS['test_cases'] = [];

function testCase(string $name, callable $fn): void
{
    $GLOBALS['test_cases'][] = [$name, $fn];
}

function assertSameValue($expected, $actual, string $message = ''): void
{
    if ($expected !== $actual) {
        $label = $message !== '' ? $message : 'Values are not identical.';
        throw new RuntimeException($label . PHP_EOL . 'Expected: ' . var_export($expected, true) . PHP_EOL . 'Actual: ' . var_export($actual, true));
    }
}

function assertTrue(bool $value, string $message = ''): void
{
    if (!$value) {
        throw new RuntimeException($message !== '' ? $message : 'Expected condition to be true.');
    }
}

function runAllTests(): void
{
    $passed = 0;
    foreach ($GLOBALS['test_cases'] as [$name, $fn]) {
        $fn();
        echo "PASS: {$name}\n";
        $passed++;
    }

    echo "Completed {$passed} tests.\n";
}
