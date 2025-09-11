# Changelog

**All notable changes to this project will be documented in this file.**

- The format is based on [keep-a-changelog](https://keepachangelog.com/en/1.1.0/),
- and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

`SV 2.0.0 = MAJOR . MINOR . PATCH - Pre-Release(Alpha, Beta) + Build(Number)`

## [0.4.0] - 11-Sep-2025

### Changed

- **Sorting Logic**: The output digest now sorts files by directory depth.
Files in the root (`./file.txt`) appear before files in subdirectories (`./src/main.py`).
- **Dotfile Sorting**: Files or directories starting with a `.` are now sorted last,
regardless of their directory depth.
- **Default Ignores**: `.gitignore` files are now ignored by default and excluded
from the output digest.

## [0.3.0] - 2025-08-27

### Changed

- Enhance CHANGELOG.
- Add versions.
- Add README badges.

## [0.2.0] - 2025-08-19

### Changed

- **Major Improvement**: The script now uses `git ls-files` to get a list of tracked files
This is much faster and more accurately respects `.gitignore` rules than the previous
manual method.
- The script now gracefully falls back to the manual `os.walk` method if the target
directory is not a Git repository or if `git` is not installed.
- Improved binary file detection by checking for null bytes in files, rather than
relying solely on a list of extensions.
- Replaced basic `sys.argv` with the `argparse` module fora proper
command-line interface, adding support for `--output` and `--max-bytes` arguments.
- Token estimation is now more accurate if the `tiktoken` library is installed,
otherwise it falls back to a character-based heuristic.

## [0.1.0] - 2025-08-19

### Added

- Initial version of the `gittxt` script.
- Core functionality to process a local Git repository into a single text file.
- Smart filtering based on `.gitignore`, default ignore patterns, and non-source file types.
- Generation of a directory tree at the beginning of the output file.
- Prioritization of `README.md` and `CHANGELOG.md` in the output.

[0.4.0]: https://github.com/abdsufa/gittxt/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/abdsufa/gittxt/compare/v0.1.0...v0.3.0
[0.2.0]: https://github.com/abdsufa/gittxt/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/abdsufa/gittxt/releases/tag/v0.1.0
