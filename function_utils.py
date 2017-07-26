import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def Fonseca(x_list):
    # -4 <= xi <= 4
    s1,s2 = 0.0,0.0
    n = len(x_list)
    for x in x_list :
        s1 = s1 + pow(x-1.0/math.sqrt(float(n)),2.0)
        s2 = s2 + pow(x+1.0/math.sqrt(float(n)),2.0)

    target = []
    target.append(1.0 - math.exp(-s1))
    target.append(1.0 - math.exp(-s2))
    return target

def Kursawe(x_list):
    # -5 <= xi <= 5, i = 3
    f1,f2 = 0.0,0.0
    for i in range(0,2) :
        f1 = f1 - 10*math.exp(-0.2*math.sqrt(pow(x_list[i],2.0)+pow(x_list[i+1],2.0)))
    for i in range(0,3) :
        f2 = f2 + pow(abs(x_list[i]),0.8) + 5*math.sin(pow(x_list[i],3.0))
    target = [f1,f2]
    return target

def Binh_and_Korn(x_list):
    # 0 <= x <=5, 0 <= y <= 3
    x = x_list[0]
    y = x_list[1]
    f1 = 4*pow(x,2) + 4*pow(y,2)
    f2 = pow(x-5,2)+pow(y-5,2)
    target = [f1,f2]
    return target

def Binh_and_Korn_constraints(x_list):
    # 0 <= x <=5, 0 <= y <= 3
    x = x_list[0]
    y = x_list[1]
    g1 = max(0, 25 - pow(x-5,2) - pow(y,2))
    g2 = max(0, pow(x-8,2)+pow(y+3,2) - 7.7)
    violation = [g1,g2]
    return violation

def Griewank(x_list):
    # -300 <= xi <= 300
    # global minimal is at [0,0,..] where value = 0
    x1 = 0.0
    x2 = 1.0
    for i,x in enumerate(x_list,1):
        x1 = x1 + x*x
        x2 = x2 * math.cos(x/math.sqrt(i))
    return x1/4000 - x2 + 1

def Rastrigrin(x_list):
    # -30 <= xi <= 30
    # global minimal is at [0,0,..] where value = 0
    x1 = 0.0
    for i,x in enumerate(x_list,1):
        x1 = x1 + x*x - 10*math.cos(2*math.pi*x) + 10
    return x1

def Rosenbrock(x_list):
    # -30 <= xi <= 30
    # global minimal is at [1,1,..] where value = 0
    x1 = 0.0
    for i in range(0,len(x_list)-1):
        x1 = x1 + 100*(x_list[i]*x_list[i]-x_list[i+1])*(x_list[i]*x_list[i]-x_list[i+1]) +\
             (1-x_list[i])*(1-x_list[i])
    return x1

def Ackley(x_list):
    # -5 <= xi <= 5
    # global minimal is at [0,0,..] where value = 0
    x1 = 0.0
    x2 = 0.0
    for i,x in enumerate(x_list,1):
        x1 = x1 + x*x
        x2 = x2 + math.cos(2*math.pi*x)
    x1 = -0.2*math.sqrt(x1/i)
    x2 = x2/i
    return -20*math.pow(math.e,x1) - math.pow(math.e,x2) + 22.7182818285

if __name__ == '__main__':
        
    print Ackley([0,0])

    fig = plt.figure()
    ax = Axes3D(fig)
    X = np.arange(-5, 5, 0.02)
    Y = np.arange(-5, 5, 0.02)
    Z = [ ([0]*len(Y)) for i in range(len(X)) ] # x rows y columns
    X, Y = np.meshgrid(X, Y)

    for i in range(0,len(Z)):
        for j in range(0,len(Z[0])):
            Z[i][j] = Ackley([X[i][j],Y[i][j]])
            
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.coolwarm,linewidth=2)
    plt.show()

