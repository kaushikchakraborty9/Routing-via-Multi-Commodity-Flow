#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import networkx as nx
import scipy as sp
from random import seed
from random import randint
import networkx as nx
# seed random number generator

def graph_plot(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes, node_color='r', node_size=500, alpha=0.8)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=1.0, alpha=0.5, edge_color='b')
    labels = nx.draw_networkx_labels(G, pos)
    plt.axis('off')
    plt.show()
    plt.draw()





def graph_read():


    H = nx.read_graphml('Surfnet.graphml.xml')
   # H = nx.read_graphml('SANET.graphml.xml')

    #for e in H.edges:
    #    print(e.values())

    max=400
    Nodes = list(H.nodes)
    #print(len(Nodes))
    Arcs = []
    Wt = []
    G=nx.DiGraph()

    for i in Nodes:
        G.add_node(int(i)+1)

    #graph_plot_adv(H)
    i=0
    seed(1)
    for (n,m,w) in H.edges:
        x= randint(1,max)
        Arcs.append((int(n)+1,int(m)+1,x))
        Arcs.append((int(m)+1, int(n)+1, x))

    #print(Arcs)



    G.add_weighted_edges_from(Arcs)







    #graph_plot(G)

    return G



def Mod_net(G,l):

    Nodes = []
    Arcs = []
    for i in G.nodes:
        for j in range(l+1):
            Nodes.append((i-1)*(l+1)+j+1)
    #print(G.edges())
    for (i,j) in G.edges():
        for k in range(l):

            Arcs.append(((i-1)*(l+1)+k+1,(j-1)*(l+1)+k+2,list(G.edges[i,j].values())[0]))
            #Arcs.append(( (j - 1) * (l + 1) + k + 2, (i - 1) * (l + 1) + k + 1, list(G.edges[i, j].values())[0]))

    return (Nodes,Arcs)







def draw_graph(G,D,paths):
    pos = nx.get_node_attributes(G, 'pos')
    repeater_nodes = []
    end_nodes = []
    col = ['r','g','b','c']
    for (i,j) in D:
        end_nodes.append(i)
        end_nodes.append(j)
        #end_nodes.append((i,j))
    for node in G.nodes():
        if node not in end_nodes:
            repeater_nodes.append(node)
  #      if G.nodes[node]['type'] == 'repeater_node':
  #          repeater_nodes.append(node)
  #          print(node.pos)
  #      else:
  #          end_nodes.append(node)
  #      i=i+1
    fig, ax = plt.subplots(figsize=(10, 7))
    k=0
    for (i,j) in D:
        ende_nodes = nx.draw_networkx_nodes(G=G, pos=pos, nodelist=[i,j], node_shape='s', node_size=700,
                                       node_color=col[k], label="End Node")
        ende_nodes.set_edgecolor('k')
        k=k+1
    rep_nodes = nx.draw_networkx_nodes(G=G, pos=pos, nodelist=repeater_nodes, node_size=600,
                                       node_color=[[0 / 255, 166 / 255, 214 / 255]], label="Repeater Node")
    rep_nodes.set_edgecolor('k')
    nx.draw_networkx_labels(G=G, pos=pos, font_size=18, font_weight="bold")
    sp_edge=[]

    nx.draw_networkx_edges(G=G, pos=pos, width=1)
    nx.draw_networkx_edges(G=G, pos=pos, edgelist = paths, width=4)

    plt.axis('off')
    margin = 0.33
    fig.subplots_adjust(margin, margin, 1. - margin, 1. - margin)
    ax.axis('equal')
    fig.tight_layout()
    plt.show()












def graph_plot_adv(D,paths):
    pos = {}
    map = {}
    color_map = []
    end_node_list =[]
    for (i,j) in D:
        end_node_list.append(i)
        end_node_list.append(j)
        #end_node_list.append((i,j))

    G = nx.read_gml('Surfnet.gml')

    H = nx.Graph()
    i=1
    for node, nodedata in G.nodes.items():
        #print(i,nodedata)
        #pos[node] = [nodedata['Longitude'], nodedata['Latitude']]
        if i ==13:
            pos[i] = [nodedata['Longitude']+0.2, nodedata['Latitude']]
        elif i == 40:
            pos[i] = [nodedata['Longitude'] - 0.2, nodedata['Latitude']]
        elif i == 45:
            pos[i] = [nodedata['Longitude'] + 0.2, nodedata['Latitude']]
        elif i == 38:
            pos[i] = [nodedata['Longitude'] - 0.2, nodedata['Latitude']-0.2]
        elif i == 24:
            pos[i] = [nodedata['Longitude'], nodedata['Latitude'] - 0.2]
        elif i == 23:
            pos[i] = [nodedata['Longitude']+0.2, nodedata['Latitude'] - 0.3]
        elif i == 15:
            pos[i] = [nodedata['Longitude'], nodedata['Latitude'] - 0.2]
        elif i == 34:
            pos[i] = [nodedata['Longitude']-0.3, nodedata['Latitude']+0.17]
        elif i == 33:
            pos[i] = [nodedata['Longitude']-0.15, nodedata['Latitude']]
        elif i == 35:
            pos[i] = [nodedata['Longitude']-0.15, nodedata['Latitude'] + 0.2]
        else:
            pos[i] = [nodedata['Longitude'], nodedata['Latitude']]
        map[node] =i
        H.add_node(i)
        if i in end_node_list:
            color_map.append('green')
            nodedata['type'] = 'end_node'
        else:
            color_map.append([30 / 255, 144 / 255, 255 / 255])
            nodedata['type'] = 'repeater_node'
        i=i+1

    for (u,v) in G.edges:
        H.add_edge(map[u],map[v])
    nx.set_node_attributes(G, pos, name='pos')

    nx.set_node_attributes(H,pos,name = 'pos')

    draw_graph(H,D,paths)

