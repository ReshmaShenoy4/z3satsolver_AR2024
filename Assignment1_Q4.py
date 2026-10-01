from z3 import *

import time
start_time = time.time()

solver = Solver()

final_a = Int('final_a')
final_b = Int('final_b')

a = Int('a')
b = Int('b')
solver.add(a == 1, b == 1)

b_values = [b]  

for i in range(1, 11):
    
    test = Bool(f'test_{i}')

   
    branch1_a = a + 2 * b  
    branch1_b = b + 3      
    branch2_a = a + i      
    branch2_b = b - branch2_a  

    a = If(test, branch1_a, branch2_a)
    b = If(test, branch1_b, branch2_b)

    
    b_current = Int(f'b_{i}')
    solver.add(b_current == b)  
    b_values.append(b_current)  


for n in range(1, 11):
    solver.push()  
    solver.add(b == 210 + n)
    if solver.check() == sat:
        print(f"Program crashes for n = {n}")
    else:
        print(f"Program is safe for n = {n}")
    solver.pop()  

end_time = time.time()

computation_time = end_time - start_time
print("Computation time:%s seconds" %computation_time)


#for the second part of the qn


# solver.add(final_a == a)
# solver.add(final_b == b)
# solver.add(final_b == 210 + 3)

# if solver.check() == sat:
#     model = solver.model()
#     print("Solution found:")
#     print(f"Final values: a = {model[final_a]}, b = {model[final_b]}")
    
    
#     for i in range(1, 11):
#         test_value = model[Bool(f'test_{i}')]
#         b_value = model[Int(f'b_{i}')]
#         print(f"Iteration {i}: test = {test_value}, b = {b_value}")
# else:
#     print("No solution found.")