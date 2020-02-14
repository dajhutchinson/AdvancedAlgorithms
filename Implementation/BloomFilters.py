from Hashing import Hash_Function

# NOTE - I think I shouldn't be passing s=m for Hash_Function() instatiation

class Abstract_Bloom_Filter():

    def __init__(self,m:int): print("__init__() - Not Implemented"); pass # m is size of table
    def insert(self,k:int) -> bool: return "insert() - Not Implemented"
    def member(self,k:int) -> bool: return "member() - Not Implemented"

class Bloom_Filter_Array(Abstract_Bloom_Filter):

    def __init__(self,m:int):
        self.__B=["0"]*m

    def insert(self,k:int):
        if (k>len(self.__B)): return False
        self.__B[k]="1"
        return True

    def member(self,k:int):
        if (k>=len(self.__B)): return False
        return self.__B[k]=="1"

    def __str__(self):
        return "".join(self.__B)

class Bloom_Filter_Hash_Table(Abstract_Bloom_Filter):

    def __init__(self,m:int):
        self.__B=["0"]*m
        self.__h=Hash_Function(s=m)

    def insert(self,k:int) -> bool:
        self.__B[self.__h.hash(k,len(self.__B))]="1"

    def member(self,k:int) -> bool:
        return (self.__B[self.__h.hash(k,len(self.__B))]=="1")

    def __str__(self):
        return "".join(self.__B)

class Bloom_Filter_Proper(Abstract_Bloom_Filter):

    def __init__(self,m:int,r:int):
        self.__B=["0"]*m
        self.__hs=[]
        for i in range(r): self.__hs.append(Hash_Function(s=m))

    def insert(self,k:int) -> bool:
        for h in self.__hs:
            self.__B[h.hash(k,len(self.__B))]="1"

    def member(self,k:int) -> bool:
        for h in self.__hs:
            if (self.__B[h.hash(k,len(self.__B))]=="0"): return False
        return True

    def __str__(self):
        return "".join(self.__B)

if __name__=="__main__":
    # Bloom_Filter_Array example
    filter=Bloom_Filter_Proper(m=100,r=2)
    for i in range(0,40,2):
        filter.insert(i)
    print(filter)
    for i in range(0,20):
        print(filter.member(i),end=", ")
