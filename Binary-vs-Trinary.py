#-------------------------------------------------------------------------------
"""
    Purpose: To test the complexities of a binary and trinary search. Simply
             run the program to see the results. Preset values: 5 lists
             with different lengths (n), and 3 values for k, per experiment.
             Values use constant k for ALL lists, then will redo the experiment
             with a new k-value (change of divisibility of n). All sizes
             of n have been hardcoded and can be changed on lines 24. Values
             of k will be decided within the 'd' list, found on line 29.
"""
#-------------------------------------------------------------------------------

import time, random

def main():
    n = [50000, 75000, 100000, 500000, 10000000]
    statements = ["--- BINARY SEARCH ---", "--- TRINARY SEARCH ---", \
                  "--- BINARY SEARCH (not in list) ---", \
                  "---TRINARY SEARCH (not in list) ---"]
    lists = []
    d = [10, 5, 2]

    print 'Sorting lists...\n'

    for i in range(len(n)):
        lists.append(randomList(n[i]))
        qsort(lists[i])

    print 'Begin search\n'

    for m in range(len(d)):
        size = n[0]/d[m]

        for i in range(4):
            k = defineK(lists[i], i, size, n)

            print statements[i]

            for j in range(len(n)):
                if i % 2 == 0:  #Binary
                    search(lists[j], k, i)
                else:           #Trinary
                    search(lists[j], k, i)
            print ""

def bin_search(A, first, last, target):
    #returns index of target in A, if present
    #returns -1 if target is not present in A

    if first > last:
        return -1
    else:
        mid = (first + last)/2

        if A[mid] == target:
            return mid
        elif A[mid] > target:
            return bin_search(A, first, mid-1, target)
        else:
            return bin_search(A, mid+1, last, target)

def trin_search(A, first, last, target):
    #returns index of target in A, if present
    #returns -1 if target is not present in A

    if first > last:
        return -1
    else:
        one_third = first + (last - first)/3
        two_thirds = first + 2*(last - first)/3

    if A[one_third] == target:
        return one_third
    elif A[one_third] > target:
        #search the left-hand third
        return trin_search(A, first, one_third-1, target)
    elif A[two_thirds] == target:
        return two_thirds
    elif A[two_thirds] > target:
        #search the middle third
        return trin_search(A, one_third+1, two_thirds-1, target)
    else:
        #search the right-hand third
        return trin_search(A, two_thirds+1, last, target)

def qsort(lis, lowIndex=0, highIndex=None):
    """
    An in-place version of quick sort.  Sorts lis[lowIndex:highIndex+1] in
    place.  If highIndex is None, we use the highest index in the list.
    No return value.
    """
    if highIndex == None:
        highIndex = len(lis)-1
    if lowIndex >= highIndex:
        # list segment has 0 or 1 elements, already sorted
        return

    # swap the middle value into the first position in the list to use
    # as the partition value, to avoid worst-case behavior
    midIndex = (lowIndex+highIndex)//2
    lis[lowIndex],lis[midIndex] = lis[midIndex],lis[lowIndex]
    pval = lis[lowIndex]
    # indexes i and j divide A into sections.  The invariant is:
    #   lis[lowIndex] == pval
    #   if lowIndex<index<=i: lis[lowIndex] < pval
    #   if i<index<=j: lis[lowIndex] >= pval
    i = lowIndex
    j = lowIndex
    while j < highIndex:
        j += 1
        if lis[j] < pval:
            # swap this value into the section that is < pval
            i += 1
            lis[i],lis[j] = lis[j],lis[i]
    # swap the partition value into its proper position
    lis[lowIndex],lis[i] = lis[i],lis[lowIndex]

    # sort each of the two sections of the list and we're done
    qsort(lis,lowIndex,i)
    qsort(lis,i+1,highIndex)

def randomList(length):
    """
    Helper function: creates a list of random numbers
    Parameter: the length for the list
    """
    randList = []
    for i in range(length):
        randList.append(random.randint(0, length))
    return randList

def defineK(lis, iteration, size, n):
    """
        Function that starts the process of randomizing values of k. Takes
        a list, an iteration based on the for loop starting this function (the
        last two iterations cause different results in this function and
        'search'. If the iteration is greater than 1, then it will assume we
        are dealing with k-values and searches NOT within the list).
    """

    k = []

    #First if-statement deals with randomizing k values not in the list. It
    #randomizes from the max size to two times the max size (guarantees
    #nonexistence in lists)
    for i in range(size):
        if iteration > 1: #For values not in list (last pair of experiments)
            k.append(random.randint(n[-1], 2*n[-1]))
        else: #For values in list (first pair of experiments)
            k.append(random.randint(0, len(lis)-1))

    return k

def search(lis, k, iteration):
    """
        Function that processes the searches. The parameter iteration determines
        whether to do a search with k values in/out of the list, and also, based
        on its divisibility with 2, determines whether to start a binary search
        or a trinary search
    """

    t = time.clock()

    for i in range(len(k)):
        if iteration % 2 == 0:  #Binary
            bin_search(lis, 0, len(lis)-1, k[i])
        else:           #Trinary
            trin_search(lis, 0, len(lis)-1, k[i])

    print "N =", len(lis), "| k =", len(k), ":  ", round(time.clock() - t, 6),\
            "seconds process time"

main()