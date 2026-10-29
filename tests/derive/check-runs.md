# Checks on 0123456789ab in example-org/repo

The check runs and commit statuses GitHub recorded on `feature` in example-org/repo, as its REST API (version 2026-03-10) returns them. `scripts/github_export.py check-runs` printed this, and `scripts/derive.py --check-runs` reads the JSON below.

```json
{
  "api_version": "2026-03-10",
  "check_runs": [
    {
      "app_id": 4242,
      "app_slug": "other-ci",
      "conclusion": "success",
      "name": "Build the docs",
      "status": "completed"
    },
    {
      "app_id": 15368,
      "app_slug": "github-actions",
      "conclusion": "skipped",
      "name": "label",
      "status": "completed"
    },
    {
      "app_id": 15368,
      "app_slug": "github-actions",
      "conclusion": "skipped",
      "name": "lint",
      "status": "completed"
    },
    {
      "app_id": 15368,
      "app_slug": "github-actions",
      "conclusion": "success",
      "name": "unit / pytest",
      "status": "completed"
    }
  ],
  "ref": "feature",
  "repository": "example-org/repo",
  "sha": "0123456789abcdef0123456789abcdef01234567",
  "statuses": [
    {
      "context": "external / scan",
      "state": "success"
    }
  ]
}
```
