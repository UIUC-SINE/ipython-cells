# ipython-cells

IPython extension for executing cells Jupyter-style in .py files.  Supports Jupyter and Spyder cell syntax.

Brings the advantages of linear, selective-execution during development to IPython without the bloat of Jupyter.

#### Example

We can execute the invidual cells in a `.py` file just like a Jupyter notebook.

`example.py`

``` python
# %% cell1
a = 10
print(a)

# %% cell2
a += 1
print(a)
```

In IPython:

``` python

# load the extension and a .py file
%load_ext ipython_cells
%load_file example.py

# run some cells
%cell_run cell1
10
%cell_run cell2
11

# list available cells for running
%list_cells
['__first', 'cell1', 'cell2']
```

#### Installation

``` bash
pip install ipython-cells
```

Optionally, automatically load ipython-cells when IPython starts

`~/.ipython/profile_default/ipython_config.py`
``` python
c.InteractiveShellApp.extensions = [
    'ipython_cells'
]
```

#### Execute a range of cells

``` python
%load_file example.py

# run all cells from beginning of file to cell2 (inclusive)
%cell_run ^cell2
10
11

# run all cells from cell1 (inclusive) to end of file
%cell_run cell1$
12
13
```

#### Autoreloading
``` python
# load example.py with autoreloading
%load_file example.py --autoreload

%cell_run cell1
10
# example.py is modified by an external editor (e.g. `a = 10`  ->  `a = 20`)
# File change is detected and automatically reloaded
%cell_run cell1
20

```

#### Cell Delimiter Syntax

Cells are delimited by special comments.  Both Jupyter and Spyder style cells are supported.

Examples

- `# %% foobar_cell`
- `# In[foobar_cell]`
- `# %% foobar_cell some extra text`
- `# In[foobar_cell] some extra text`
