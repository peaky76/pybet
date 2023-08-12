# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The versioning refers to the versions on pypi

## [0.7.3] (2023-08-12)

### Docs

- add `Market.derive` details
- amend api and getting started documentation

## [0.7.2] (2023-08-08)

### Fixes

- typing in `Market.derive`

### Docs

- fix config ref in `.readthedocs.yaml`

## [0.7.1] (2023-08-08)

### Docs

- add `.readthedocs.yaml` v2 config

### Others

- ruff ignore E731
- refactor `Market` testing to harmonise approaches

## [0.7.0] (2023-08-08)

### New Features

- `Market.derive` method

### Others

- ruff ignore F821

## [0.6.2] (2023-05-08)

### Fixes

- make `Odds.__repr__` class specific
- allow `Odds.probability` and `Odds.percentage` class methods to operate at "never" and "always" extremes

### Others

- add ruff

## [0.6.1] (2023-05-05)

### Fixes

- fix for `ValueError` check in `Market.meld` (was merged pre-0.6.0 but missing from release)

## [0.6.0] (2023-04-29)

### New Features

- `Market.meld` method

## [0.5.0] (2023-04-27)

### New Features

- optional commission arg in `kelly`

### Docs

- minor style fix on CHANGELOG

### Others

- reorder dependencies in `pyproject.toml`
- add `prep.sh` script

## [0.4.2] (2023-02-24)

### Refactorings

- Improve type hinting in `kelly`
- Improve var names in `kelly`
- Replace check for negative `kelly` with use of max

### Others

- Configure ignores for coverage
- Complete coverage in `Odds` and `Market`
- Suspend type checking on complex constructors

## [0.4.1] - 2023-02-18

### Added

- [Documentation pages at readthedocs.io](https://pybet.readthedocs.io)

### Other

- Major internal linting, build and ci changes

## [0.4.0] - 2023-01-27

### Added

- `staking` module
- `staking.kelly` method

## [0.3.0] - 2022-05-29

### Added

#### On `Market` class

- `.apply_margin` instance method
- `.equalise` instance method
- `.fill` instance method
- `.wipe` instance method

## [0.2.0] - 2022-02-02

### Added

- `Market` class
- `.favourites` property
- `.percentage` property
- `.overround_per_runner` property
- `.is_overbroke` property
- `.is_overround` property
- `.is_fair` property
- `.without` instance method

## [0.1.0] - 2022-01-30

### Added

- `Odds` class
- Class methods to instantiate `Odds` from moneyline, fractional odds, implied percentage and probability
- Instance methods to convert `Odds` to moneyline, fractional odds, implied percentage and probability
- `.evens` class method
- `.inverted` class method
- `.is_odds_against` and `.is_odds_on` properties
- Dunder methods for `__str__, __add__, __mul__, __rmul__, __true_div__`
- `STANDARD_FRACTIONALS` constant
