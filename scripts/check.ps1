$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")

function Invoke-Check {
    param(
        [string]$Name,
        [string[]]$Arguments
    )

    Write-Host "`n=== $Name ===" -ForegroundColor Cyan

    & uv @Arguments

    if ($LASTEXITCODE -ne 0) {
        throw "$Name failed with exit code $LASTEXITCODE."
    }

    Write-Host "$Name passed." -ForegroundColor Green
}

# 1. Synchronize dependencies
Invoke-Check -Name "Dependency synchronization" -Arguments @(
    "sync", "--locked"
)

# 2. Check and automatically fix linting
Write-Host "`n=== Ruff linting ===" -ForegroundColor Cyan

uv run --locked ruff check .

if ($LASTEXITCODE -eq 1) {
    Write-Host "Linting issues detected. Applying safe fixes..." `
        -ForegroundColor Yellow

    uv run --locked ruff check . --fix

    if ($LASTEXITCODE -gt 1) {
        throw "Ruff encountered an unexpected error."
    }
}
elseif ($LASTEXITCODE -ne 0) {
    throw "Ruff linting failed to execute."
}

# 3. Automatically fix formatting
Invoke-Check -Name "Automatic formatting" -Arguments @(
    "run", "--locked", "ruff", "format", "."
)

# 4. Verify linting after automatic fixes
Invoke-Check -Name "Final linting verification" -Arguments @(
    "run", "--locked", "ruff", "check", "."
)

# 5. Verify formatting after automatic fixes
Invoke-Check -Name "Final formatting verification" -Arguments @(
    "run", "--locked", "ruff", "format", "--check", "."
)

# 6. Static type checking
Invoke-Check -Name "Static type checking" -Arguments @(
    "run", "--locked", "mypy", "src"
)

# 7. Automated tests and coverage
Invoke-Check -Name "Tests and coverage" -Arguments @(
    "run", "--locked", "pytest",
    "--cov=quantlab",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml"
)

# 8. Package build
Invoke-Check -Name "Package build" -Arguments @(
    "build"
)

Write-Host "`n========================================" `
    -ForegroundColor Green

Write-Host "All quality checks passed." `
    -ForegroundColor Green

Write-Host "========================================" `
    -ForegroundColor Green

Write-Host "`nReview any automatically modified files before committing."
