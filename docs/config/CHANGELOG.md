# Changelog

## [1.0.2] - 2024-04-16

### Changed
- Added requests header to prevent 403 error when scraping questions.
- Fixed a typo in the example notebook.


## [1.0.1] - 2024-01-04

### Changed
- Updated the pyproject.toml file to make `marko` a required dependency. It was previously an extra `file` dependency. I had included it as an extra so that users who simply want to get question information would not have to install `marko` as well. However, seeing as `leetscrape question <qid>` is a core feature of the package, I have decided to make `marko` a required dependency.

### Docs
- Added this changelog section to the docs.
- Fixed inactive badges in the Homepage.

### README
- Updated the README to call out the new Changelog page on the docs.