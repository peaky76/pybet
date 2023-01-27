# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The versioning refers to the versions on pypi

## [Unreleased]

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

## [0.3.0] - 2022-05-29

### Added

#### On `Market` class

- `.apply_margin` instance method
- `.equalise` instance method
- `.fill` instance method
- `.wipe` instance method

## [0.4.0] - 2023-01-27

### Added

- `staking` module
- `staking.kelly` method
