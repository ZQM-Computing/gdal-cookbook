# Security policy

## Supported version

Security fixes are applied to the `main` branch. This repository contains GDAL/OGR command-line patterns; it is not a hosted service.

## Reporting a vulnerability

Email **zqmcomputing@gmail.com** with the subject `gdal-patterns security` if you find a vulnerability in the example commands or workflow configuration — for example a pattern that silently overwrites or deletes data beyond what it documents. Please do not open a public issue for a sensitive report.

Include the affected file, the impact you observed, and reproduction steps when available.

## Command-line caution

GDAL commands act directly on your files, and flags like `-overwrite` do exactly what they say. The patterns are written against synthetic sample data; read a command before adapting it to a directory containing data you care about.
