#!/usr/bin/python

import sys
import numpy as np
import networkx as nx

out_mixed = open(sys.argv[1])
out_norm = open(sys.argv[2], 'w')

w_edges = []
for e in out_mixed:
    w_edges.append(e.strip().split())

edges = []
for e in w_edges:
    edges.append((e[0], e[1]))

g = nx.Graph(edges)
deg = g.degree()

for e in w_edges:
    out_norm.write(' '.join(map(str, [e[0], e[1], (int(e[2]) - 1) / (deg[e[0]] + deg[e[1]])])) + '\n')

out_mixed.close()
out_norm.close()