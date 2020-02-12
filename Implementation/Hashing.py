from random import randint

class Abstract_Dynamic_Hash_Table():

    def __init__(self,m:int,values:[("key","val")]): print("__init__() - Not Implemented"); pass # m is size of table
    def insert(self,key,value): return "insert() - Not Implemented"
    def lookup(self,key): return "lookup() - Not Implemented"
    def delete(self,key): return "delete() - Not Implemented"

class Abstract_Static_Hash_Table():

    def __init__(self,m:int,values:[("key","val")]): print("__init__() - Not Implemented"); pass # m is size of table
    def lookup(self,key): return "lookup() - Not Implemented"

class FKS_Static_Hash_Table():
    """
    build in O(n) expected time (O(1) amortised expected)
    lookup O(1) time in worst case
    uses O(n) space (O(1) amortised expected)
    """
    def __init__(self,m:int,values:[("key","val")]):# m is size of table
        self.__hs=[None]*m
        while True: # while more than n collisions
            self.__h=Hash_Function(s=len(values)) # Pick hash funcion
            # Prepare table
            self.__table=[]
            for i in range(0,m): self.__table.append([])

            for (k,v) in values: # Insert values
                key=self.__h.hash(k,m)
                self.__table[key].append((k,v))

            # Count number of collisions
            collisions=0
            for t in self.__table:
                collisions+=(len(t)*(len(t)-1))/2

            if (collisions<len(values)): # less than n collsions
                break

        for i in range(0,m): # Build sub tables
            entries=self.__table[i]
            while True: # Build sub table, repeat if a collision occurs
                self.__hs[i]=Hash_Function(s=len(entries)**2) # Pick hash function
                ti=[None]*(len(entries)**2) # prepare table

                collision=False # record if collision occurs
                for (k,v) in entries: # insert values
                    key=self.__hs[i].hash(k,len(entries)**2)
                    if (ti[key]!=None): collision=True; break # rebuild table
                    else: ti[key]=v

                if (not collision): break # success

            self.__table[i]=ti # store table
        print(self.__table)

    def lookup(self,key)->"val":
        i=self.__h.hash(key,len(self.__table))
        j=self.__hs[i].hash(key,len(self.__table[i]))
        return self.__table[i][j]

class Hash_Function():

    __primes=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53
             ,59,61,67,71,73,79,83,89,97,101,103,107
             ,109,113,127,131,137,139,149,151,157,163
             ,167,173,179,181,191,193,197,199,211,223
             ,227,229,233,239,241,251,257,263,269,271
             ,277,281,283,293,307,311,313,317,331,337
             ,347,349,353,359,367,373,379,383,389,397
             ,401,409,419,421,431,433,439,443,449,457
             ,461,463,467,479,487,491,499,503,509,521,523,541] # First 100 primes (im lazy)

    def __init__(self,s,p=None,a=None,b=None): # Supply either p (a prime >s) or s (size of key set)
        if (p): self.__p=p
        else:
            valid_primes=[p for p in Hash_Function.__primes if p>s]
            self.__p=valid_primes[randint(0,len(valid_primes)-1)]

        if (a): self.__a=a
        else: self.__a=randint(1,self.__p)

        if (a): self.__b=a
        else: self.__b=randint(0,self.__p)

    def __str__(self): # Print hash function
        return ("(({}x+{}) mod {}) mod m".format(self.__a,self.__b,self.__p))

    def hash(self,val:int,m:int) -> int: # has a value, m is size of table
        # ((ax+b) mod p) mod m
        return ((self.__a*val+self.__b) % self.__p) % m

if __name__=="__main__":
    table=FKS_Static_Hash_Table(m=5,values=[(0,"Hello"),(1,"World"),(3,"This"),(4,"is"),(7,"a"),(10,"test")])
    print(table.lookup(0)) # Note that if you pass a key which is not associated you will likely have a value returned
    print(table.lookup(1))
    print(table.lookup(3))
