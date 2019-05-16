import unittest
import shutil
from IPython.testing.globalipapp import get_ipython
from IPython.utils.io import capture_output

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
        foo = 0
        foo_compare = 0

        # test caret syntax
        self.ip.magic('cell_run ^cell1')
        foo_compare += 2
        self.assertEqual(foo, foo_compare)

        # test dollar syntax
        self.ip.magic('cell_run cell2$')
        foo_compare += 5
        self.assertEqual(foo, foo_compare)

        # test single cell running
        self.ip.magic('cell_run cell3')
        foo_compare += 3
        self.assertEqual(foo, foo_compare)

        # ----- test autoreloading -----
        foo = 0
        foo_compare = 0

        shutil.copy('example.py', 'tmp_example.py')
        self.ip.magic('load_file tmp_example.py --autoreload')
        self.ip.magic('cell_run cell1')
        foo_compare += 1
        self.assertEqual(foo, foo_compare)

        # test that modified cell is run
        shutil.copy('example_edited.py', 'tmp_example.py')
        self.ip.magic('cell_run cell1')
        foo_compare += 2
        self.assertEqual(foo, foo_compare)

if __name__ == '__main__':
    unittest.main()
