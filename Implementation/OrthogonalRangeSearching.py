from BinarySearchTree import Balanced_Binary_Search_Tree

"""
# TODO:
    -  Multidimensional case but that requires reworking binary search to store a key and and an element and i can't be asked
"""
class Abstract_Orthogonal_Range_Search():

    def __init__(self,d:int,data:[("d*int")]): print("__init__() - Not Implemented"); pass # d is the number of dimensions, data should be array of d dimensional tuples
    def lookup(self,x_bounds:("d*int"),y_bounds:("d")) -> bool: return "lookup() - Not Implemented"

class One_D_Orthogonal_Range_Search():

    def __init__(self,data:[int]):
        self.t=Balanced_Binary_Search_Tree.build_tree(data)

    # return values in bound (unsorted)
    def lookup(self,lower_bound:int,upper_bound:int)->[int]:
        res=[]
        succ=self.t.successor(lower_bound)
        pred=self.t.predecessor(upper_bound)
        path=self.t.path(succ,pred) # path between successor and predecessor (elems are trees)
        path_values=[i.v for i in path] # values on path

        for i in path: # note these are read left to right
            if (i.v>=lower_bound and i.v<=upper_bound): res.append(i.v) # node value is in range
            # find off path edge
            if (i.l!=None): # left tree exists
                if (i.l.v not in path_values): # and is off path edge
                    if (i.l.v>=lower_bound and i.l.v<=upper_bound): # and root is in bound
                        res+=i.l.all_keys()
            if (i.r!=None): # right tree exists
                if (i.r.v not in path_values): # and is off path edge
                    if (i.r.v>=lower_bound and i.r.v<=upper_bound): # and root is in bound
                        res+=i.r.all_keys()
        return res


if __name__=="__main__":
    vals=[i for i in range(0,100,3)]
    range_search=One_D_Orthogonal_Range_Search(vals)
    #print(range_search.t)
    vals=range_search.lookup(16,47)
    vals.sort()
    print(vals) # all multiples of 3 between 16 & 47
