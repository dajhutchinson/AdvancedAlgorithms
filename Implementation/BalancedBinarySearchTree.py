class Balanced_Binary_Search_Tree():

    # Insertion Only
    def __init__(self,v:int,l:int,r:int):
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
    array=[i for i in range(15)]
    tree=Balanced_Binary_Search_Tree.build_tree(array)
    print(tree)
