# Example data for github-actions

This folder holds example data for testing and demonstrating the datamodel, in
three subfolders:

- `valid`: data that conforms to the datamodel, used to verify the datamodel.
- `invalid`: data that does not conform to the datamodel, used to verify the
  validation.
- `problem`: data the current schema version does not yet handle correctly,
  again split into valid and invalid.

Name every example file by the scheme `ClassName-###.yaml`. ClassName is the
name of a class in the schema, written as the schema writes it. "###" can be a
number or one or more other characters allowed in filenames. The ClassName is
derived by splitting at the first "-" and taking the part before the "-".
