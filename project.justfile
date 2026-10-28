## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

# ============ The merged schema for the docs site ============

# `just gen-doc` writes docs/schema/github_actions.yaml with the modules'
# elements folded in but the `imports:` list kept, so a tool that loads it
# looks for the modules beside it. This file has no imports at all: the one to
# vendor or load offline. Run it after gen-doc.
[group('model development')]
gen-merged:
  uv run gen-linkml --mergeimports -f yaml {{source_schema_path}} > docs/schema/{{schema_name}}_merged.yaml
