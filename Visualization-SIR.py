import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
from Networks import NetWorks

# Graph Initialization
# Depending on the compexlity of your network, the total number of nodes should not exceed 4000, exceeding the threshold may cause computer to crash
# restart computer if told cannot allocate memory

n=2000
G=NetWorks.small_world(n, 3, .5)

# r, h=2, 8
# G=NetWorks.balanced_tree(r,h)

# n = 800
# G=NetWorks.channel(500, 4)

# n = 100
# G=NetWorks.complete_graph(100)

# m, n=50, 80
# G=NetWorks.barbell_graph(100, 200)

pos = nx.spring_layout(G)

# SIR - Simulate Disease Spread
def SIR (G, r0, ti, k, days):
    initial_adopters = np.random.choice(len(list(G)), k, replace=False)
    initial_adopters = initial_adopters.tolist()
    s = []
    s.append(list(set(list(G)) - set(initial_adopters)))
    i = []
    i.append(initial_adopters)
    r = []
    r.append(initial_adopters)
    r_temp=[]
    r_temp.append(initial_adopters)
    t = 0
    e = [[]]
    while t<days:
        if len(i[t])==0 or len(i[t])==len(list(G)):
            break
        new_adopters = []
        new_edges = []
        for node in i[t]:
            neighbors = list(G.neighbors(node))
            p = r0 / len(neighbors)
            for neighbor in neighbors:
                if neighbor in s[t] and neighbor not in new_adopters and random.random() < p:
                    new_adopters.append(neighbor)
                    edge=(node, neighbor)
                    new_edges.append(edge)
        e.append(e[t] + new_edges)
        s.append(list(set(s[t]) - set(new_adopters)))
        i.append(i[t] + new_adopters)
        r.append(r[t]+new_adopters)
        r_temp.append(new_adopters)
        t += 1
        if t>= ti:
            i[t] = list(set(i[t]) - set(r_temp[t - ti]))
    return t, s, i, r, e

Basic_Reproduction_Numbers = {'Measles':12, "COVID-19":2.7, "SARS":3, "MERS":.8, "COMMON_COLD":2.4}
r0 = Basic_Reproduction_Numbers.get("COVID-19")

k = 5
ti=2
days=90

t, s, i, r, e=SIR(G, r0, ti, k, days)

# Build Plot
fig, ax = plt.subplots(figsize=(160,90))

def update(frame):
    ax.clear()
    # Susceptible nodes
    nx.draw_networkx_edges(G, pos=pos, ax=ax, edge_color="gray")
    if len(s[frame])>0:
        susceptible_nodes = nx.draw_networkx_nodes(G, pos=pos, nodelist=s[frame], node_size=50, node_color="green",  ax=ax)
        susceptible_nodes.set_edgecolor("black")

    # Infectious nodes
    if len(i[frame]) > 0:
        infectious_nodes = nx.draw_networkx_nodes(G,pos=pos, nodelist=i[frame], node_size=50, node_color="red", ax=ax)
        infectious_nodes.set_edgecolor("black")

    # Removed nodes
    if frame>=ti:
        removed_nodes = nx.draw_networkx_nodes(G,pos=pos, nodelist=r[frame-ti], node_size=50, node_color="grey", ax=ax)
        removed_nodes.set_edgecolor("black")

    # Infectious edges
    nx.draw_networkx_edges(G, pos=pos, edgelist=e[frame], width=1.5, ax=ax)
    ax.set_title("SIR Model" + " Day " + str(frame + 1), fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])


ani = matplotlib.animation.FuncAnimation(fig, update, frames=t+1, interval=500, repeat=False)
plt.show()
