# Install dependencies
1. `pip install networkx`

# How to prepare data files
1. `dist{ID}.txt` file: each line contains `x` and `f(x)`, distribution of each
   module
2. `module_relations.txt`: edge list of dependency graph, each line contains `u
   v w` corresponding to a directed edge `u->v` with weight `w`.

# How to run

1. Prepare `dist{ID}.txt` files in `out/` directory
2. Prepare `module_relations.txt` in project root directory
3. Run `$g++ -O2 main.cpp && ./a.out module_relations.txt >result.txt$`
4. Run `$python3 drawer.py$`
