
# coding: utf-8

# In[17]:

"""
This is a model to explore the effect of the intergroup conflict escalation on the collective behavior of individuals' 
opinion dynamics.
The model coded here is a modified version of the bounded confidence with rejection mechanism model that was originally proposed 
by Huet et al (2008).
Please note that for values of m=1 and beta=1, the proposed model equals to Huet et al (2008).

Meysam Alizadeh
Department of Computational Social Science
George Mason University
March 2014
malizad2@gmu.edu
"""

# Importing necessary libraries
import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import scipy as sp
from scipy import stats


# In[39]:

"""
Defining constant variables
"""
mu = 0.3 # constriction factor used to limit the convergence velocity
delta = 1 # intolerance threshold
beta = 3 # conflict escalation intolerance coefficient
no_of_runs = 1 # Number of times the whole model will be run 
max_iter = 1000000 # maximum number of iteration at each run
no_of_agents = 1000
U = 0.2 # level of uncertainty
epsilon = 0.15 # minimum distance between agents to consider them in a same cluster
m = 5 # number of initial groupings
p = 0.1 # connectivity probability of the random network


# In[3]:

"""
Defining the psign function.
"""
def psign (x):
    if x >= 0:
        x = 1
    else:
        x = -1
    return x


# In[4]:

"""
Initialization of the Model.
We represent each person as an agent in our model.
Each agent has a following attributes:
    1) Opinion: a list containing 2 real random number between -1 and 1 
    2) Uncertainty (U): a list containing 2 real random number between 0 and 1 (here U is always set as 0.2)
"""
    
# Defining the init method: a special method that gets invoked when an object is instantiated
def init():
    global op1, op2, grouping, network, adj_mat
    op1 = [(-1 + 2 * random.random()) for agents in range(no_of_agents)]
    op2 = [(-1 + 2 * random.random()) for agents in range(no_of_agents)]
    grouping = [random.randint(1,m) for agents in range(no_of_agents)]
    network = nx.erdos_renyi_graph(no_of_agents,p)
    adj_mat = nx.adjacency_matrix(network)


# In[10]:

"""
Updating Rules
"""

def Interact():
    global op1, op2, grouping, network, adj_mat

    # Selecting two random agents among all agents that are immediate neighbor on the network
    
    while True:
        node1 = random.randint(0, no_of_agents - 1)
        node2 = random.randint(0, no_of_agents - 1)
        if (node1 != node2) and (adj_mat[node1,node2] == 1):
            break
        
    # Calculating new opinion based on opinion interaction rules

    op1_diff = abs (op1[node2] - op1[node1])
    op2_diff = abs (op2[node2] - op2[node1])
        
    if grouping[node1] == grouping[node2]: # check whether the two selected agents are from same group
            
        if op1_diff <= U and op2_diff <= U:
            op1[node1] = op1[node1] + mu * (op1[node2] - op1[node1])
            op2[node1] = op2[node1] + mu * (op2[node2] - op2[node1])
            op1[node2] = op1[node2] + mu * (op1[node1] - op1[node2])
            op2[node2] = op2[node2] + mu * (op2[node1] - op2[node2])
    
        elif op1_diff > U and op2_diff <= U and op1_diff <= (1 + delta) * U:
            op2[node1] = op2[node1] + mu * (op2[node2] - op2[node1])       
            op2[node2] = op2[node2] + mu * (op2[node1] - op2[node2]) 
                
        elif op1_diff <= U and op2_diff > U and op2_diff <= (1 + delta) * U:       
            op1[node1] = op1[node1] + mu * (op1[node2] - op1[node1])
            op1[node2] = op1[node2] + mu * (op1[node1] - op1[node2])
                
        elif op1_diff > U and op2_diff <= U and op1_diff > (1 + delta) * U:
            op2[node1] = op2[node1] - mu * psign(op2[node2] - op2[node1]) * (U - op2_diff)
            op2[node2] = op2[node2] - mu * psign(op2[node1] - op2[node2]) * (U - op2_diff)            
    
        elif op1_diff <= U and op2_diff > U and op2_diff > (1 + delta) * U:
            op1[node1] = op1[node1] - mu * psign(op1[node2] - op1[node1]) * (U - op1_diff)
            op1[node2] = op1[node2] - mu * psign(op1[node1] - op1[node2]) * (U - op1_diff)
            
    else: # if agents are not from the same group
        
        if op1_diff <= U and op2_diff <= U:
            op1[node1] = op1[node1] + mu * (op1[node2] - op1[node1])
            op2[node1] = op2[node1] + mu * (op2[node2] - op2[node1])
            op1[node2] = op1[node2] + mu * (op1[node1] - op1[node2])
            op2[node2] = op2[node2] + mu * (op2[node1] - op2[node2])
                
        elif op1_diff > U and op2_diff <= U and op1_diff > (1 + delta) * U:
            op2[node1] = op2[node1] - beta * mu * psign(op2[node2] - op2[node1]) * (U - op2_diff)
            op2[node2] = op2[node2] - beta * mu * psign(op2[node1] - op2[node2]) * (U - op2_diff)            
    
        elif op1_diff <= U and op2_diff > U and op2_diff > (1 + delta) * U:
            op1[node1] = op1[node1] - beta * mu * psign(op1[node2] - op1[node1]) * (U - op1_diff)
            op1[node2] = op1[node2] - beta * mu * psign(op1[node1] - op1[node2]) * (U - op1_diff)
        
# bounding the opinions between -1 and 1
    if abs(op1[node1]) > 1: op1[node1] = psign(op1[node1])
    if abs(op1[node2]) > 1: op1[node2] = psign(op1[node2])
    if abs(op2[node1]) > 1: op2[node1] = psign(op2[node1])
    if abs(op2[node2]) > 1: op2[node2] = psign(op2[node2])
