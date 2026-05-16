<?php

declare(strict_types=1);

$GLOBALS['test_cases'] = [];

function testCase(string $name, callable $fn): void
{
    $GLOBALS['test_cases'][] = [$name, $fn];
}

function assertStrictEqual($expected, $actual, string $message = ''): void
{
    if ($expected !== $actual) {
        $label = $message !== '' ? $message : 'Values are not identical.';
        $details = sprintf(
            "%s\nExpected:\n%s\nActual:\n%s",
            $label,
            var_export($expected, true),
            var_export($actual, true)
        );
        throw new RuntimeException($details);
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
    $failed = 0;
    foreach ($GLOBALS['test_cases'] as [$name, $fn]) {
        try {
            $fn();
            echo "PASS: {$name}\n";
            $passed++;
        } catch (Throwable $throwable) {
            echo "FAIL: {$name}\n";
            echo $throwable->getMessage() . "\n";
            $failed++;
        }
    }

    echo "Completed {$passed} passing and {$failed} failing tests.\n";
    if ($failed > 0) {
        exit(1);
    }
}
