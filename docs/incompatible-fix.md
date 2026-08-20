# IncompatibleWith Rule Fix

## Original Rule 5 Issue

The current rule 5 for `incompatibleWith` documentation is infeasible because:
- JSON files (`templates.json`) do not support inline comments
- The rule instructs to "add a short comment in `templates.json` next to the `incompatibleWith` entry"

## Revised Rule 5

**Document the rationale.** Use alternative documentation methods since JSON cannot contain inline comments:

### Valid Options:

1. **PR Description**: Document collision paths and rationale in the pull request description where the `incompatibleWith` entries are added.

2. **Extension README**: Include the collision rationale in the extension's `README.md` file.

3. **AI_ML_AUTHORING.md**: For AI/ML extensions, add the rationale to the `incompatibleWith` matrix section.

4. **Issue Reference**: Document in the original issue that triggered this incompatibility.

5. **CHANGELOG/NOTES**: Add documentation to a changelog or notes file in the repository.

### Preferred Order:

1. **Primary**: PR description (most discoverable and immediate)
2. **Secondary**: Extension README (useful for users reading about extensions)
3. **Tertiary**: AI_ML_AUTHORING.md (for AI/ML catalog entries)

## Example Documentation

```json
{
  "name": "fastapi-docker",
  "slug": "fastapi-docker",
  "incompatibleWith": ["fastapi-container", "fastapi-k8s"],
  "url": "fastapi-docker/"
}
```

### Documented Rationale (in PR description):

> **Collision paths**: Both `fastapi-docker` and `fastapi-container` ship `Dockerfile` and `compose.yml` overlays for the same FastAPI template type. Selecting both would overwrite the same generated files.
>
> **Resolution**: Users choose one deployment strategy: containerization via Docker Compose or via container runtime integrations.
>
> **Related**: #91, #119

## Checklist Updates

Update the checklist for new `incompatibleWith` entries:

- [ ] Both entries list each other by `slug`
- [ ] Slugs referenced are valid entries in `templates.json`
- [ ] The collision path(s) are documented (see alternatives above)
- [ ] An existing `incompatibleWith` wasn't already covering the pair
- [ ] If a new packaging strategy was introduced, it was discussed in the issue or Discord first
- [ ] Rationale documented using one of the valid methods (PR description, README, etc.)