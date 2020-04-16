
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import networkx as nx
import scipy as sp
from random import seed
from random import randint
import networkx as nx



def graph_read():

"""Read the input graph from a .graphml.xml file. Here we consider the 'Surfnet.graphml.xml' as the input file."""
    H = nx.read_graphml('Surfnet.graphml.xml')

    max=400
    Nodes = list(H.nodes)
    #print(len(Nodes))
    Arcs = []
    Wt = []
    G=nx.DiGraph()

    for i in Nodes:
        G.add_node(int(i)+1)

    i=0
    seed(1)
    for (n,m,w) in H.edges:
        x= randint(1,max)
        Arcs.append((int(n)+1,int(m)+1,x))
        Arcs.append((int(m)+1, int(n)+1, x))

    G.add_weighted_edges_from(Arcs)
    return G




def Mod_net(G,l):
    
"""Modify the original network G for applying the length constrained multi-commodity flow formulation. 
For each node u in the original graph G = (V,E,C) we create l+1 copies of u. They are u+0, ... , u+l. 
If two nodes u,v in the original network G is connected by an edge (u,v), then in the modified network G'=(V',E',C') 
we will have the following edges,
(u+0,v+1), (u+1,v+2), ... (u+(l-1),v+l)."""

    Nodes = []
    Arcs = []
    for i in G.nodes:
        for j in range(l+1):
            Nodes.append((i-1)*(l+1)+j+1)
    for (i,j) in G.edges():
        for k in range(l):

            Arcs.append(((i-1)*(l+1)+k+1,(j-1)*(l+1)+k+2,list(G.edges[i,j].values())[0]))

    return (Nodes,Arcs)




