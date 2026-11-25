# Contributing Guidelines

## Development Principles

All contributions should prioritize correctness,
reproducibility, maintainability, and clarity.

## Development Workflow

1. Identify the current development step in ROADMAP.md.
2. Implement the required functionality.
3. Add appropriate automated tests.
4. Run all applicable quality checks.
5. Document implementation decisions and limitations.
6. Update ROADMAP.md.
7. Create a descriptive Git commit.

## Code Standards

- Use descriptive names.
- Follow PEP 8 conventions.
- Use type annotations where appropriate.
- Document public classes and functions.
- Avoid unnecessary code duplication.
- Keep modules focused on a single responsibility.
- Introduce dependencies only when justified.

## Research Standards

- Document assumptions and mathematical methods.
- Avoid look-ahead bias.
- Separate training and testing periods.
- Include transaction costs when applicable.
- Use appropriate benchmarks.
- Report positive and negative results.
- Maintain reproducible experiment configurations.

## Testing

New functionality should include automated tests.

Tests should use deterministic fixtures and should not
depend on live external market data services.

## Data Management

Do not commit credentials, API keys, large market datasets,
or data that cannot legally be redistributed.

## Commit Messages

Use descriptive conventional commit messages.

Examples:

- feat: implement historical data loader
- fix: correct portfolio accounting
- test: add return calculation tests
- docs: update development roadmap
- refactor: simplify strategy interface
- ci: configure automated quality checks
- chore: update project dependencies
