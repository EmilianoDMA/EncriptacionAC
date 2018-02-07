# powered by evilnapsis
# website http://evilnapsis.com
def convert(d):
    if(d=="000"): r = '0';
    elif(d=="001"): r = '1';
    elif(d=="010"): r = '1';
    elif(d=="011"): r = '1';
    elif(d=="100"): r = '0';
    elif(d=="101"): r = '1';
    elif(d=="110"): r = '1';
    elif(d=="111"): r = '0';
    return r;
#print convert("001")

#cad = "101011100101000"
cad = raw_input("input >> ")
ran = raw_input("range >> ")
t =len(cad)
index = t-1
print "longitud : ",t
r = ""
for j in range(int(ran)):
    aux1 = index # este debe ser longitud -1 , al iniciar
    aux2 = index -index # este debe ser 0 al iniciar
    aux3 = index - (index-1) # este debe ser 1 al iniciar
    cnt = 1
    r=""
    for i in range(t):
        if aux3==t:
           aux3=0
        l = cad[aux1]
        m = cad[aux2]
        n = cad[aux3]
    
        n1 = l+m+n
        if cnt==1:
            aux1 = 0
            aux2 = 1
            aux3 = 2
        else :
            aux1 = aux1 +1
            aux2 = aux2 +1
            aux3 = aux3 +1
        cnt = cnt+1
        r += convert(n1)
    cad = r
    print r