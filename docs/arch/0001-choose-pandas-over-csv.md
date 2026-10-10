# ADR 1: Load Alpha Vantage JSON payloads as pandas DataFrames

- Status: Accepted
- Date: 2026-10-10

## Context

Alpha Vantage returns nested JSON. The response JSON was initially parsed using Python standard library and written as a CSV file with the `csv` module.

## Decision

Pandas supports easier parsing and conversion of JSON payloads.

Pass the JSON response to `DataFrame()` or `DataFrame.from_dict(..., orient="index")`

## Consequences

- `pandas` is a required dependency for ingestion

## Alternatives considered

**json plus the csv module** Flatten each row into a dict and write it with `csv.DictWriter`.
