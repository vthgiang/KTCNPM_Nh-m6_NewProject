# Install dependencies
1. `pip install networkx`

# How to prepare data files
1. `out/dist{ID}.txt` file: each line contains `x` and `f(x)`, distribution of each
   module (identified by module ID), where `x` is the number of days and `f(x)`
   is the probability that the module is finished in exactly `x` days.

   This is the output of old project's java code.
2. `module_relations.txt`: edge list of dependency graph, each line contains `u
   v w` corresponding to a directed edge `u->v` with weight `w`.
3. (Optional) `result_group.txt`, each line describes a group by a list of
   module IDs.

# How to run

1. Prepare `dist{ID}.txt` files in `out/` directory
2. Prepare `module_relations.txt` in project root directory
3. Build ` ./build.sh`
3. Run `./main 3 module_relations.txt`. Here the first param is the limit on
   the number of modules in a group.
4. Run `python3 drawer.py`

# How to customize groups division

1. Modify `result_group.txt`
2. Run `./main 3 module_relations.txt result_group.txt`
3. Run `python3 drawer.py`

