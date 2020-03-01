class Abstract_Van_Emde_Boas_Tree():

    def __init__(self,u:int): print("__init__() - Not Implemented"); pass # u is size
    def add(self,value:int)->bool: return "add() - Not Implemented"
    def lookup(self,value:int)->bool: return "lookup() - Not Implemented"
    def delete(self,value:int)->bool: return "delete() - Not Implemented"
    def predecessor(self,value:int)->int: return "predecessor() - Not Implemented" # return the largest x in T st x<=value
    def successor(self,value:int)->int: return "successor() - Not Implemented" # return the smallest x in T st x>=value

class vEB_Tree_Array(Abstract_Van_Emde_Boas_Tree):

    # NOTE here our universe is [0,u-1]

    def __init__(self,u:int): # u=size of universe
        self.a=[0]*u # u length array of 0s
        self.u=u     # store universe size

    # Insert value
    def add(self,value:int)->bool:
        if (value>=self.u or value<0): return False # not in universe
        self.a[value]=1
        return True

    # Delete value
    def delete(self,value:int)->bool:
        if (value>=self.u or value<0): return False # not in universe
        self.a[value]=0
        return True

    # Return whether a value is in the structure
    def lookup(self,value:int)->bool:
        if (value>=self.u or value<0): return False # not in universe
        return self.a[value]==1

    # return the largest x in T st x<=value
    def predecessor(self,value:int)->int:
        while (True):
            if (value<0 or value>sekf.u-1): return -1 # no predecessor
            if (self.a[value]==1): return value # predecessor found
            value-=1 # move left along the list

    # return the smallest x in T st x>=value
    def successor(self,value:int)->int:
        while (True):
            if (value<0 or value>self.u-1): return -1 # no predecessor
            if (self.a[value]==1): return value # predecessor found
            value+=1 # move left along the list

    def __str__(self):
        vals=[str(i) for i in range(0,self.u) if self.a[i]==1]
        return "[{}]".format(",".join(vals))

class vEB_Tree_Constant_Height(Abstract_Van_Emde_Boas_Tree):

    def __init__(self,u:int): # u=size of universe
        self.a=[0]*u
        self.sqrt_u=int(u**.5)
        self.c=[0]*(1+self.sqrt_u) # summary
        self.u=u

    # Insert value
    def add(self,value:int)->bool:
        if (value<0 or value>=self.u): return False # Not in universe
        self.a[value]=1
        self.c[int(value/self.sqrt_u)]=1
        return True

    # Delete value
    def delete(self,value:int)->bool:
        if (value<0 or value>=self.u): return False # Not in universe
        self.a[value]=0
        for i in range(int(value/self.sqrt_u)*self.sqrt_u,int(1+value/self.sqrt_u)*self.sqrt_u):
            if (i>=self.u): # end of universe
                break
            if (self.a[i]==1):
                return True
        self.c[int(value/self.sqrt_u)]=0
        return True

    # Return whether a value is in the structure
    def lookup(self,value:int)->bool:
        if (value<0 or value>=self.u): return False # Not in universe
        if (self.c[int(value/self.sqrt_u)]==0): return False
        return self.a[value]==1

    # return the largest x in T st x<=value
    def predecessor(self,value:int)->int:
        for i in range(value,int(value/self.sqrt_u)*self.sqrt_u-1,-1):
            if self.a[i]==1: return i
        for i in range(int(value/self.sqrt_u)-1,-1,-1):
            if (self.c[i]==1):
                for j in range(self.sqrt_u*(i+1)-1,self.sqrt_u*i-1,-1):
                    if (self.a[j]==1): return j
        return False # No predecessor

    # return the smallest x in T st x>=value
    def successor(self,value:int)->int:
        for i in range(value,int(value/self.sqrt_u)*(self.sqrt_u+1)-1,1):
            if self.a[i]==1: return i
        for i in range(int(value/self.sqrt_u)+1,self.sqrt_u+1,1):
            if (self.c[i]==1):
                for j in range(self.sqrt_u*i,self.sqrt_u*(i+1)-1,1):
                    if (self.a[j]==1): return j
        return False # No successors

    def __str__(self):
        vals=[str(i) for i in range(0,self.u) if self.a[i]==1]
        return "[{}]".format(",".join(vals))+"\na="+"[{}]".format(",".join([str(i) for i in self.a]))+"\nc="+"[{}]".format(",".join([str(i) for i in self.c]))

class vEB_Tree_Recursive(Abstract_Van_Emde_Boas_Tree):

    # Stores [0,u-1]

    """
    IDEA
     - split universe of size sqrt_u into sqrt_u blocks.
       each block can be considered as its own universe of size sqrt_u.
     - Each block stores values [1,sqrt_u] in it
       For block i these are equivalent to [i*sqrt_u+1,(i+1)*sqrt_u] in the overal universe
     - Each layer has a summary which is a bit-array of size sqrt_u which stores whether a block stores any values
    """

    def __init__(self,u:int): # u=size of universe
        self.u=u
        self.sqrt_u=int(u**.5)
        if u<=2: # leaf
            self.t=[0]*u # bit array
        else: # node
            temp=self.sqrt_u**2
            size=self.sqrt_u
            while(temp<self.u):
                size+=1
                temp+=self.sqrt_u
            self.c=[0]*size
            self.t=[vEB_Tree_Recursive(self.sqrt_u) for i in range(size)]

    # Insert value
    def add(self,value:int)->bool:
        if (value<0 or value>=self.u): return False # Out of universe
        block=int(value/self.sqrt_u)
        index=value-self.sqrt_u*block
        if isinstance(self.t[0],int): # leaf of tree
            self.t[index]=1
            return True
        else: # node in tree
            self.c[block]=1 # update summary
            return self.t[block].add(index) # insert to sub tree

    # Delete value
    def delete(self,value:int)->bool:
        if (value<0 or value>=self.u): return False # out of universe
        block=int(value/self.sqrt_u)
        index=value-self.sqrt_u*block
        if isinstance(self.t[0],int): # leaf of tree
            self.t[index]=0
            return True
        else: # node of tree
            if self.c[block]==0: # don't progress any further
                return True
            else:
                res=self.t[block].delete(index)
                if (res and self.t[block].__is_empty()):
                    self.c[block]=0
                return res

    # Return whether a value is in the structure
    def lookup(self,value:int)->bool:
        if (value<0 or value>=self.u): return False # out of universe
        block=int(value/self.sqrt_u)
        index=value-self.sqrt_u*block
        if isinstance(self.t[0],int): # Leaf of tree
            return self.t[index]==1
        else:
            if (self.c[block]==0): return False
            else:
                return self.t[block].lookup(index)

    # return the largest x in T st x<=value
    def predecessor(self,value:int)->int:
        pass

    # return the smallest x in T st x>=value
    def successor(self,value:int)->int:
        pass

    # returns whether tree is empty
    def __is_empty(self)->bool:
        if isinstance(self.t[0],int): # leaf of tree
            b=True
            for i in range(len(self.t)):
                b&=(self.t[i]==0)
            return b # true if all values are 0
        else:
            b=True
            for i in range(len(self.t)):
                b&=self.t[i].__is_empty()
            return b # true if all


    def __str__(self):
        if isinstance(self.t[0],int): # Leaf of tree (ie just bit array)
            return "Leaf({}) - [{}]".format(self.u,",".join([str(i) for i in self.t]))
        else:
            string="Node({}) - Summary [{}]\n".format(self.u,",".join([str(i) for i in self.c]))
            for t in self.t:
                string+="    {}\n".format(str(t))
            return string

if __name__=="__main__":
    tree=vEB_Tree_Recursive(9)
    tree.add(1)
    tree.add(4)
    tree.add(8)
    print(tree)
    tree.delete(1)
    tree.delete(2)
    print(tree)
