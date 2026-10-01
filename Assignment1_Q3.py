from z3 import *
import time

start_time = time.time()
s = Optimize()
n = Int('n')
n=21
s0 = int(n/2)
satisfiable_loops = 0
#[BitVec("input%s" % i, 1) for i in range(10)]
# A,B,C,S are the boolean variable indicating whether there is a truck in that village or not.
A = [Bool("A[%s]" % i) for i in range(n)]
B = [Bool("B[%s]" % i) for i in range(n)]
C = [Bool("C[%s]" % i) for i in range(n)]
S = [Bool("S[%s]" % i) for i in range(n)]

# We define paths of boolean type. We define 6 paths ie 
P1=[Bool("P1[%s]" % i) for i in range(n)] # Path between S-A
P2=[Bool("P2[%s]" % i) for i in range(n)] # Path between S-C
P3=[Bool("P3[%s]" % i) for i in range(n)] # Path between A-C
P4=[Bool("P4[%s]" % i) for i in range(n)] # Path between A-B
P5=[Bool("P5[%s]" % i) for i in range(n)] # Path between B-C
P6=[Bool("P6[%s]" % i) for i in range(n)] # Path between C-B

#We define Capacity of each village as integer variable as we have to do arithmetic operations on them
CA = [Int("CA[%s]" % i) for i in range(n)]
CB = [Int("CB[%s]" % i) for i in range(n)]
CC = [Int("CC[%s]" % i) for i in range(n)]
CS = [Int("CS[%s]" % i) for i in range(n)]

#We also define constants to hold the max values
CA_max = Int('CA_max')
CB_max = Int('CB_max')
CC_max = Int('CC_max')
CS_max = Int('CS_max')

#Define weights for each paths
wt_P1 = Int('wt_P1')
wt_P2 = Int('wt_P2')
wt_P3 = Int('wt_P3')
wt_P4 = Int('wt_P4')
wt_P5 = Int('wt_P5')
wt_P6 = Int('wt_P6')
C_min = Int('C_min')

s.add(wt_P1==15)
s.add(wt_P2==15)
s.add(wt_P3==12)
s.add(wt_P4==17)
s.add(wt_P5==13)
s.add(wt_P6==9)


# Initial State
s.add(A[0] == False)
s.add(B[0] == False)
s.add(C[0] == False)
s.add(S[0] == True)

s.add(CA_max == 90)
s.add(CB_max == 120)
s.add(CC_max == 90)
s.add(CS_max == 150) #Changed 
s.add(C_min==60)
s.add(CA[0]==60)
s.add(CB[0]==60)
s.add(CC[0]==60)
s.add(CS[0]==130)

village = []

# Consideration is : in the ith iteration, you just calculate what is the ith village, based on the previous village and the path taken from the previous village
#Calculate the Capacity of the villages in the ith iteration, based on the path taken from the previous village

for i in range(1,n):
    #s.push()
 

    s.add(Or(A[i],B[i],C[i],S[i]) == True) # The truck should be at one of the place
    s.add(Or(P1[i],P2[i],P3[i],P4[i],P5[i],P6[i]) == True) # The truck should be at one of the place

    s.add(And(Implies(P1[i],And(Not(P2[i]),Not(P3[i]),Not(P4[i]),Not(P5[i]),Not(P6[i]))),
              Implies(P2[i],And(Not(P1[i]),Not(P3[i]),Not(P4[i]),Not(P5[i]),Not(P6[i]))),
              Implies(P3[i],And(Not(P2[i]),Not(P1[i]),Not(P4[i]),Not(P5[i]),Not(P6[i]))),
              Implies(P4[i],And(Not(P2[i]),Not(P3[i]),Not(P1[i]),Not(P5[i]),Not(P6[i]))),
              Implies(P5[i],And(Not(P2[i]),Not(P3[i]),Not(P4[i]),Not(P1[i]),Not(P6[i]))),
              Implies(P6[i],And(Not(P2[i]),Not(P3[i]),Not(P4[i]),Not(P5[i]),Not(P1[i])))))

    s.add(And(Implies(A[i],And(Not(B[i]),Not(C[i]),Not(S[i]))),
              Implies(B[i],And(Not(A[i]),Not(C[i]),Not(S[i]))),
              Implies(C[i],And(Not(B[i]),Not(A[i]),Not(S[i]))),
              Implies(S[i],And(Not(B[i]),Not(C[i]),Not(A[i])))))

   # Which path to take 
    s.add(And(Implies(A[i-1],Or(P4[i],P3[i],P1[i])),
              Implies(B[i-1],Or(P4[i],P5[i])),
              Implies(C[i-1],Or(P2[i],P3[i],P6[i])), 
              Implies(S[i-1],Or(P1[i],P2[i]))))
    
    #Which village to go
    s.add(And(Implies(And(C[i-1],P3[i]),A[i]),
             Implies(And(C[i-1],P2[i]),S[i]),
             Implies(And(S[i-1],P1[i]),A[i]),
             Implies(And(S[i-1],P2[i]),C[i]),
             Implies(And(A[i-1],P1[i]),S[i]),
             Implies(And(A[i-1],P3[i]),C[i]),
             Implies(And(A[i-1],P4[i]),B[i]),
             Implies(And(B[i-1],P4[i]),A[i]),
             Implies(And(C[i-1],P6[i]),B[i]),
             Implies(And(B[i-1],P5[i]),C[i])))
    

    
    #Truck is at S
    s.add(Implies(S[i],And(CA[i]==CA[i-1]-wt_P1,CB[i]==CB[i-1]-wt_P1,CC[i]==CC[i-1]-wt_P1,CS[i]==CS_max)))

    #Truck is at A
    s.add(And(Implies(And(A[i],P1[i]),And(CB[i]==CB[i-1]-wt_P1,CC[i]==CC[i-1]-wt_P1)),
              Implies(And(A[i],P3[i]),And(CB[i]==CB[i-1]-wt_P3,CC[i]==CC[i-1]-wt_P3)),
              Implies(And(A[i],P4[i]),And(CB[i]==CB[i-1]-wt_P4,CC[i]==CC[i-1]-wt_P4))))
    

    s.add(And(Implies(And(A[i],P1[i]),If((CA[i-1]-wt_P1)<C_min,And(CA[i]<=CA_max,CA[i]>=C_min,CS[i]== CS[i-1]-(CA[i]-CA[i-1]+wt_P1)),And(CA[i]==CA[i-1],CS[i]==CS[i-1]))),
              Implies(And(A[i],P3[i]),If((CA[i-1]-wt_P3)<C_min,And(CA[i]<=CA_max,CA[i]>=C_min,CS[i]== CS[i-1]-(CA[i]-CA[i-1]+wt_P3)),And(CA[i]==CA[i-1],CS[i]==CS[i-1]))),
              Implies(And(A[i],P4[i]),If((CA[i-1]-wt_P4)<C_min,And(CA[i]<=CA_max,CA[i]>=C_min,CS[i]== CS[i-1]-(CA[i]-CA[i-1]+wt_P4)),And(CA[i]==CA[i-1],CS[i]==CS[i-1])))))
    
    #Truck is at C  
    s.add(And(Implies(And(C[i],P2[i]),And(CB[i]==(CB[i-1]-wt_P2),CA[i]==(CA[i-1]-wt_P2))),
              Implies(And(C[i],P3[i]),And(CB[i]==(CB[i-1]-wt_P3),CA[i]==(CA[i-1]-wt_P3))),
              Implies(And(C[i],P5[i]),And(CB[i]==(CB[i-1]-wt_P5),CA[i]==(CA[i-1]-wt_P5)))))


    s.add(And(Implies(And(C[i],P2[i]),If((CC[i-1]-wt_P2)<C_min,And(CC[i]<=CC_max,CC[i]>=C_min,CS[i]== CS[i-1]-(CC[i]-CC[i-1]+wt_P2)),And(CC[i]==CC[i-1],CS[i]==CS[i-1]))),
              Implies(And(C[i],P3[i]),If((CC[i-1]-wt_P3)<C_min,And(CC[i]<=CC_max,CC[i]>=C_min,CS[i]== CS[i-1]-(CC[i]-CC[i-1]+wt_P3)),And(CC[i]==CC[i-1],CS[i]==CS[i-1]))),
              Implies(And(C[i],P5[i]),If((CC[i-1]-wt_P5)<C_min,And(CC[i]<=CC_max,CC[i]>=C_min,CS[i]== CS[i-1]-(CC[i]-CC[i-1]+wt_P4)),And(CC[i]==CC[i-1],CS[i]==CS[i-1])))))
 
    #Truck at B
    s.add(And(Implies(And(B[i],P4[i]),And(CA[i]==CA[i-1]-wt_P4,CC[i]==CC[i-1]-wt_P4)),
              Implies(And(B[i],P6[i]),And(CA[i]==CA[i-1]-wt_P6,CC[i]==CC[i-1]-wt_P6))))
    
    s.add(And(Implies(And(B[i],P4[i]),If((CB[i-1]-wt_P4)<C_min,And(CB[i]<=CB_max,CB[i]>=C_min,CS[i]== CS[i-1]-(CB[i]-CB[i-1]+wt_P4)),And(CB[i]==CB[i-1],CS[i]==CS[i-1]))),
              Implies(And(B[i],P6[i]),If((CB[i-1]-wt_P6)<C_min,And(CB[i]<=CB_max,CB[i]>=C_min,CS[i]== CS[i-1]-(CB[i]-CB[i-1]+wt_P6)),And(CB[i]==CB[i-1],CS[i]==CS[i-1])))))
    

    #Possible contraints
    s.add(CS[i]>0)
    s.add(CS[i]<(CA[i]+CB[i]+CC[i]))
    s.add(CA[i]>0)
    s.add(CB[i]>0)
    s.add(CC[i]>0)
    s.add(Implies(And(i>=s0, (i % s0) ==0), And(A[i] == A[s0], B[i] == B[s0], C[i]==C[s0],S[i]==S[s0],CA[i] == CA[s0],CB[i]==CB[s0],CC[i]==CC[s0],CS[i]==CS[s0]), 
                  And(CA[i]==CA[i],CB[i]==CB[i],CC[i]==CC[i],CS[i]==CS[i],A[i] == A[i], B[i] == B[i], C[i]==C[i],S[i]==S[i])))
    #print(s.check())
    if(s.check()==sat):
        satisfiable_loops += 1


end_time = time.time()

computation_time = end_time - start_time
print("Computation time:%s seconds" %computation_time)
print("Total number of loops/iterations:%s"%(n-1))
print("Number of satisfiable loops:%s"%satisfiable_loops)
print("Number of un-satisfiable loops:%s"%(n-satisfiable_loops-1))
for i in range(n):
    if(s.model().evaluate(A[i])==True): village.append('A')
    elif(s.model().evaluate(B[i])==True): village.append('B')
    elif(s.model().evaluate(C[i])==True): village.append('C')
    else:village.append('S')
print(village)

#Lasso schedule check
if(s.check() == sat):
    m=s.model()
    for i in range(1,n):
        if((i % s0) ==0):
            print(i)
            print("CA[%s]="%i,s.model().evaluate(CA[i], model_completion = True))
            print("CB[%s]="%i,s.model().evaluate(CB[i], model_completion = True))
            print("CC[%s]="%i,s.model().evaluate(CC[i], model_completion = True))
            print("CS[%s]="%i,s.model().evaluate(CS[i], model_completion = True)) 


#if(s.check() == sat):
#   m=s.model()
#   for i in range(0,n):
        #print("A[%s]="%i,s.model().evaluate(A[i], model_completion = True))
        #print("B[%s]="%i,s.model().evaluate(B[i], model_completion = True))
        #print("C[%s]="%i,s.model().evaluate(C[i], model_completion = True))
        #print("S[%s]="%i,s.model().evaluate(S[i], model_completion = True))
        #print("P1[%s]="%i,s.model().evaluate(P1[i], model_completion = True))
        #print("P2[%s]="%i,s.model().evaluate(P2[i], model_completion = True))
        #print("P3[%s]="%i,s.model().evaluate(P3[i], model_completion = True))
        #print("P4[%s]="%i,s.model().evaluate(P4[i], model_completion = True))
        #print("P5[%s]="%i,s.model().evaluate(P5[i], model_completion = True))
        #print("P6[%s]="%i,s.model().evaluate(P6[i], model_completion = True))
        #print("CA[%s]="%i,s.model().evaluate(CA[i], model_completion = True))
        #print("CB[%s]="%i,s.model().evaluate(CB[i], model_completion = True))
        #print("CC[%s]="%i,s.model().evaluate(CC[i], model_completion = True))
        #print("CS[%s]="%i,s.model().evaluate(CS[i], model_completion = True))  
        

        