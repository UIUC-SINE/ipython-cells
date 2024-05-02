from IPython.core.getipython import get_ipython
from IPython.core.magic import (Magics, magics_class, line_magic)
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)
from logging import error
from os.path import getmtime
from collections import OrderedDict
import re
import sys

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

        with open(self.filename, 'r') as f:
            lines = f.readlines()

        self.cells = OrderedDict()
        self.line_nums = {}

        # put all code above the first cell comment into a cell called __first
        cell_name = '__first'
        self.cells[cell_name] = ''
        self.line_nums[cell_name] = 0

        # loop lines in filename and create cells dictionary
        for line_num, line in enumerate(lines, 1):

            # handle spyder and jupyter styles
            jupyter_match = re.match('^\s*#\sIn\[([^\]]*)\]', line)
            spyder_match = re.match('^\s*#\s?%%\s?(\S*)', line)
            if jupyter_match is not None:
                cell_name = jupyter_match.group(1)
                self.cells[cell_name] = ''
                self.line_nums[cell_name] = line_num
            elif spyder_match is not None:
                cell_name = spyder_match.group(1)
                self.cells[cell_name] = ''
                self.line_nums[cell_name] = line_num

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

        concatenated = ''
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
                    # prepend newlines so snippet line num matches file line num
                    #cell = '\n' * index + cell
                    # change traceback filename
                    #code = compile(cell, self.filename, 'exec')
                    # code = '\n' * self.line_nums[cell_name] + cell
                    # code = '#\n\n\n\nraise Exception\n'
                    # print('line_nums:', self.line_nums[cell_name])
                    # print('-----------')
                    # print(code)
                    # print('-----------')
                    # self.shell.run_cell(code)
                    # self.shell.run_cell(cell)
                    concatenated += cell
            else:
                error('No such cell {} found in {}'.format(
                    cell_name,
                    self.filename
                ))
                return

        self.shell.run_cell(concatenated)

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

def fake_traceback(exc_value, tb, filename, lineno):
    """Produce a new traceback object that looks like it came from the
    template source instead of the compiled code. The filename, line
    number, and location name will point to the template, and the local
    variables will be the current template context.
    :param exc_value: The original exception to be re-raised to create
        the new traceback.
    :param tb: The original traceback to get the local variables and
        code info from.
    :param filename: The template filename.
    :param lineno: The line number in the template source.
    """
    if tb is not None:
        # Replace the real locals with the context that would be
        # available at that point in the template.
        locals = get_template_locals(tb.tb_frame.f_locals)
        locals.pop("__jinja_exception__", None)
    else:
        locals = {}

    globals = {
        "__name__": filename,
        "__file__": filename,
        "__jinja_exception__": exc_value,
    }
    # Raise an exception at the correct line number.
    code = compile("\n" * (lineno - 1) + "raise __jinja_exception__", filename, "exec")

    # Build a new code object that points to the template file and
    # replaces the location with a block name.
    try:
        location = "template"

        if tb is not None:
            function = tb.tb_frame.f_code.co_name

            if function == "root":
                location = "top-level template code"
            elif function.startswith("block_"):
                location = f"block {function[6:]!r}"

        # Collect arguments for the new code object. CodeType only
        # accepts positional arguments, and arguments were inserted in
        # new Python versions.
        code_args = []

        for attr in (
            "argcount",
            "posonlyargcount",  # Python 3.8
            "kwonlyargcount",
            "nlocals",
            "stacksize",
            "flags",
            "code",  # codestring
            "consts",  # constants
            "names",
            "varnames",
            ("filename", filename),
            ("name", location),
            "firstlineno",
            "lnotab",
            "freevars",
            "cellvars",
            "linetable",  # Python 3.10
        ):
            if isinstance(attr, tuple):
                # Replace with given value.
                code_args.append(attr[1])
                continue

            try:
                # Copy original value if it exists.
                code_args.append(getattr(code, "co_" + attr))
            except AttributeError:
                # Some arguments were added later.
                continue

        code = CodeType(*code_args)
    except Exception:
        # Some environments such as Google App Engine don't support
        # modifying code objects.
        pass

    # Execute the new code, which is guaranteed to raise, and return
    # the new traceback without this frame.
    try:
        exec(code, globals, locals)
    except BaseException:
        return sys.exc_info()[2].tb_next
