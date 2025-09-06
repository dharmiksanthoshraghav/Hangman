def sort(l,k):
    for i in range(0,len(l)):
        j=0
        while j<(len(l)-1):
            if l[j][k]>l[j+1][k]:
                l[j],l[j+1]=l[j+1],l[j]
            j+=1
    return l