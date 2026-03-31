# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Custom checks for author email addresses.
  These can be configured in a `checks.author-email` table,
  e.g:

    ```toml
    [[checks.author_email]]
    pattern = '@example\.(com|net|org)$'
    message = "Fake email address provided."
    ```

## [0.0.1] - 2026-03-23

The first release of this tool.
