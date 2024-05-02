import unittest
import shutil
from IPython.testing.globalipapp import get_ipython
# from IPython.utils.io import capture_output

class Tests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.ip = get_ipython()
        self.ip.run_line_magic('load_ext', 'ipython_cells')
        self.ip.run_line_magic('load_file', 'example.py')

    def test_list_cells(self):
        result = self.ip.run_line_magic('list_cells', None)
        self.assertEqual(result, ['__first', 'cell1', 'cell2', 'cell3', '', 'cell4'])

    def test_run_cells(self):
        # test __first
        self.ip.run_line_magic('cell_run', '__first')
        self.assertEqual(self.ip.user_ns['foo'], 1)

        # test caret syntax
        self.ip.user_ns['foo'] = 0
        self.ip.run_line_magic('cell_run', '^cell1')
        self.assertEqual(self.ip.user_ns['foo'], 1)

        # test dollar syntax
        self.ip.user_ns['foo'] = 0
        self.ip.run_line_magic('cell_run', 'cell2$')
        self.assertEqual(self.ip.user_ns['foo'], 9)

        # test multi cell running
        self.ip.user_ns['foo'] = 0
        self.ip.run_line_magic('cell_run', 'cell3 cell3')
        self.assertEqual(self.ip.user_ns['foo'], 6)

        # ----- test autoreloading -----

        self.ip.user_ns['foo'] = 0
        shutil.copy('example.py', 'tmp_example.py')
        self.ip.run_line_magic('load_file', 'tmp_example.py')
        self.ip.run_line_magic('cell_run', 'cell1')
        self.assertEqual(self.ip.user_ns['foo'], 1)

        # test that modified cell is run
        shutil.copy('example_edited.py', 'tmp_example.py')
        self.ip.run_line_magic('cell_run', 'cell1')
        self.assertEqual(self.ip.user_ns['foo'], 2)

if __name__ == '__main__':
    unittest.main()
