---
project: The APISSER Methodology for Systematic Literature Reviews in Engineering
author: stefanie castillo
orcid: 0000-0001-8091-0706
upload date: 14 June 2024
---

The APISSER Methodology for Systematic Literature Reviews in Engineering
========================================================================
> by [stefaniecg](mailto:stefaniecg@icloud.com), [ORCID: 0000-0001-8091-0706](https://orcid.org/0000-0001-8091-0706)
  14 June 2024, Innsbruck, Austria

This repository contains the graphical user interface (GUI) used in the case study shown in the paper: The APISSER Methodology for Systematic Literature Reviews in Engineering [1].

Compilation notes:
   - This project is written in [python](https://www.python.org).
   - It uses `tk` and `panda` packages for python.
   - As of June 2024 I couldn't run `tk` and `panda` packages on the latest python which is `python3.12`, thus I had to compile it with `python3.11`.

To run the GUIs for each phase in terminal:
   - _screen & select_ phase: `python3.11 ss_gui.py`
   - _extract_ phase: `python3.11 ex_gui.py`

---------------
# Information about repo

The database contains only one table, please extend as required with more tables.
Each systematic literature review GUI has a folder.

## Projects folders info
   - `./ecs_tiqp/`: The Electronic Control System of a Trapped-Ion Quantum Processor: A Systematic Literature Review [2]

Inside each SLR folder the organization is as follows:

### Files info
   - `ss_gui.py`: screen and select main gui file
   - `ss_lib.py`: library of functions for the `ss_gui` file
   - `ex_gui.py`: extract main gui file
   - `ex_lib.py`: library of functions for the `ex_gui` file
   - `db_lib.py`: library of database related information

### Folders info
   - `./data`: data downloaded from webofscience/scopus and converted to csv format for importing into the database
   - `./db`: location of database
   - `./fig`: figures generated from the data
   - `./rep`: reports generated with the data

---------------
# Licence

CC BY 4.0 - ATTRIBUTION 4.0 INTERNATIONAL [licence info](https://creativecommons.org/licenses/by/4.0/)
   - Attribution — You must give appropriate credit to the author and the paper [1]
   - You are free to:
     * Share — copy and redistribute the material in any medium or format for any purpose, even commercially.
     * Adapt — remix, transform, and build upon the material for any purpose, even commercially.

---------------
# References

[1] S. Castillo et.al, “The APISSER Methodology for Systematic Literature Reviews in Engineering,” IEEE Access, vol. 10, pp. 23700–23707, 2022, doi: [10.1109/ACCESS.2022.3148206](https://doi.org/10.1109/ACCESS.2022.3148206)
[2] S. Castillo, “The Electronic Control System of a Trapped-Ion Quantum Processor: a Systematic Literature Review,” IEEE Access, Jun. 2023, doi: [10.1109/ACCESS.2023.3289936](https://doi.org/10.1109/ACCESS.2023.3289936).
