## Summary

Closes #

## What changed?

- [ ] The converter or the mapping overlay (`scripts/`), and the regenerated schema and artefacts
- [ ] SSSOM mappings (`src/gist/mappings/`), citing the definition on both sides
- [ ] Tests or example data (`tests/`)
- [ ] This repo's own `.lokf/knowledge/` bundle (documentation *about this repo*)
- [ ] Repository packaging only (CI, templates, docs unrelated to the schema)

## Checklist

- [ ] `just test` passes locally
- [ ] Generated files were regenerated with `just gen-project`, not edited by hand
- [ ] Nothing new is defined under `gist:` or `gistd:`
- [ ] If `.lokf/` changed, `cd .lokf && just lokf-validate` passes
- [ ] A behaviour change has an entry under `## [Unreleased]` in `CHANGELOG.md`

## AI Assistance

If you used AI tools while preparing this PR, you are still the author and responsible for understanding, verifying, and defending your submission. Please engage with reviewers personally rather than through your agent during feedback and revisions. Don't dump LLM output into this PR without curation. See the [AI Covenant](../AI_COVENANT.md) for details.
