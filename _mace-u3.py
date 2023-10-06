#!/usr/bin/python

import sys

r = open(sys.argv[1])
w = open(sys.argv[2], 'w')

for clique in r:
    if len(clique.split()) == 3:
        w.write(clique)

r.close()
w.close()