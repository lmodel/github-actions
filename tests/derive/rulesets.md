# Rulesets of example-org/repo

The rulesets of example-org/repo, and the rules in effect on its default branch `main`, as GitHub's REST API (version 2026-03-10) returns them. `scripts/github_export.py rulesets` printed this, and `scripts/derive.py --rulesets` reads the JSON below.

```json
{
  "api_version": "2026-03-10",
  "branch_rules": [
    {
      "ruleset_id": 101,
      "ruleset_source": "example-org/repo",
      "ruleset_source_type": "Repository",
      "type": "deletion"
    },
    {
      "parameters": {
        "do_not_enforce_on_create": false,
        "required_status_checks": [
          {
            "context": "unit / pytest",
            "integration_id": 15368
          },
          {
            "context": "label / ruff",
            "integration_id": 15368
          },
          {
            "context": "external / scan",
            "integration_id": 9999
          }
        ],
        "strict_required_status_checks_policy": true
      },
      "ruleset_id": 101,
      "ruleset_source": "example-org/repo",
      "ruleset_source_type": "Repository",
      "type": "required_status_checks"
    }
  ],
  "default_branch": "main",
  "repository": "example-org/repo",
  "rulesets": [
    {
      "_links": {
        "self": {
          "href": "https://api.github.com/repos/example-org/repo/rulesets/101"
        }
      },
      "bypass_actors": [
        {
          "actor_id": 5,
          "actor_type": "RepositoryRole",
          "bypass_mode": "pull_request"
        }
      ],
      "conditions": {
        "ref_name": {
          "exclude": [],
          "include": [
            "~DEFAULT_BRANCH"
          ]
        }
      },
      "enforcement": "active",
      "id": 101,
      "name": "main",
      "rules": [
        {
          "type": "deletion"
        },
        {
          "parameters": {
            "do_not_enforce_on_create": false,
            "required_status_checks": [
              {
                "context": "unit / pytest",
                "integration_id": 15368
              },
              {
                "context": "label / ruff",
                "integration_id": 15368
              },
              {
                "context": "external / scan",
                "integration_id": 9999
              }
            ],
            "strict_required_status_checks_policy": true
          },
          "type": "required_status_checks"
        }
      ],
      "source": "example-org/repo",
      "source_type": "Repository",
      "target": "branch"
    },
    {
      "_links": {
        "self": {
          "href": "https://api.github.com/repos/example-org/repo/rulesets/202"
        }
      },
      "conditions": {
        "ref_name": {
          "exclude": [],
          "include": [
            "~ALL"
          ]
        }
      },
      "enforcement": "evaluate",
      "id": 202,
      "name": "docs trial",
      "rules": [
        {
          "parameters": {
            "do_not_enforce_on_create": true,
            "required_status_checks": [
              {
                "context": "Build the docs"
              }
            ],
            "strict_required_status_checks_policy": false
          },
          "type": "required_status_checks"
        }
      ],
      "source": "example-org",
      "source_type": "Organization",
      "target": "branch"
    }
  ]
}
```
