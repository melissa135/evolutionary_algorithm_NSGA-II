import numpy as np
import random
from function_utils import *
from evolution_search_nsga import parameter_lower_bound,parameter_upper_bound

class individual(object):

    def __init__(self,temp):
        self.parameter = temp[:]
        self.target = get_target(self.parameter)
        self.violation = get_violation(self.parameter)
        self.front_rank = 0
        self.domination_counter = 0
        self.crowding_distance = 0
        self.set = set()

    def show(self):
        print self.parameter,self.target
        

def get_target(parameter):
    return Binh_and_Korn(parameter)


def get_violation(parameter):
    return Binh_and_Korn_constraints(parameter)


def initial_population(p_size,para_num,lower_bound,upper_bound):
    population = []
    for i in range(0,p_size):
        temp = []
        for j in range(0,para_num):
            lb = lower_bound[j]
            ub = upper_bound[j]
            temp.append(random.uniform(lb,ub))
        ind = individual(temp)
        population.append(ind)
    return set(population) 


def is_dominate(p,q):
    dominate = False
    
    for i in range(0,len(p.target)):
        if p.target[i] > q.target[i] :
            return False
        if p.target[i] < q.target[i] :
            dominate = True
            
    for i in range(0,len(p.violation)):
        if p.violation[i] > q.violation[i] :
            return False
        if p.violation[i] < q.violation[i] :
            dominate = True
            
    return dominate


def fast_non_dominated_sort(population):
    f_set = set()
    rank = 1
    for p in population:
        for q in population:
            if p is q :
                continue
            if is_dominate(p,q):
                p.set.add(q)
            elif is_dominate(q,p):
                p.domination_counter = p.domination_counter + 1
        if p.domination_counter == 0 :
            p.front_rank = rank
            f_set.add(p)

    while not len(f_set)==0 :
        rank = rank + 1
        temp_set = set()
        for p in f_set :
            for q in p.set :
                q.domination_counter = q.domination_counter - 1
                if q.domination_counter==0 and q.front_rank==0 :
                    q.front_rank = rank
                    temp_set.add(q)
        f_set = temp_set


def calculate_crowd_dis(population,parameter_num):
    infinite = 100000.0 # a large number as infinte
    
    for dim in range(0,parameter_num):
        new_list = sort_by_coordinate(population,dim)
        
        new_list[0].crowding_distance += infinite
        new_list[-1].crowding_distance += infinite
        max_distance = new_list[0].parameter[dim] - new_list[-1].parameter[dim]
        for i in range(1,len(new_list)-1):
            distance = new_list[i-1].parameter[dim] - new_list[i+1].parameter[dim]
            if max_distance == 0 :
                new_list[i].crowding_distance = 0
            else :
                new_list[i].crowding_distance += distance/max_distance
            
    for p in population :
        p.crowding_distance = p.crowding_distance/parameter_num


def sort_by_coordinate(population,dim): # selection sort, which can be replaced with quick sort
    p_list = []
    for p in population:
        p_list.append(p)

    for i in range(0,len(p_list)-1):
        for j in range(i+1,len(p_list)):
            if p_list[i].parameter[dim] < p_list[j].parameter[dim]:
                temp = p_list[i]
                p_list[i] = p_list[j]
                p_list[j] = temp
                
    return p_list


def tournment_select(prarents,part_num=2): # binary tournment selection
    
    participants = random.sample(prarents, part_num)
    best = participants[0]
    best_rank = participants[0].front_rank
    best_crowding_distance = participants[0].crowding_distance
    
    for p in participants[1:] :
        if p.front_rank < best_rank or \
           (p.front_rank == best_rank and p.crowding_distance > best_crowding_distance):
            best = p
            best_rank = p.front_rank
            best_crowding_distance = p.crowding_distance
            
    return best


def genarate(p_size,prarents,cross_prob,mutation_prob):
    # generate two children from two parents
    
    children = set()
    while len(children) < p_size:
        parent1 = tournment_select(prarents)
        parent2 = tournment_select(prarents)
        while parent1 == parent2 :
            parent2 = tournment_select(prarents)
            
        child1,child2 = cross(parent1,parent2,cross_prob)
        child1 = mutation(child1,mutation_prob)
        child2 = mutation(child2,mutation_prob)

        children.add(child1)
        children.add(child2)
    return children


def cross(p1,p2,prob): # the random linear operator
    if random.uniform(0,1) >= prob:
        return p1,p2
    
    parameter1,parameter2 = [],[]
    linear_range = 2
    alpha = random.uniform(0,linear_range)
    for j in range(0,len(p1.parameter)):
        parameter1.append(alpha*p1.parameter[j] +
                          (1-alpha)*p2.parameter[j] )
        parameter2.append((1-alpha)*p1.parameter[j] +
                          alpha*p2.parameter[j] )
    c1 = individual(parameter1)
    c2 = individual(parameter2)
    return c1,c2


def mutation(p,prob): # uniform random mutation

    mutation_space = 0.1
    parameter = []
    for i in range(0,len(p.parameter)):
        if random.uniform(0,1) < prob:
            para_range = mutation_space*(parameter_upper_bound[i]-parameter_lower_bound[i])
            mutation = random.uniform(-para_range,para_range)
            parameter.append(p.parameter[i]+mutation)
        else :
            parameter.append(p.parameter[i])

    p_new = individual(parameter)            
    return p_new
