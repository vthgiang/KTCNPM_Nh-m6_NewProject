from queue import Queue
from functools import cmp_to_key
import matplotlib.pyplot as plt
import numpy as np
import copy 

from distribution import Distribution
from constant import *


class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

class Solver:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.best_mu = 1e9
        self.res = None

    def calc(self, group_id, partition):
        dis_res = []
        for group in partition:
            now = None
            for u in group:
                foo = copy.deepcopy(self.nodes[u])
                for edge in edges:
                    if edge.v == u and group_id[edge.u] >= group_id[u]:
                        foo = foo.add(Distribution.from_mu_sigma(edge.w, 0.01, edge.w * 2))

                foo = foo.div(NUM_TEAM)
                if now is None:
                    now = foo
                else:
                    now = now.max(foo)
            
            if len(dis_res) > 0:
                now = now.add(dis_res[-1])
            
            dis_res.append(now)

        if (dis_res[-1].mu < self.best_mu):
            print(partition)
            print(dis_res[-1].mu)
            self.best_mu = dis_res[-1].mu
            self.res = (copy.deepcopy(partition), dis_res)

    def dfs(self, group_id, partition):
        if all(x >= 0 for x in group_id):
            self.calc(group_id, partition)
            return

        first = -1
        for i in range(len(self.nodes)):
            if group_id[i] >= 0:
                continue
            if first == -1:
                first = i

            # create a new group
            if first == i and (len(partition) == 0 or len(partition[-1]) == MAX_GROUP_SIZE):
                group_id[i] = len(partition)
                partition.append([])
                partition[-1].append(i)
                self.dfs(group_id, partition)
                partition.pop()
                group_id[i] = -1

            # add to the last group
            if len(partition) > 0 and len(partition[-1]) < MAX_GROUP_SIZE and partition[-1][-1] < i:
                group_id[i] = len(partition) - 1 
                partition[-1].append(i)
                self.dfs(group_id, partition)
                partition[-1].pop()
                group_id[i] = -1

    # @return (partition[][], distributions[])
    def solve(self):
        self.best_mu = 1e9
        self.res = None
        partition = []
        group_id = np.full(len(self.nodes), -1, dtype=int)
        self.dfs(group_id, partition)
        return self.res

nodes = []
edges = []

with open("dist2.txt") as f:
    lines = [line.rstrip() for line in f]
    pdf = []
    for line in lines:
        tokens = [float(x.strip()) for x in line.split(' ')]
        pdf.append(tokens[1])
    pdf = np.array(pdf)
    dis = Distribution(pdf)
    for i in range(12):
        nodes.append(copy.deepcopy(dis))

# print(nodes[0].mu)
# plt.plot(nodes[1].pdf, label = "a")
# plt.legend()
# plt.show()

# with open('module_names.txt') as f:
#     lines = [line.rstrip() for line in f]
#     for line in lines:
#         tokens = [x.strip() for x in line.split('\t')]
#         nodes.append(Distribution.from_mu_sigma(int(tokens[2]), int(tokens[3])))

with open('module_relations.txt') as f:
    lines = [line.rstrip() for line in f]
    for line in lines:
        tokens = [int(x.strip()) for x in line.split('\t')]
        edges.append(Edge(tokens[0] - 1, tokens[1] - 1, tokens[2]))

solver = Solver(nodes, edges)

(partition, distributions) = solver.solve()
print(partition)
print(distributions[-1].mu)