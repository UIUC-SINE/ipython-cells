from IPython.core.magic import (Magics, magics_class, line_magic)
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)
from logging import error
from os.path import getmtime

@magics_class
class IPythonCells(Magics):

    filename = None

    @line_magic
    @magic_arguments()
    @argument('filename', type=str, help='path to file')
    @argument('--autoreload', action='store_true', default=False, help='automatically reload cells when file changes')
    def load_file(self, args_str):
        """Load a .py file for use with %cell_run"""
        args = parse_argstring(self.load_file, args_str)
        self.filename = args.filename
        self.autoreload = args.autoreload

        self.load_cells()

    def load_cells(self):
        self.cells = {
            'foo': ['print(\'hello world!!!!!\')', 'a=456', 'print(b)']
        }
        self.load_time = getmtime(self.filename)


    @line_magic
    @magic_arguments()
    @argument('cell_name', type=str, help='name of cell to run')
    @argument('variable_overrides', nargs='*', type=str, help='override variable when running')
    def cell_run(self, args_str):
        """Run a specific cell in the loaded py file"""

        if self.filename is None:
            error("No file loaded.  Use %load_file to load a .py file")
            return

        if self.autoreload and self.load_time < getmtime(self.filename):
            self.load_cells()

        args = parse_argstring(self.cell_run, args_str)

        if args.cell_name in self.cells.keys():
            for variable in args.variable_overrides:
                self.shell.ex(variable)

            self.shell.run_cell('\n'.join(self.cells[args.cell_name]))
        else:
            error('No such cell {} found in {}'.format(
                args.cell_name,
                self.loaded
            ))

ip = get_ipython()
ip.register_magics(IPythonCells)
