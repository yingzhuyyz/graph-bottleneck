import networkx as nx
import matplotlib.pyplot as pl
import random
import numpy

def mk_graph():
    N1 = 100
    N2 = 100
    conn_degree = 2

    # Generate two random graphs (disjoint)
    g1 = nx.fast_gnp_random_graph(N1, 0.1)
    g2 = nx.relabel_nodes(
            nx.fast_gnp_random_graph(N2, 0.05),
            lambda x: x+N1)
    g  = nx.compose(g1, g2)

    # Connect them by conn_degree
    V1 = list(g1.nodes())
    V2 = list(g2.nodes())
    u1 = random.sample(V1, conn_degree)
    u2 = random.sample(V2, conn_degree)
    for n1, n2 in zip(u1, u2):
        g.add_edge(n1, n2)

    # intializes the weights of edges and nodes
    for e in g.edges():
        g.get_edge_data(*e)['w'] = 0
    for n in g.nodes():
        g.node[n]['w'] = 0

    return g


def random_conn(g):
    V = list(g.nodes())
    u = random.choice(V)
    v = random.choice(V)
    path = nx.shortest_path(g, u, v)
    for i in range(len(path)-1):
        g.get_edge_data(path[i], path[i+1])['w'] += 1
    for n in path:
        g.node[n]['w'] += 1

def get_edge_color(g):
    edges = g.edges()
    ws = [g.get_edge_data(*e)['w'] for e in edges]
    max_w = max(ws)
    return [w / max_w for w in ws]

def get_node_size(g, vmin, vmax):
    nodes = g.nodes()
    ws = [g.node[n]['w'] for n in nodes]
    max_w = max(ws)
    return [vmin + (w/max_w)*(vmax-vmin) for w in ws]

g = mk_graph()
Nv = len(g.nodes())
Ne = len(g.edges())

# Simulation
for i in range(100):
    random_conn(g)

# Plot the graph
pl.figure()
cmap = pl.get_cmap("Greys")
nx.draw(g,
    node_size = get_node_size(g, 0, 200),
    edge_color = get_edge_color(g),
    edge_vmin = 0,
    edge_vmax = 1,
    edge_cmap = cmap,
    alpha = 0.2
    )
pl.savefig('a.png')
