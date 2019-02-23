# ipython-cells

This repo contains the codes for bringing Jupyter-like cell functionality to ipython.

## Example

Suppose we have a .py file with cells separated by user created comments

`example.py`

``` python
# %% cell1
a = 10

# %% cell2
a += 1
print(a)
```

In ipython:

``` python

# load the extension
%run ipython_cells.py

# load example.py with autoreloading enabled
%load_file example.py --autoreload

# simple cell running
%cell_run cell1
%cell_run cell2
11
%cell_run cell2
11

# override variables
%cell_run cell2 a=100
101

# example.py is modified by an external editor (e.g. `a += 1`  ->  `a += 2`)
# we detect that and automatically reload the cells
%cell_run cell2
103
```
