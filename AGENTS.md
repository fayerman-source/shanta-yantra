# Repository Guidelines

## Project Structure & Module Organization
This repository is a docs-first public skeleton for Shanta Yantra. The root contains the core project documents, and `docs/` holds the stable design references.

- `README.md`: public overview and positioning.
- `GOVERNANCE.md`: decision framework and feature boundaries.
- `docs/ARCHITECTURE.md`: three-phase architecture overview.
- `docs/INTERACTION_MODEL.md`: response model and session rules.
- `docs/ROADMAP.md`: implementation sequence.

If code is added later, place runtime code under `src/` and tests under `tests/` or the language-standard equivalent.

## Build, Test, and Development Commands
There is no application build yet. Current work is document curation and design refinement.

- `git status`: inspect pending changes.
- `rg "term" .`: find terminology across docs.
- `git log --oneline`: review commit style.
- `markdownlint **/*.md`: optional Markdown validation if installed.

## Writing Style & Naming Conventions
Use direct, plain language. Prefer short sections, concrete headings, and examples over abstract claims. Keep names stable and descriptive.

File naming:
- root docs use canonical names such as `README.md` and `GOVERNANCE.md`
- design docs in `docs/` use uppercase descriptive filenames such as `ARCHITECTURE.md`

Avoid lineage claims, internal provenance notes, or speculative metaphysical language in public-facing files.

## Testing Guidelines
Testing currently means consistency checks across documents.

Before committing:
- verify links and file references
- grep for banned internal terms or private paths
- confirm terminology stays aligned with governance constraints
- confirm new docs do not overclaim what the system can do

## Commit & Pull Request Guidelines
Use concise, imperative commit messages, for example:
- `Add public governance skeleton`
- `Refine architecture wording`
- `Document interaction boundaries`

Pull requests should summarize:
- purpose of the change
- files touched
- any terminology or boundary changes
- any open questions that still need resolution

## Security & Publication Notes
Do not introduce private notes, local filesystem paths, raw transcripts, or external attribution claims without review. This repo should stay publishable by default.
