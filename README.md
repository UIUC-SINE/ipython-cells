# ipython-cells

iPython extension for executing cells Jupyter-style in .py files.  Supports Jupyter and Spyder cell syntax.

Brings the advantages of linear, selective-execution during development to iPython without the bloat of Jupyter.

## Example

Suppose we have a .py exported by Jupyter.

`example.py`

``` python
# %% cell1
a = 10
print(a)

# %% cell2
a += 1
print(a)
```

In ipython:

``` python

# load the extension
%load_ext ipython_cells

# load example.py and run a cell
%load_file example.py
%cell_run cell1
10

# load example.py with autoreloading
%load_file example.py --autoreload
%cell_run cell1
10
# example.py is modified by an external editor (e.g. `a = 10`  ->  `a = 20`)
# we detect that and automatically reload the cells
%cell_run cell1
20

# run all cells from beginning of file to cell2 (inclusive)
%cell_run ^cell2
10
11

# run all cells from cell1 (inclusive) to end of file
%cell_run cell1$
12
13

%list_cells
['__first', 'cell1', 'cell2']
```

## Installation

``` bash
pip install ipython-cells
```

Optionally, automatically load ipython-cells when ipython starts

`~/.ipython/profile_default/ipython_config.py`
``` python
c.InteractiveShellApp.extensions = [
    'ipython_cells'
]
```
