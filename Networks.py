'''
this file contains 5 types of networks:
    1. watts_strogatz_graph
    2. self-balancing tree
    3. channel network
    4. complete graph
    5. barbell graph
'''

import networkx as nx
import matplotlib.pyplot as plt
import sys
import random

class NetWorks:
    def small_world(n, k, p):
        if (k >= n):
            sys.exit("k cannot be larger than the total amount of nodes n")

        G = nx.Graph()
        nodes = list(range(n))
        # connect each node to k/2 neighbors
        for j in range(1, k // 2+1):
            targets = nodes[j:] + nodes[0:j] # first j nodes are now last in list
            G.add_edges_from(zip(nodes,targets))
        # rewire edges from each node
        # loop over all nodes in order (label) and neighbors in order (distance)
        # no self loops or multiple edges allowed
        for j in range(1, k // 2+1): # outer loop is neighbors
            targets = nodes[j:] + nodes[0:j] # first j nodes are now last in list
            # inner loop in node order
            for u,v in zip(nodes,targets):
                if random.random() < p:
                    w = random.choice(nodes)
                    # Enforce no self-loops or multiple edges
                    while w == u or G.has_edge(u, w):
                        w = random.choice(nodes)
                        if G.degree(u) >= n-1:
                            break
                    else:
                        G.remove_edge(u,v)
                        G.add_edge(u,w)
        return G

    def balanced_tree(r, h):
        n=0
        for i in range(h):
            n+=r**i
        G = nx.empty_graph(n)
        for j in range(n):
            for k in range(r):
                G.add_edge(j, r*j+k+1)

        return G

    # Channel Graph
    # n must be greater than r
    def channel(n, r):
        G = nx.empty_graph(n)
        for i in range(0, n, r):
            for j in range(r):
                for k in range(r):
                    G.add_edge(i+j, i+j+r-k)
        return G

    # Complete Graph
    def complete_graph(n):
        G = nx.empty_graph(n)
        for i in range(n):
            for j in range(n):
                if i!=j:
                    G.add_edge(i, j)
        return G

    # Barbell Graph
    def barbell_graph(m, n):
        G = nx.empty_graph(m+n)
        for i in range(m):
            for j in range(m):
                if i != j:
                    G.add_edge(i, j)
        for k in range(n):
            for l in range(n):
                if k!=l:
                    G.add_edge(k+m, l+m)
        G.add_edge(m-1, m)
        return G

#tests below
# G=NetWorks.small_world(100, 2, .5)
# G=NetWorks.balanced_tree(2,5)
# G=NetWorks.channel(60, 4)
# G=NetWorks.complete_graph(10)
# G=NetWorks.barbell_graph(10, 10)
# nx.draw(G)
# plt.draw()
# plt.show()
