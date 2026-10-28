# Example data for github-actions

This folder contains example data for testing and demonstrating the datamodel,
sorted in subfolders:

- `valid` for data conforming to the datamodel. Used to verify the datamodel.
- `invalid` for data not conforming to the datamodel. Used to verify the validation.
- `problem` for data which are not yet handled correctly in the current schema version,
   again separated into valid/invalid.

The filenames of all example data must conform to the scheme `ClassName-###.yaml`
where ClassName must be the name of a class from the schema, as it is written there. "###" can be a number
or one or more other characters allowed in filenames. The ClassName is derived by
splitting at the first "-" and taking the part before the "-".
