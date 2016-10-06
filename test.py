import unittest

from discover_dependencies import is_python_file, get_params, remove_quotes, dep_to_drake

class TestIsPython(unittest.TestCase):

    def test_not_python(self):
        self.assertEqual(is_python_file(''), False)
        self.assertEqual(is_python_file('evil.R'), False)

    def test_is_python(self):
        self.assertEqual(is_python_file('nice.py'), True)
        self.assertEqual(is_python_file('nice.zip.py'), True)


class TestGetParams(unittest.TestCase):

    def test_no_params(self):
        self.assertEqual(get_params('odo()'), (None, None))
        self.assertEqual(get_params('temp = odo()'),
                         (None, None))
        self.assertEqual(get_params('temp = odo("only one arg")'),
                         (None, None))

    def test_params(self):
        self.assertEqual(get_params('odo("1", "2")'), ('"1"', '"2"'))
        self.assertEqual(get_params('odo(123, "2")'), ('123', '"2"'))
        self.assertEqual(get_params('odo(param1, param2)'),
                         ('param1', 'param2'))


class TestRemoveQuotes(unittest.TestCase):

    def test_remove_quotes(self):
        self.assertEqual(remove_quotes(''), '')
        self.assertEqual(remove_quotes('hello'), 'hello')
        self.assertEqual(remove_quotes('"hello"'), 'hello')
        self.assertEqual(remove_quotes("'hello'"), 'hello')

class TestDepsToMake(unittest.TestCase):

    def test_normal_case(self):
        dep = (['1.csv', '1.py'], ['2.csv'])
        result = "2.csv<- 1.csv, 1.py\n  python3 1.py"
        self.assertEqual(dep_to_drake('1.py', dep), result)

    def test_several_deps(self):
        dep = (['1.csv', '1.py'], ['2.csv', '3.csv'])
        result = "2.csv<- 1.csv, 1.py\n  python3 1.py"
        result += "\n3.csv<- 1.csv, 1.py\n  python3 1.py"
        self.assertEqual(dep_to_drake('1.py', dep), result)

unittest.main()
