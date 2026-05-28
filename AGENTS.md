# AGENTS.md

## Project

Pricing service for an e-commerce platform.
Handles discounts (volume, coupon), tax calculation, and final price breakdown.

## Setup

```bash
pip install -r requirements.txt
pytest
```

## Architecture

| File               | Role                                      |
|--------------------|-------------------------------------------|
| app/models.py      | Data classes: Customer, Order, OrderItem  |
| app/discounts.py   | Discount rules and cap logic              |
| app/pricing.py     | Orchestrates discounts + tax              |
| tests/             | Pytest test suite                         |

## Development rules

- Propose a plan before editing any file.
- Keep diffs minimal — change only what is necessary.
- Add tests for every new behavior, including edge cases.
- Do not change public function signatures unless explicitly requested.
- Prefer simple code over clever abstractions.
- Do not modify unrelated files.

## Safety

- Summarize all changed files at the end of your response.
- Explain any non-obvious decision in the diff.
- Run the test suite after implementing changes.
