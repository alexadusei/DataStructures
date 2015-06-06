"""
    Purpose: To test the total depth ratios between a binary search tree and a
             reb-black search tree. This ratio will determine the compactness
             of a BST vs a RBT based on the percentage of the ratio.
"""
import random

def main():
    sizes = [200, 1000, 5000, 25000]
    k = 5000

    print 'TOTAL DEPTHS (k = ' + str(k) + ')\n'

    for n in sizes:
        lis = [i for i in range(1, n+1)]
        print '------- ' + 'N =', str(n)+ ' ------'
        ratios = [0, 0, 0, 0, 0] #make a list for incrementing each category

        for i in range(k):
            random.shuffle(lis)
            BST = createTree(lis)
            RBT = createTree(lis, 'RBT') #2nd parameter means a RBT

            R = float(Total_Depth(BST)) / Total_Depth(RBT)

            #increment each category based on the ratio
            if R < 0.5:
                ratios[0] += 1
            elif 0.5 <= R <= 0.75:
                ratios[1] += 1
            elif 0.75 <= R <= 1.25:
                ratios[2] += 1
            elif 1.25 <= R <= 1.5:
                ratios[3] += 1
            else: #R > 1.5
                ratios[4] += 1

        sumRatios = sum(ratios)

        #print results
        print 'R < 0.5:\t\t\t', str((float(ratios[0])/sumRatios) * 100) + '%'
        print '0.5 <= R <= 0.75:\t', str((float(ratios[1])/sumRatios) * 100) + '%'
        print '0.75 <= R <= 1.25:\t', str((float(ratios[2])/sumRatios) * 100) + '%'
        print '1.25 <= R <= 1.5:\t', str((float(ratios[3])/sumRatios) * 100) + '%'
        print 'R > 1.5:\t\t\t', str((float(ratios[4])/sumRatios) * 100) + '%' '\n'

    print 'Finished processes'

#-------------------------------BINARY SEARCH TREE------------------------------
def insert(tree, value):
    """
    Insert value to tree and return pointer to the root of the modified
    tree.  (This will be different from the original root only when
    we're adding the value to an empty tree.)
    """

    # If the tree is empty, this value becomes the new root.
    # Otherwise, recursively insert the value to the left or right
    # sub-tree.
    if tree == None:
        return {'data':value, 'left':None, 'right':None}
    elif tree['data'] == value:
        return tree
    elif value <= tree['data']:
        tree['left'] = insert(tree['left'],value)
        return tree
    else: # value > tree['data']
        tree['right'] = insert(tree['right'],value)
        return tree

def search(tree, value):
    """
    Search tree for value, returning True if value is found, False otherwise.
    """
    if tree == None:
        return [False]
    elif value == tree['data']:
        return [tree['data']]
    elif value < tree['data']:
        return [tree['data']] + search(tree['left'],value)
    else: # value > tree['data']:
        return [tree['data']] + search(tree['right'],value)

def Total_Depth(tree, depth=1):
    """
    Computes the sum of the depths of all vertices in the tree, where the depth
    of a vertex is its level in the tree (root has depth 1). Second variable
    'depth' does not need to be included during original calling of function,
    as it has default value of 1. Use function as 'TotalDepth(tree)'.
    """

    #Tertiary operater. Uses a boolean to determine the output.
    return 0 if tree == None or tree['data'] == None else \
        Total_Depth(tree['left'], depth+1) + Total_Depth(tree['right'],
                                                            depth+1) + depth

#--------------------------------REB-BLACK TREES--------------------------------

def RB_insert(tree, value):
    #insert the value into the Red-Black tree
    tree = rec_RB_insert(tree, value)
    tree['colour'] = 'B'
    return tree

def rec_RB_insert(tree, value):
    # if data is 'None', the vertex is a leaf. Creates vertex, colours it red
    # and gives it two empty leaves coloured Black
    if tree == None or tree['data'] == None:
        tree = {'colour': 'R', 'data':value}
        tree['left'] = {'colour':'B', 'data':None}
        tree['right'] = {'colour':'B', 'data':None}
        return tree
    elif tree['data'] == value:
        return tree
    else:
        if value > tree['data']: #recurse down the right side
            tree['right'] = rec_RB_insert(tree['right'], value)

            # checking for balance
            if tree['colour'] == 'R':
            # current's parent will check for red vertices
                return tree
            elif tree['right']['colour'] == 'R':
                #if current's right child is Red, check the granndchildren
                if hasRedChild(tree['right']):
                #there are two consecutive Red vertices - fix the problem
                    return RB_fix_R(tree, value)
                else: # no rebalance needed
                    return tree
            else: # tree['right'] is Black - there's no Red-Red conflict
                return tree
        else: # value < tree['data'] - recurse down the left side
            tree['left'] = rec_RB_insert(tree['left'], value)

            if tree['colour'] == 'R': # parent
                return tree
            elif tree['left']['colour'] == 'R': # grandparent
                if hasRedChild(tree['left']):
                    return RB_fix_L(tree, value)
                else:
                    return tree
            else:
                return tree

def hasRedChild(tree):
    return tree['left']['colour'] == 'R' or tree['right']['colour'] == 'R'

def RB_fix_L(current, value):
    # current's left child is Red with a Red child, so we need to fix things
    child = current['left']
    sibling = current['right']

    if sibling['colour'] == 'R':
        # no rotation, just recolour and continue
        child['colour'] = 'B'
        sibling['colour'] = 'B'
        current['colour'] = 'R'
        return current
    else:
        # sibling colour is Black, so we need to rotate
        # we can use 'value' to figure out which rotation is needed
        if value < child['data']:
            # single rotation case - the LL situation
            # identify the important grandchild
            grandchild = child['left']
            # fix the pointers
            current['left'] = child['right']
            child['right'] = current
            # fix the colours
            child['colour'] = 'B'
            current['colour'] = 'R'
            # return the new root of this subtree
            return child
        else:
            # double rotation case - the LR situation
            #identify the important grandchild
            grandchild = child['right']
            #fix the pointers
            child['right'] = grandchild['left']
            current['left'] = grandchild['right']
            grandchild['left'] = child
            grandchild['right'] = current
            # fix the colours
            grandchild['colour'] = 'B'
            current['colour'] = 'R'
            # return the new root of this subtree
            return grandchild

def RB_fix_R(current, value):
    child = current['right']
    sibling = current['left']

    if sibling['colour'] == 'R':
        child['colour'] = 'B'
        sibling['colour'] = 'B'
        current['colour'] = 'R'
        return current
    else:
        if value > child['data']:
            grandchild = child['right']
            current['right'] = child['left']
            child['left'] = current
            child['colour'] = 'B'
            current['colour'] = 'R'
            return child
        else:
            grandchild = child['left']
            child['left'] = grandchild['right']
            current['right'] = grandchild['left']
            grandchild['right'] = child
            grandchild['left'] = current
            grandchild['colour'] = 'B'
            current['colour'] = 'R'
            return grandchild

def RB_search(tree, value):
    """
    Search tree for value, returning True if value is found, False otherwise.
    """
    if tree['data'] == None: # again, leaves will have 'none' for the data key
        return [False]
    elif value == tree['data']:
        return [str(tree['data']) + '(' + str(tree['colour']) + ')']
    elif value < tree['data']:
        return [str(tree['data']) + '(' + str(tree['colour']) + ')'] + \
                RB_search(tree['left'],value)
    else: # value > tree['data']:
        return [str(tree['data']) + '(' + str(tree['colour']) + ')'] + \
                RB_search(tree['right'],value)

#-------------------------------TEST FUNCTIONS----------------------------------
def createTree(values, treeType=0):
    """
    Shortcut for testing & debugging: creates a tree from a Python list of
    values. Entering anything for the second parameter will create a RBT, while
    entering no 2nd paramenter is a BST.
    """
    tree = None
    for v in values:
        tree = insert(tree, v) if treeType == 0 else RB_insert(tree, v)
    return tree

def printTree(tree, indent=0):
    """
    Recursive version is simple: print the right sub-tree, the root,
    and the left subtree.  (In that order so that if you tilt your head
    to the left things are in the right place.) Second parameter is the type
    to indent the tree. Works for both BSTs and RBTs by checking the amount of
    keys in the dictionary (BST only have data, left, right while RBT had the
    additional key 'colour').
    """
    if tree == None or tree['data'] == None:
        return
    else:
        printTree(tree['right'],indent+4)
        if len(tree.keys()) == 3:
            print " "*indent + str(tree['data'])
        else:
            print " "*indent + str(tree['data'])+'(' + str(tree['colour']) +')'
        printTree(tree['left'],indent+4)

main()