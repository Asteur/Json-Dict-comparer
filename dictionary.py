import unittest


class Comparasion:

    def __init__(self, d1, d2):
        self.d1 = d1
        self.d2 = d2

    def compare_dict(self):
        res = {}
        keys = list(self.d1.keys() | self.d2.keys())
        try:
            keys = sorted(keys)
        except Exception:
            pass
        for k in keys:
            eq_k = self.d1.get(k) == self.d2.get(k)
            if not eq_k:
                if isinstance(self.d1.get(k), dict) and isinstance(self.d2.get(k), dict):
                    C2 = Comparasion(self.d1.get(k), self.d2.get(k))
                    res[k] = C2.compare_dict()
                else:
                    res[k] = self.d2.get(k)
        return res

class TestComparasion(unittest.TestCase):
    def setUp(self):
        self.data = {'a':{'a1':1,'a2':2},'b':{'b1':{'b11':1,'b12':2}}}

    def test_init(self):
        res = {}

        c = Comparasion(self.data, self.data)
        c_res = c.compare_dict()

        self.assertEqual(res, c_res)

    def test_setitem(self):
        import copy
        data = copy.deepcopy(self.data)

        data['a']['a1'] = 3
        data['b']['b1']['b11'] = 5
        res =  {'a':{'a1':3},'b':{'b1':{'b11':5}}}

        c = Comparasion(self.data, data)
        c_res = c.compare_dict()

        self.assertEqual(res, c_res)

    def test_delitem(self):
        import copy
        data = copy.deepcopy(self.data)
        del data['b']

        res =  {'b': None}

        c = Comparasion(self.data, data)
        c_res = c.compare_dict()

        self.assertEqual(res, c_res)

    def test_update(self):
        data = {}
        res = {'a':{'a1':1,'a2':2},'b':{'b1':{'b11':1,'b12':2}}}

        c = Comparasion(data, self.data)
        c_res = c.compare_dict()

        self.assertEqual(res, c_res)


if __name__ == '__main__':
    unittest.main()
