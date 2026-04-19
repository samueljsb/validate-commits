# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.3] - 2026-04-19

### Added

- The `--since` CLI option
  allows a base reference to be provided.
  This facilitates checking commits since a default branch
  that is not called 'main'.
- A [pre-commit](https://pre-commit.com) hook definition.

## [0.0.2] - 2026-03-31

### Added

- Custom checks for author and co-author email addresses.
  These can be configured in a `checks.author-email` table,
  e.g:

    ```toml
    [[checks.author_email]]
    pattern = '@example\.(com|net|org)$'
    message = "Fake email address provided."
    ```

### Changed

- "Commit author has no email" now also checks co-author emails,
  as determined from `Co-authored-by` trailers.
- Error messages now indicate why a check failed,
  by showing the name of the author without an email
  or the portion of a summary/email that matched a custom rule.

## [0.0.1] - 2026-03-23

The first release of this tool.
