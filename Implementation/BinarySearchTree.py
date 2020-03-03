class Binary_Search_Tree():

    def __init__(self,value:int,left:"Binary_Search_Tree",right:"Binary_Search_Tree"): print("__init__() - Not Implemented"); pass # m is size of table

    # core
    def insert(self,key,value): return "insert() - Not Implemented"

    # lookup
    def lookup(self,key): return "lookup() - Not Implemented"
    def predecessor(self,key): return "predecessor() - Not Implemented"
    def successor(self,key): return "successor() - Not Implemented"

    # structure
    def left_rotation(self)->"Binary_Search_Tree": return "left_rotation() - Not Implemented"
    def right_rotation(self)->"Binary_Search_Tree": return "right_rotation() - Not Implemented"

    # utility
    def all_keys(self)->[int]: return "height() - Not Implemented"
    def height(self)->int: return "height() - Not Implemented"
    def path(self,left:int,right:int)->["Binary_Search_Tree"]: return "path() - Not Implemented" # list of nodes on path between two values (value doesnt have to be in tree)
    def root_path(self,key:int)->["Binary_Search_Tree"]: return "root_path() - Not Implemented" # list of nodes on path from root to value (value doesnt have to be in tree)

class Balanced_Binary_Search_Tree():

    # Insertion Only
    def __init__(self,v:int,l:"Balanced_Binary_Search_Tree",r:"Balanced_Binary_Search_Tree"):
        self.v=v
        self.l=l
        self.r=r

    # insert element to tree
    def insert(self,v:int)->"Balanced_Binary_Search_Tree":
        if (v>=self.v): # insert into right subtree
            if (self.r==None):
                self.r=Balanced_Binary_Search_Tree(v,None,None)
                return self
            self.r=self.r.insert(v)
        # insert into left subtree
        else:
            if (self.l==None):
                self.l=Balanced_Binary_Search_Tree(v,None,None)
                return self
            self.l=self.l.insert(v)
        if (not self.is_balanced()):
            if (self.l==None):l_height=0
            else: l_height=self.l.height()
            if (self.r==None): r_height=0
            else: r_height=self.r.height()

            if (l_height>r_height):
                t=self.right_rotation()
                #print("RIGHT\n"+str(t))
                return t
            else:
                t=self.left_rotation()
                #print("LEFT\n"+str(t))
                return t
        else:
            return self

    # return whether a key is in the tree
    def lookup(self,key:int)->bool:
        if key==self.v: return True
        if (key>self.v and self.r==None): return False
        elif key>self.v: return self.r.lookup(key)
        if (key<self.v and self.l==None): return False
        elif key<self.v: return self.l.lookup(key)

    # return predecessor to key in the tree, if one exists
    def predecessor(self,key:int,parent_value=None)->int:
        if key==self.v: return key
        if (key>self.v and self.r==None): return self.v
        elif key>self.v: return self.r.predecessor(key,self.v)
        if (key<self.v and self.l==None): return parent_value # might be none
        elif key<self.v: return self.l.predecessor(key,parent_value)

    # return successor to key in the tree, if one exists
    def successor(self,key:int,parent_value=None)->int:
        if key==self.v: return key
        if (key>self.v and self.r==None): return parent_value # might be none
        elif key>self.v: return self.r.successor(key,parent_value)
        if (key<self.v and self.l==None): return self.v
        elif key<self.v: return self.l.successor(key,self.v)

    # returns path root to key (basterisation of lookup())
    # works even if key is not in tree
    def root_path(self,key:int)->["Balanced_Binary_Search_Tree"]:
        node=self
        path_arr=[node]
        while (True):
            if key==node.v: break
            if (key>node.v and node.r==None): break # might be none
            elif key>node.v:
                node=node.r
                path_arr.append(node)
            if (key<node.v and node.l==None): break
            elif key<node.v:
                node=node.l
                path_arr.append(node)
        return path_arr

    def path(self,left:int,right:int)->["Balanced_Binary_Search_Tree"]:
        if (left>right): return None
        left_path=self.root_path(left)
        right_path=self.root_path(right)
        shared_root_index=[i for i in range(min(len(left_path),len(right_path))) if left_path[i].v==right_path[i].v][-1] # index of last shared node in paths
        path=[i for i in left_path[shared_root_index+1:]][::-1]+[i for i in right_path[shared_root_index:]]
        return path

    # return height of tree
    def height(self)->int:
        if (self.l==None): l_height=0
        else: l_height=self.l.height()
        if (self.r==None): r_height=0
        else: r_height=self.r.height()
        return max(l_height,r_height) + 1

    # return whether tree is balanced
    def is_balanced(self)->bool:
        if (self.l==None):
            l_balanced=True
            l_height=0
        else:
            l_balanced=self.l.is_balanced()
            l_height=self.l.height()
        if (self.r==None):
            r_balanced=True
            r_height=0
        else:
            r_balanced=self.r.is_balanced()
            r_height=self.r.height()

        return l_balanced and r_balanced and (abs(r_height-l_height)<=1)

    # left rotate
    def left_rotation(self)->"Balanced_Binary_Search_Tree":
        if self.r==None: # no pivot to rotate about
            return False
        pivot=self.r
        pivot_left_subtree=pivot.l
        self.r=pivot_left_subtree
        pivot.l=self
        return pivot

    # right rotate
    def right_rotation(self)->"Balanced_Binary_Search_Tree":
        if self.l==None: # no pivot to rotate about
            return False
        pivot=self.l
        pivot_right_subtree=pivot.r
        self.l=pivot_right_subtree
        pivot.r=self
        return pivot

    # return all keys stored in (sub)-tree (unsorted)
    def all_keys(self)->[int]:
        keys=[self.v]
        if (self.r!=None): keys+=self.r.all_keys()
        if (self.l!=None): keys+=self.l.all_keys()
        return keys

    # build balanced tree for list of integers
    def build_tree(data:[int])->"Balanced_Binary_Search_Tree":
        tree=Balanced_Binary_Search_Tree(data[0],None,None)
        for i in data[1:]:
            tree=tree.insert(i)
        return tree

    def __str__(self):
        if self.l==None: l_str="None"
        else:
            l_str=str(self.l)
            spl=l_str.split("\n")
            spl=["  "+s for s in spl]
            l_str="\n".join(spl)
        if self.r==None: r_str="None"
        else:
            r_str=str(self.r)
            spl=r_str.split("\n")
            spl=["  "+s for s in spl]
            r_str="\n".join(spl)
        return "v:{}\n  l:{}\n  r:{}".format(self.v,l_str,r_str)

if __name__=="__main__":
    array=[i for i in range(0,15,2)]
    tree=Balanced_Binary_Search_Tree.build_tree(array)
    print(tree)
    for i in range(-2,17,1):
        print(i,tree.root_path(i))
    print(tree.path(left=0,right=8))
