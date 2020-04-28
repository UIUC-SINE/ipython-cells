import unittest
import shutil
from IPython.testing.globalipapp import get_ipython
# from IPython.utils.io import capture_output

class Tests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.ip = get_ipython()
        self.ip.magic('load_ext ipython_cells')
        self.ip.magic('load_file example.py')

    def test_list_cells(self):
        result = self.ip.magic('list_cells')
        self.assertEqual(result, ['__first', 'cell1', 'cell2', 'cell3'])

    def test_run_cells(self):
        global foo

        # test __first
        self.ip.magic('cell_run __first')
        self.assertEqual(foo, 1)

        # test caret syntax
        foo = 0
        self.ip.magic('cell_run ^cell1')
        self.assertEqual(foo, 1)

        # test dollar syntax
        foo = 0
        self.ip.magic('cell_run cell2$')
        self.assertEqual(foo, 5)

        # test multi cell running
        foo = 0
        self.ip.magic('cell_run cell2 cell3')
        self.assertEqual(foo, 5)

        # ----- test autoreloading -----

        shutil.copy('example.py', 'tmp_example.py')
        self.ip.magic('load_file tmp_example.py')
        self.ip.magic('cell_run cell1')
        self.assertEqual(foo, 1)

        # test that modified cell is run
        shutil.copy('example_edited.py', 'tmp_example.py')
        self.ip.magic('cell_run cell1')
        self.assertEqual(foo, 2)

if __name__ == '__main__':
    unittest.main()
