# Validate Commits

Validate commit messages and metadata.

## Usage

```console
$ validate-commits --help
usage: validate-commits [-h]

options:
  -h, --help  show this help message and exit
```

The tool will check all commits
between `main` and the current `HEAD`.

## Checks

### Built-in rules

There are several built-in rules,
which are checked automatically:

- "Commit author has no email"
  -- all commits must have an author email.
- "Commit is empty"
  -- empty commits are not allowed.
- "Fixup commit"
  -- 'fixup' commits should be squashed into the commit they fix up.

### Custom rules

Custom rules may be provided in a `validate-commits-config.toml` file.
Rules must be provided as a regular expression pattern and an error message
and will be checked against the commit summary.

Custom rules should be defined in a `[[checks.summary]]` table,
e.g:

```toml
[[checks.summary]]
pattern = '\d'
message = "Numbers in commit summary."
```
