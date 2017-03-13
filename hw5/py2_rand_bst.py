from __future__ import division
from BSTNode import BSTNode
from BSTree import BSTree
import random

## bugs to vladimir dot kulyukin at gmail dot com

## implement this method
def gen_rand_bst(num_nodes, a, b):
    bst = BSTree()
    for i in range(num_nodes):
        key = random.randint(a,b)
        bst.insertKey(key)
    return bst


## implement this method
def estimate_list_prob_in_rand_bsts_with_num_nodes(num_rbsts, num_nodes, a, b):
    #this is a counter for how many rbst's are lists
    num_lists = 0
    rbsts_lists = []
    list_prob_dict = {}
    for i in range(num_rbsts):
        bst = gen_rand_bst(num_nodes, a, b)
        if bst.isList():
            num_lists += 1
            #add the bst that is a list to the rbsts_lists array
            rbsts_lists.append(bst)


    list_prob_dict[0] = (num_lists/num_rbsts, rbsts_lists)
    return list_prob_dict[0]




def estimate_list_probs_in_rand_bsts(num_nodes_start, num_nodes_end, num_rbsts, a, b):
    d = {}
    for num_nodes in xrange(num_nodes_start, num_nodes_end+1):
        d[num_nodes] = estimate_list_prob_in_rand_bsts_with_num_nodes(num_rbsts, num_nodes, a, b)
    return d

## implement this method
def estimate_balance_prob_in_rand_bsts_with_num_nodes(num_rbsts, num_nodes, a, b):
    #this is a counter for how many rbst's are lists
    num_balanced = 0
    rbsts_balanced = []
    balanced_prob_dict = {}
    for i in range(num_rbsts):
        bst = gen_rand_bst(num_nodes, a, b)
        if bst.isBalanced():
            num_balanced += 1
            #add the bst that is a list to the rbsts_lists array
            rbsts_balanced.append(bst)

    balanced_prob_dict[0] = (num_balanced/num_rbsts, rbsts_balanced)
    return balanced_prob_dict[0]

def estimate_balance_probs_in_rand_bsts(num_nodes_start, num_nodes_end, num_rbsts, a, b):
    d = {}
    for num_nodes in xrange(num_nodes_start, num_nodes_end+1):
        d[num_nodes] = estimate_balance_prob_in_rand_bsts_with_num_nodes(num_rbsts, num_nodes, a, b)
    return d

if __name__ == '__main__':

    # d = estimate_list_probs_in_rand_bsts(5, 200, 1000, 0, 1000000)
    # for k, v in d.iteritems():
    #     print('probability of linearity in rbsts with %d nodes = %f' % (k, v[0]))

    b = estimate_balance_probs_in_rand_bsts(5, 200, 1000, 0, 1000000)
    for k, v in b.iteritems():
        print('probability of balance in rbsts with %d nodes = %f' % (k, v[0]))
