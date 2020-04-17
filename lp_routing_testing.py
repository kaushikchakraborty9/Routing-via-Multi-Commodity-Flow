import matplotlib
matplotlib.use('TkAgg')
import networkx as nx
from pulp import *
from random import seed
from random import randint
from Grap_reading import graph_read, Mod_net


Arcs=[]
D = []                                      #Modified demand set
dem=4                                       #Total number of demands
min_len=6                                   #minimum path length
length=[]                                   #path length constraint
D_acc=[]                                    #Actual demand set
q=0.5                                       # BSM success probability

Aff=[]                                      #Variables for the LP objective function
vars=[]                                     #LP variables

G = graph_read('Surfnet.graphml.xml')       #Reading the graph
n = len(list(G.nodes()))
#Seed for generating random numbers
seed(85)

for (i, j) in G.edges():
    Arcs.append((i, j, list(G.edges[i, j].values())[0]))
max_len=10
(Nodes_mod,Arcs_mod) = Mod_net(G,max_len)   #Create the modified network
N = len(Nodes_mod)                          #Total number of nodes in the modified network
G_mod = nx.DiGraph()                        #Modified network
G_mod.add_nodes_from(Nodes_mod)
G_mod.add_weighted_edges_from(Arcs_mod)

# Demand Creation
for i in range(dem):
    s = 1
    t = 1
    l = randint(min_len, max_len)
    while s==t:
        s = randint(1, n )
        t = randint(1, n )
        D_acc.append((s,t))
    for k in range(l):
        D.append(((s-1)*(max_len+1)+1, (t-1)*(max_len+1)+k+2))
        length.append(k+1)
print("Demands: ",D_acc)
print("Modified Demand: ", D)
print("Lengths: ", length)
tot_dem = len(D)


sum_in=[None]*len(Nodes_mod)*tot_dem
sum_out=[None]*len(Nodes_mod)*tot_dem


# Creates the boundless Variables as real numbers
for k in range(tot_dem):
    temp_vars=[]

    for (i,j,w) in Arcs_mod:
        x = LpVariable((i,j,k),lowBound = 0,upBound = w,cat='Continuous')
        temp_vars.append((i,j,k,x))

        if(i==D[k][0]):
            Aff.append((x, q**(length[k]-1)))

    vars.append(temp_vars)


# Creates the 'prob' variable to contain the problem data
prob = LpProblem("Routing Problem",LpMaximize)

# Creates the objective function

flow = LpAffineExpression(Aff)
print(flow)
prob += flow, "Total Rate"

# Creates all problem constraints - this ensures the amount going into each node is at least equal to
# the amount leaving

for k in range(tot_dem):
    s = D[k][0]
    t = D[k][1]
    for v in Nodes_mod:

        if(v!= s and v!=t):
            sum_out[k*N+v-1] = lpSum([x] for (i,j,l,x) in vars[k] if i==v and i!=t and j!=s)
            sum_in[k*N+v-1] = lpSum([x] for (i,j,l,x) in vars[k] if j==v and i!=t and j!=s)


# flow conservation
for k in range(tot_dem):
    s = D[k][0]
    t = D[k][1]
    for v in G_mod.nodes:
        if(v!=s and v!=t):
            prob += sum_in[k*N+v-1] == sum_out[k*N+v-1]

# capacity constraints
Arcs_undir=[]
for (u,v,w) in Arcs:
    if (u,v,w) not in Arcs_undir and (v,u,w) not in Arcs_undir:
        Arcs_undir.append((u,v,w))
edge_cap = [None]*len(Arcs)
for (u,v,w) in Arcs_undir:
    temp_var=[]
    for k in range(tot_dem):
        for m in range(max_len+1):
            for (i,j,l,x) in vars[k]:
                if ((i == (u - 1) * (max_len + 1) + m) and j == ((v - 1) * (max_len + 1) + m+1)) or (i == ((v - 1) * (max_len + 1) + m) and j == (u - 1) * (max_len + 1) + m+1):
                    temp_var.append(x)
    prob += lpSum([x] for x in temp_var) <= w






# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
non_zero_var =[]
for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)
        non_zero_var.append(v)

# The optimised objective function value is printed to the screen
print("Total Achievable Rate = ", value(prob.objective))

