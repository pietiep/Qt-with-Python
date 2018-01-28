def printTree(t,l,r,level):
    if(l<=r):
        print("{}{}{}".format(level*"-",t[l],l))
        #gibt es Sons?
        if(t[l][1]>0):
            for j in range(t[l][1]):
                l+=printTree(t,l+j+1,r,level+1)
                print(l, t[l][1], level)
            return j+1
    return 0

if __name__ == "__main__":
    t = [[22,2,0],[23,3,0],[24,0,1],[25,0,1],[26,0,1],[27,1,0],[28,0,1]]
    printTree(t,0,len(t)-1,0)
