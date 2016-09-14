import timeit
import random
import unittest
import matplotlib.pyplot as plt



__author__ = "Shu Yan"


class SortingTest(unittest.TestCase):

    def __init__(self, func):
        super(SortingTest, self).__init__('sorting_test')
        self.func = func

    def sorting_test(self):
        for i in range(1, 8):
            m = int(random.random() * 2 ** i)
            n = int(random.random() * 4 ** i)
            test_list = [random.randint(-m, m) for x in xrange(n)]
            self.assertListEqual(sorted(test_list), self.func(test_list))
            print "test:{0}  length:{1}".format(i, n)


class SearchingTest(unittest.TestCase):

    def __init__(self, func):
        super(SearchingTest, self).__init__('run_test')
        self.func = func

    def run_test(self):
        for i in range(9):
            n = int(random.random() * 4 ** i)
            test_list = sorted([random.randint(0, 2**i) for x in xrange(n)])
            val = random.randint(0, 2**i)
            try:
                idx = test_list.index(val)
            except ValueError:
                idx = -1
            self.assertEqual(idx, self.func(test_list, val))
            print 'test:{0}  length:{1}  search:{2}  index:{3}'.format(i+1, n, val, idx)


def func_timer(func, *args, **kwargs):

    """test function running time"""

    def test():
        func(*args, **kwargs)
    return timeit.timeit(test, number=5) / 5


def sort_timer(func):

    """test sorting algorithms"""
    
    def test():
        func(my_list)
    
    for i in xrange(1, 10):
        my_list = [random.randint(0, 1000) for x in xrange(1000*i)]
        print '{0} : {1}'.format(i, timeit.timeit(test, number=1))