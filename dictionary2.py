import unittest

class CustomDict(dict):
    def __init__(self, *args, **kwargs):

        super(CustomDict, self).__init__({k:CustomDict(i) if type(i)==dict else i for k, i in dict(*args, **kwargs).items()})
        self.__dict__['__dict_keys__'] = list(self.keys())
        self.__dict__['__changes__'] = {}

    def __setitem__(self, key, item):
        if type(item) == dict:
            item = CustomDict(item)
        super(CustomDict, self).__setitem__(key, item)
        self.__dict__['__changes__'][key] = item

    def __delitem__(self, key):
        super(CustomDict, self).__delitem__(key)
        if key in self.__dict__['__dict_keys__']:
            self.__dict__['__changes__'][key] = None
        else:
            del self.__dict__['__changes__'][key]

    def update(self, *args, **kwargs):

        for k, v in dict(*args, **kwargs).items():
            self.__dict__['__changes__'].__setitem__(k, v)
            self.__setitem__(k, v)

    def pop(self, key):
        if key in self.__dict__['__dict_keys__']:
            self.__dict__['__changes__'][key] = None
        else:
            del self.__dict__['__changes__'][key]
        return super(CustomDict, self).pop(key)

    def clear(self):
        self.__dict__['__changes__'] = {i:None for i in self.__dict__['__dict_keys__']}
        return super(CustomDict, self).clear()

    def changes(self):
        changes_results = {}

        for k, v in self.items():
            key_changes = self.__dict__['__changes__'].get(k)
            if type(v) == CustomDict:
                if not key_changes:
                    key_changes = v.changes()

            if key_changes:
                changes_results[k] = key_changes

        for i in self.__dict__['__dict_keys__']:
            if i not in self.keys() and i not in changes_results.keys():
                changes_results[i] = None

        return changes_results

# unittests

class TestComparasion(unittest.TestCase):
    def setUp(self):
        self.data = CustomDict({'a':{'a1':1,'a2':2},'b':{'b1':{'b11':1,'b12':2}}})

    def test_init(self):
        res = {}
        c_res = self.data.changes()

        self.assertEqual(res, c_res)

    def test_setitem(self):
        self.data['a']['a1'] = 3
        self.data['b']['b1']['b11'] = 5

        res =  {'a':{'a1':3},'b':{'b1':{'b11':5}}}
        c_res = self.data.changes()

        self.assertEqual(res, c_res)

    def test_delitem(self):
        del self.data['b']

        res =  {'b': None}
        c_res = self.data.changes()

        self.assertEqual(res, c_res)

    def test_update(self):
        self.data = CustomDict()
        self.data.update({'a':{'a1':1,'a2':2},'b':{'b1':{'b11':1,'b12':2}}})
        res = {'a':{'a1':1,'a2':2},'b':{'b1':{'b11':1,'b12':2}}}

        c_res = self.data.changes()

        self.assertEqual(res, c_res)

    def test_pop(self):
        self.data.pop('b')
        res = {'b': None}

        c_res = self.data.changes()

        self.assertEqual(res, c_res)

    def test_clear(self):
        self.data.clear()
        res = {'a': None, 'b': None}

        c_res = self.data.changes()

        self.assertEqual(res, c_res)

#run
if __name__ == '__main__':
    unittest.main()
