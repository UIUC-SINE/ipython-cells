from IPython.core.getipython import get_ipython
from IPython.core.magic import (Magics, magics_class, line_magic)
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)
from logging import error
from os.path import getmtime
from collections import OrderedDict
import re

@magics_class
class IPythonCells(Magics):

    filename = None

    @line_magic
    @magic_arguments()
    @argument('filename', type=str, help='path to file')
    @argument('--noreload', action='store_true', default=False, help='dont automatically reload cells when file changes')
    def load_file(self, args_str):
        """Load a .py file for use with %cell_run"""

        args = parse_argstring(self.load_file, args_str)
        self.filename = args.filename
        self.noreload = args.noreload

        self.load_cells()

    def load_cells(self):
        """Read the given file and generate an ordered dictionary with the keys as
        the cell names and values as the list of line strings in that cell.

        The cell indicator is taken as '# %%' character.
        """

        file = open(self.filename, "r")
        f = file.readlines()
        self.cells = OrderedDict()

        # put all code above the first cell comment into a cell called __first
        cell_name = '__first'
        self.cells[cell_name] = ''

        # loop lines in filename and create cells dictionary
        for line in f:

            # handle spyder and jupyter styles
            jupyter_match = re.match('^#\sIn\[([^\]]+)\]', line)
            spyder_match = re.match('^#\s?%%\s?(\S+)', line)
            if jupyter_match is not None:
                cell_name = jupyter_match.group(1)
                self.cells[cell_name] = ''
            elif spyder_match is not None:
                cell_name = spyder_match.group(1)
                self.cells[cell_name] = ''

            self.cells[cell_name] += line

        self.load_time = getmtime(self.filename)
        self.shell.set_hook('complete_command', self.cell_run_complete, re_key='%cell_run')

    @line_magic
    @magic_arguments()
    @argument('cell_names', nargs='*', type=str, help='name of cell to run')
    # @argument('variable_overrides', nargs='*', type=str, help='override variable when running')
    def cell_run(self, args_str):
        """Run a specific cell in the loaded py file"""

        if self.filename is None:
            error("No file loaded.  Use %load_file to load a .py file")
            return

        if not self.noreload and self.load_time < getmtime(self.filename):
            self.load_cells()

        args = parse_argstring(self.cell_run, args_str)

        for arg in args.cell_names:

            cell_name = arg.lstrip('^').rstrip('$')
            to_first = arg.startswith('^')
            to_last = arg.endswith('$')

            # execute cell or cell range
            if cell_name in self.cells.keys():
                # for variable in args.variable_overrides:
                #     self.shell.ex(variable)

                index = list(self.cells.keys()).index(cell_name)

                if to_first:
                    cells = list(self.cells.values())[0:index + 1]
                elif to_last:
                    cells = list(self.cells.values())[index:]
                else:
                    cells = [self.cells[cell_name]]

                for cell in cells:
                    self.shell.run_cell(cell)
            else:
                error('No such cell {} found in {}'.format(
                    cell_name,
                    self.filename
                ))
                return

    @line_magic
    def list_cells(self, args):
        """Return a list of loaded cells"""

        if hasattr(self, 'cells'):
            return list(self.cells.keys())
        else:
            error("No file loaded.  Use %load_file to load a .py file")

    def cell_run_complete(self, foo, event):
        """Autocomplete for %cell_run"""

        return list(self.cells.keys())


def load_ipython_extension(ip):
    """Load the extension in IPython."""

    ip.register_magics(IPythonCells)

if __name__ == "__main__":
    load_ipython_extension(get_ipython())
