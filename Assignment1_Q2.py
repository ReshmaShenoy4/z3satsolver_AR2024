from z3 import *

import time

start_time = time.time()

s=Optimize()
n=Int('n')
n=11

width  = [Int("width[%s]"  % i) for i in range(n)]
height = [Int("heigth[%s]" % i) for i in range(n)]
x_cor  = [Int("x_cor[%s]"  % i) for i in range(n)]
y_cor  = [Int("y_cor[%s]"  % i) for i in range(n)]

width_max  = Int('width_max')
height_max = Int('height_max')

width_max  = 30
height_max = 30
x_init = 0
y_init = 0

values = [(4,5),(4,6),(5,21),(6,9),(6,8),(6,10),(6,11),(7,12),(8,9),(10,11),(10,20)]

for i in range(n):    
    #Traingles can be rotated
    s.add(Or(And(width[i]==values[i][0],height[i]==values[i][1]),And(width[i]==values[i][1],height[i]==values[i][0])))
 
    #All the triangles should be inside the big canvas
    s.add(And(x_cor[i]>=0,x_cor[i]+width[i]<=width_max))
    s.add(And(y_cor[i]>=0,y_cor[i]+height[i]<=height_max))


#No overlap condition
for i in range(n):
    for j in range (n):
        if(i!=j):
            s.add(Or(x_cor[j]>=x_cor[i]+width[i],x_cor[j]+width[j]<=x_cor[i],y_cor[j]>=y_cor[i]+height[i],y_cor[j]+height[j]<=y_cor[i])) #New poster must either be to the left or right of the current poster


x_1 = Int('x_1')
y_1 = Int('y_1')
x_2 = Int('x_2')
y_2 = Int('y_2')

x_1p = Int('x_1p')
y_1p = Int('y_1p')
x_2p = Int('x_2p')
y_2p = Int('y_2p')

s.add(Or(And((x_1>0),(x_1<30),(x_1==x_2),(y_1==0),(y_2==height_max)), And((y_1>0),(y_1<30),(y_1==y_2),(x_1==0),(x_2==height_max))))
s.add(Or(And((x_1>0),(x_1<30),(x_1==x_2),(y_1==0),(y_2==height_max)), And((y_1>0),(y_1<30),(y_1==y_2),(x_1==0),(x_2==height_max))))

for i in range(n):
   s.add(Implies((x_1==x_2),Or(x_1<=x_cor[i], x_1>=(x_cor[i]+width[i]))))
   s.add(Implies((y_1==y_2),Or(y_1<=y_cor[i], y_1>=(y_cor[i]+height[i]))))
   
print(s.check())   

end_time = time.time()

computation_time = end_time - start_time
print("Computation time:%s seconds" %computation_time)


if(s.check()==sat):
    m=s.model()
    #print(m)
    print("x_1:", s.model().evaluate(x_1, model_completion = True))
    print("x_2:", s.model().evaluate(x_2, model_completion = True))
    print("y_1:", s.model().evaluate(y_1, model_completion = True))
    print("y_2:", s.model().evaluate(y_2, model_completion = True))

########PLOTTING######
x_array=[0]*11   
y_array=[0]*11
width_array = [0]*11
height_array =[0]*11

for i in range(n):
    x_array[i] = m[x_cor[i]]
    y_array[i]= m[y_cor[i]]
    width_array[i] = m[width[i]]
    height_array[i] =m[height[i]]
    
x_cordinates = [val.as_long() for val in x_array]
y_cordinates = [val.as_long() for val in y_array]
width_cordinates = [val.as_long() for val in width_array]
height_cordinates = [val.as_long() for val in height_array]


#PLOTTING 

import matplotlib.pyplot as plt
import matplotlib.patches as patches

colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta', 
          'yellow', 'pink', 'lime', 'teal']

def rect_plotting(x,y,widths,heights):
    fig, ax= plt.subplots()

    total_width = 30
    total_height =30
    ax.set_xlim(0,40)
    ax.set_ylim(0,40)

    for i in range(11):
        rect = patches.Rectangle((x[i],y[i]),widths[i],heights[i],edgecolor ='red',facecolor=colors[i])
        ax.add_patch(rect)
        plt.pause(1)
    
    ax.plot([5,5], [0, 30], color='black', linewidth=2, linestyle='-', label='Highlighted Line')
    plt.show()

    
rect_plotting(x_cordinates,y_cordinates,width_cordinates,height_cordinates)






