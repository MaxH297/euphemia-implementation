# euphemia-implementation

Mathematical Formulation of implemented clearing mechanism: https://github.com/MaxH297/euphemia-implementation/blob/main/implementation_clearing_model.pdf

Implementation with Gurobi Solver: https://www.gurobi.com/

Steps:
- Place orders in orders/ folder. Structure based on data provided by Epex Spot: https://www.epexspot.com/en
- Add dates to be considered in dates.csv
- run run_euphemia.py

Output from conversion mechanism for examples introduced in paper is put in input/ folder, with a respective run_xy.py file performing tests.
