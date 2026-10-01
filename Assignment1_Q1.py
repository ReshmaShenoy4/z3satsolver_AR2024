from z3 import *
import time

start_time = time.time()
s=Optimize()
n=Int('n')
n=6
WT_per_nuzzles  = Int('WT_nuzzles')
WT_per_prittles = Int('WT_prittles')
WT_per_skipples = Int('WT_skipples')
WT_per_crottles = Int('WT_crottles')
WT_per_dupples  = Int('WT_dupples')

Tot_nuzzles  = Int('Tot_nuzzles')
Tot_prittles = Int('Tot_prittles')
Tot_skipples = Int('Tot_skipples')
Tot_crottles = Int('Tot_crottles')
Tot_dupples  = Int('Tot_dupples')

Sum_nuzzles  = Int('Sum_nuzzles')
Sum_prittles = Int('Sum_prittles')
Sum_skipples = Int('Sum_skipples')
Sum_crottles = Int('Sum_crottles')
Sum_dupples  = Int('Sum_dupples')

# Six trucks
num_pallets_in_truck  = [Int("num_pallets_in_truck[%s]" % i) for i in range(n)]
num_nuzzles_in_truck  = [Int("num_nuzzles_in_truck[%s]" % i) for i in range(n)]
num_prittles_in_truck = [Int("num_prittles_in_truck[%s]" % i) for i in range(n)]
num_skipples_in_truck = [Int("num_skipples_in_truck[%s]" % i) for i in range(n)]
num_crottles_in_truck = [Int("num_crottles_in_truck[%s]" % i) for i in range(n)]
num_dupples_in_truck  = [Int("num_dupples_in_truck[%s]" % i) for i in range(n)]
WT_per_truck          = [Int("WT_per_truck[%s]" % i) for i in range(n)]

#Constraints
s.add(And(Sum_nuzzles==0,Sum_dupples==0,Sum_crottles==0,Sum_prittles==0,Sum_skipples==0))
s.add(And(Tot_nuzzles == 6,Tot_prittles == 12,Tot_skipples == 15,Tot_crottles == 8))
s.add(And(WT_per_nuzzles==800,WT_per_prittles==405,WT_per_skipples==500,WT_per_crottles==2500,WT_per_dupples==600))

for i in range(n):
    #s.add(num_dupples_in_truck[i]>=0) # If i do this equal to 0, then it isnt divided amongst all trucks. But if we remove the equal sign, it gets divided amongst all.
    s.add(And(num_nuzzles_in_truck[i]>=0,num_prittles_in_truck[i]>=0,num_skipples_in_truck[i]>=0,num_crottles_in_truck[i]>=0,num_dupples_in_truck[i]>=0,num_pallets_in_truck[i]>=0))

    s.add(num_pallets_in_truck[i] == num_nuzzles_in_truck[i]+num_prittles_in_truck[i]+num_skipples_in_truck[i]+num_crottles_in_truck[i]+num_dupples_in_truck[i])
    s.add(num_pallets_in_truck[i]<=10)
    s.add(WT_per_truck[i] == ((num_nuzzles_in_truck[i]* WT_per_nuzzles) +
                              (num_prittles_in_truck[i]*WT_per_prittles)+
                              (num_skipples_in_truck[i]*WT_per_skipples)+
                              (num_crottles_in_truck[i]*WT_per_crottles)+
                              (num_dupples_in_truck[i]*WT_per_dupples)))
    s.add(WT_per_truck[i]<=8000)
    Sum_nuzzles  = Sum_nuzzles  + num_nuzzles_in_truck[i]
    Sum_prittles = Sum_prittles + num_prittles_in_truck[i]
    Sum_skipples = Sum_skipples + num_skipples_in_truck[i]
    Sum_crottles = Sum_crottles + num_crottles_in_truck[i]
    Sum_dupples  = Sum_dupples  + num_dupples_in_truck[i]

    s.add(If(num_crottles_in_truck[i]>0,num_dupples_in_truck[i]>=2,num_dupples_in_truck[i]>=0))



C_prittles = [Bool("C_prittles[%s]" % i) for i in range(n)]
C_skipples = [Bool("C_skipples[%s]" % i) for i in range(n)]
for i in range(n):
    s.add(If(num_prittles_in_truck[i]>0,C_prittles[i]==True,C_prittles[i]==False))
    s.add(If(num_skipples_in_truck[i]>0,C_skipples[i]==True,C_skipples[i]==False))

s.add(AtLeast(C_prittles[0]==True,C_prittles[1]==True,C_prittles[2]==True,C_prittles[3]==True,C_prittles[4]==True,C_prittles[5]==True,5))
s.add(AtMost(C_skipples[0]==True,C_skipples[1]==True,C_skipples[2]==True,C_skipples[3]==True,C_skipples[4]==True,C_skipples[5]==True,2))
s.add(And(Sum_nuzzles  == Tot_nuzzles,Sum_prittles == Tot_prittles,Sum_skipples == Tot_skipples,Sum_crottles == Tot_crottles))
s.maximize(Sum_dupples)

print(s.check())
if(s.check()==sat):
    m=s.model()
    #print(m)
    print("Sum_dupples:", s.model().evaluate(Sum_dupples, model_completion = True))

for i in range(n):
    print("Num_of_dupples_in_truck[%s]="%i,s.model().evaluate(num_dupples_in_truck[i], model_completion = True))
    #print("Num_of_crottles_in_truck[%s]="%i,s.model().evaluate(num_crottles_in_truck[i], model_completion = True))

end_time = time.time()

computation_time = end_time - start_time
print("Computation time:%s seconds" %computation_time)