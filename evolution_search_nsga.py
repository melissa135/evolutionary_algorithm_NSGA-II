import random
from evolution_lib import *
import matplotlib.pyplot as plt

p_size = 200
parameter_num = 2
target_num = 2
parameter_lower_bound = [ 0, 0 ]
parameter_upper_bound = [ 5, 3 ]

iteration = 100
prob_cross = 0.6
prob_mutaion = 0.05

if __name__ == '__main__':
    
    parents = initial_population(p_size,parameter_num,
                                 parameter_lower_bound,parameter_upper_bound)
    children = set()

    for it in range(1,iteration+1):
      
        all_population = parents | children
        fast_non_dominated_sort(all_population)
        calculate_crowd_dis(all_population)
       
        parents = set()
        front = 1
        while len(parents) < p_size:
            for ind in all_population:
                if ind.front_rank == front:
                    parents.add(ind)
                    if len(parents) == p_size :
                        break
            front = front + 1

        # draw the scatter diagram of population
        X,Y,C = [],[],[] 
        for p in parents:
            if True: #p.front_rank == 1 :
                X.append(p.target[0])
                Y.append(p.target[1])
                C.append(p.front_rank)
        plt.figure()
        plt.scatter(X,Y, s=10, c=C)
        plt.xlim(0,200), plt.xticks([])
        plt.ylim(0,80), plt.yticks([])
        plt.savefig('F:/scatter_'+str(it)+'.png',dpi=48)

        # calculate the indicator of population
        best = [float('inf') for i in range(0,target_num)]
        mean = [0 for i in range(0,target_num)]
        for p in parents:
            for i in range(0,target_num):
                if p.target[i] < best[i]:
                    best[i] = p.target[i]
                mean[i] = mean[i] + p.target[i]
        for i in range(0,target_num):
            mean[i] = mean[i]/p_size
        
        print 'the',it,'th generation'
        print 'best_target:',best,' mean_target:',mean

        children = genarate(p_size,parents,prob_cross,prob_mutaion)

