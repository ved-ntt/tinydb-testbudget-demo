# TestBudget on TinyDB

This repository is a copy of [TinyDB](https://github.com/msiemens/tinydb) (MIT licence) used to demonstrate
[TestBudget](https://github.com/ssbajjur-ncstate/SE-CSC-510-Group-9), a CSC 510 Group 9 project, in a real CI setup.

The only additions are `.github/workflows/testbudget.yml` and the `.testbudget/` folder. TinyDB's own CI and
publish workflows were removed so they do not run here.

## How it works

- **Every push to `master`** runs the full test suite, records each test's result and duration in TestBudget's
  history, and caches that history for later runs.
- **Every pull request**:
  1. builds links from each test to the TinyDB files it imports;
  2. reads the files the pull request changed;
  3. asks TestBudget for a plan within a budget of 30% of the suite's recorded test time;
  4. posts the plan as a `TestBudget` check run and a job summary;
  5. runs only the planned tests, in plan order, through TestBudget's pytest plugin.

## Seed history

`.testbudget/` starts with two runs so TestBudget has something to learn from: one clean run, and one run where a
deliberately seeded bug in `tinydb/queries.py` made a test fail. Runs on `master` add to this history through the
Actions cache.
