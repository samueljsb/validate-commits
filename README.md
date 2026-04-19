# Validate Commits

Validate commit messages and metadata.

## Usage

```console
$ validate-commits --help
usage: validate-commits [-h] [--since SINCE]

options:
  -h, --help     show this help message and exit
  --since SINCE  check commits since this reference
```

The tool will check all commits
between `main` and the current `HEAD`.

## Checks

### Built-in rules

There are several built-in rules,
which are checked automatically:

- "Commit author has no email"
  -- all commits must have an author email
  and all co-authors (in `Co-authored-by` trailers) must have an email.
- "Commit is empty"
  -- empty commits are not allowed.
- "Fixup commit"
  -- 'fixup' commits should be squashed into the commit they fix up.

### Custom rules

Custom rules may be provided in a `validate-commits-config.toml` file.
Rules must be provided as a regular expression pattern and an error message
and will be checked against the designated target.

### Commit summary

Checks for the commit summary (the first line of the commit message)
may be defined in a `[[checks.summary]]` table,
e.g:

```toml
[[checks.summary]]
pattern = '\d'
message = "Numbers in commit summary."
```

### Author email

Checks for author and co-author email addresses
may be defined in a `[[checks.author_email]]` table,
e.g:

```toml
[[checks.author_email]]
pattern = '@example\.(com|net|org)$'
message = "Fake email address provided."
```

## `pre-commit`

A pre-push hook is provided for `pre-commit`
and can be configured in your `.pre-commit-config.yaml`:

```yaml
default_install_hook_types: [pre-commit, pre-push]
default_stages: [pre-commit]

repos:
    # ...
    - repo: https://github.com/samueljsb/validate-commits
      rev: v0.0.3
      hooks:
          - id: validate-commits
```

N.B. This hook only runs in the pre-push stage.
Therefore, the pre-push hook must be installed,
which may require `pre-commit install` to be run again.
To ensure _other_ hooks are not run unexpectedly during the pre-push stage,
the default stage must be set at the top level.
