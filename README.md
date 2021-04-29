# ipython-cells

Jupyter for the IPython shell.  Execute commented cells in .py files in the style of Jupyter notebooks without leaving your terminal. Supports Spyder and Jupyter comment syntax.


#### Quickstart

Install the extension

    pip install ipython-cells

`example.py`

``` python
# %% cell1
print('hello')

# %% cell2
print('world')
```

In IPython:

``` python
>>> %load_ext ipython_cells
>>> %load_file example.py
>>> %cell_run cell1
hello
>>> %cell_run cell2
world
```

`example.py` is automatically reloaded when modified by an external editor.


#### Other Features

``` python
%load_file example.py

# list available cells for running
%list_cells
['__first', 'cell1', 'cell2']

# cell ranges - run all cells from beginning of file to cell2 (inclusive)
%cell_run ^cell2
hello
world

# cell ranges - run all cells from cell1 (inclusive) to end of file
%cell_run cell1$
hello
world
```

#### Automatically Load Extension

To load extension on IPython start, add this to `~/.ipython/profile_default/ipython_config.py`

``` python
c.InteractiveShellApp.extensions = [
    'ipython_cells'
]
```

#### Autoreloading
``` python
# load example.py with autoreloading
%load_file example.py

%cell_run cell1
10
# example.py is modified by an external editor (e.g. `a = 10`  ->  `a = 20`)
# File change is detected and automatically reloaded
%cell_run cell1
20

```

Auto reloading can be disabled with `%load_file example.py --noreload`

#### Cell Delimiter Syntax

Cells are delimited by special comments.  Both Jupyter and Spyder style cells are supported.  Below are different variations of a cell called `foobar_cell`.

- `# %% foobar_cell`
- `# In[foobar_cell]`
- `# %% foobar_cell some extra text`
- `# In[foobar_cell] some extra text`

#### Running Exported Jupyter Notebooks

This extension can run exported Jupyter notebooks. (`File > Download As > python (.py)`).

Be sure to run all cells before exporting so they are assigned an index. (`Cell > Run All`).

#### Tests

    cd tests
    ipython3 tests.py
