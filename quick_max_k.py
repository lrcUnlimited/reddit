# -*- coding: UTF-8 -*-
__author__ = 'li'

import random

# 最大的k个数时间,复杂度O(n)

def qselect(A, k):
    if len(A) < k: return qsort(A)
    pivot = A[-1]
    right = [pivot] + [x for x in A[:-1] if x >= pivot]
    rlen = len(right)
    if rlen == k:
        return right
    if rlen > k:
        return qselect(right, k)
    else:
        left = [x for x in A[:-1] if x < pivot]
        return qselect(left, k - rlen) + right


# qucik sort
def qsort(L):
    if len(L) < 2: return L
    pivot_element = random.choice(L)
    small = [i for i in L if i < pivot_element]
    medium = [i for i in L if i == pivot_element]
    large = [i for i in L if i > pivot_element]
    return qsort(small) + medium + qsort(large)

