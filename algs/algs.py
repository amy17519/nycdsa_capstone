__author__ = "Shu Yan"


def insertion_sort(L):

    """insertion sort"""

    L = L[:]
    for i in range(1, len(L)):
        for j in range(0, i)[::-1]:
            if L[j] > L[j+1]:
                L[j], L[j+1] = L[j+1], L[j]
                j -= 1
            else:
                break
    return L


def selection_sort(L):

    """selection sort"""

    L = L[:]
    for i in range(len(L))[::-1]:
        max_idx = 0
        for j in range(1, i):
            if L[max_idx] < L[j]:
                max_idx = j
        if L[max_idx] > L[i]:
            L[i], L[max_idx] = L[max_idx], L[i]
    return L


def merge_sort(L):

    """merge sort"""

    # define an inner function merge(): merges two sorted list into one
    def merge(l1, l2):
        merged = []
        i, j = 0, 0
        while i < len(l1) and j < len(l2):
            if l1[i] > l2[j]:
                merged.append(l2[j])
                j += 1
            else:
                merged.append(l1[i])
                i += 1
        return merged + l1[i:] + l2[j:]

    L = L[:]
    if len(L) > 1:
        mid = len(L) / 2
        # divide list with 2 or more items into two sub-lists
        left, right = L[:mid], L[mid:]
        # sort the two sub-lists individually
        left = merge_sort(left)
        right = merge_sort(right)
        # merge the two sorted sub-lists
        return merge(left, right)
    else:
        return L


def quick_sort(L):

    """quick sort"""

    # sort helper function
    def sort(L, start, end):
        if end > start:
            pivot = partition(L, start, end)
            sort(L, start, pivot - 1)
            sort(L, pivot + 1, end)

    # partition the sub-list L[lo:hi] so that L[lo:j - 1] <= L[j] <= L[j + 1:hi] and return the index j
    def partition(L, start, end):
        i, j = start + 1, end
        while True:
            while L[i] <= L[start]:
                i += 1
                if i > end:
                    break
            while L[j] > L[start]:
                j -= 1
                if j < start + 1:
                    break
            if i > j:
                break
            L[i], L[j] = L[j], L[i]
        L[start], L[j] = L[j], L[start]
        return j

    L = L[:]
    sort(L, 0, len(L) - 1)
    return L


def linear_search(L, val):
    for k, v in enumerate(L):
        if v == val:
            return k
    return -1


def binary_search(L, val):
    if len(L) == 0:
        return -1
    i, j = 0, len(L) - 1
    while i <= j:
        mid = (i + j) / 2
        if val > L[mid]:
            i = mid + 1
        elif val < L[mid]:
            j = mid - 1
        else:
            while mid > 0 and L[mid] == L[mid - 1]:
                mid -= 1
            return mid
    return -1


class HashMap(object):

    def __init__(self, capacity=16):
        self.__size = capacity
        self.__keys = [None] * self.__size
        self.__vals = [None] * self.__size
        self.__length = 0

    def __setitem__(self, key, value):
        idx = hash(key) % self.__size
        while self.__keys[idx] is not None:
            if key == self.__keys[idx]:
                break
            idx += 1
            idx %= self.__size
        if self.__length > self.__size * .75:
            self.__resize(2)
        self.__keys[idx] = key
        self.__vals[idx] = value
        self.__length += 1

    def __getitem__(self, key):
        idx = hash(key) % self.__size
        while self.__keys[idx] is not None:
            if key == self.__keys[idx]:
                return self.__vals[idx]
            idx += 1
            idx %= self.__size
        raise KeyError(0)

    def __delitem__(self, key):
        idx = hash(key) % self.__size
        while self.__keys[idx] is not None:
            if key == self.__keys[idx]:
                self.__keys[idx] = None
                self.__vals[idx] = None
                self.__length -= 1
                if self.__length < self.__size * .25:
                    self.__resize(.5)
                return
            idx += 1
            idx %= self.__size
        raise KeyError(0)

    def __resize(self, n):
        if n > 1 or self.__size > 16:
            newmap = HashMap(capacity=int(self.__size*n))
            for k in self:
                newmap[k] = self[k]
            self.__size = newmap.__size
            self.__keys = newmap.__keys
            self.__vals = newmap.__vals
        return

    def __iter__(self):
        for i in self.__keys:
            if i is not None:
                yield i

    def __len__(self):
        return self.__length

    def __str__(self):
        pairs = filter(lambda a: a[0] is not None, zip(self.__keys, self.__vals))
        return '{' + ', '.join(map(lambda x: ' : '.join(map(str, x)), pairs)) + '}'


if __name__ == "__main__":
    hm = HashMap()

    print "try add"

    for i in range(20)[::-1]:
        hm[i] = i * 2
        print i, len(hm)

    print "try del"


    for i in range(20):
        del hm[i]
        print i, len(hm)


    for k in hm:
        print k, hm[k]

