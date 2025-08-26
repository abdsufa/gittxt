# Contribution Guidelines

Thank you for your interest in contributing to gittxt!

## Rules and Coding Conventions

* Everything needed to run & understand the code lives in the repo, start from `README.md` and the file/function doc-strings.
* 4-space indentation, 87-character lines.
* `snake_case` for functions/variables; `PascalCase` for classes, `UPPER_CASE` for `CONSTANTS`.
* Be clear & Pythonic—pick self-explanatory names and comment only when ambiguity remains.
* Every file's first line should be `# gittxt/path/to/file_name.py -------` (except if it will break the file, e.g. json).
* Doc-string every public file, class & function (triple quotes, imperative).
* Import order: std-lib → 3rd-party → local, alphabetized & blank-line separated.
* Type-hint everywhere.
* Any static analysis suppression reason must be stated in the same line.
* No executable top-level code except inside a guard block: `if __name__ == "__main__":`.
* Keep functions < 42 LOC, modules < 420 LOC.
* Never use mutable default args—guard with `if arg is None:`.

## Versioning & Release History

* We use Semantic Versioning (`MAJOR.MINOR.PATCH`) and maintain a human-readable changelog in `CHANGELOG.md`.
* For any release, the `CHANGELOG.md` must be updated and a commit must be made with a message like `release: vX.Y.Z`.
*  Please Don’t dump git logs into changelogs.
