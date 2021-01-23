import networkx as nx
from constant import *

def read_distribution_node(file_name):
	with open(file_name) as f:
	    lines = [line.rstrip() for line in f]
	    pdf = []
	    for line in lines:
	        tokens = [float(x.strip()) for x in line.split(' ')]
	        pdf.append(tokens[1])
	    pdf = np.array(pdf)
	    dis = Distribution(pdf)
	    return dis

def read_graph(file_name):
	graph = nx.DiGraph(directed=True)
	f = open(file_name, "r")
	while (1):
		line = f.readline()
		if (len(line) == 0):
			break;
		numbers = line.split("\t");
		u = int(numbers[0])
		v = int(numbers[1])
		w = numbers[2]
		graph.add_edge(u, v, weight = w)
	return graph

def get_array(line):
	dist = [float(x) for x in line.split()]
	sum = []
	s = 0
	for x in dist:
		s = s + x
		sum.append(s)
		if (s >= 0.99):
			break;
	return sum

def read_result(file_name, G, color_map, dist_all, dist_sum):
	f = open(file_name, "r")
	color_id = 0
	list_node = list(G.nodes())
	prev = -1
	new_node = 12
	while (1):
		line = f.readline()
		if (len(line) == 0):
			break;
		new_node = new_node + 1
		if (prev != -1):
			G.add_edge(prev, new_node)
		color_map[new_node - 1] = COLOR_STRING[color_id]
		prev = new_node
		line = line.rstrip().replace("\n", "")
		numbers = line.split(" ");
		for number in numbers:
			number = int(number)
			index = list_node.index(number)
			color_map[index] = COLOR_STRING[color_id]
		color_id = color_id + 1
		line = f.readline()
		dist_all[new_node] = get_array(line)
		line = f.readline()
		dist_sum[new_node] = get_array(line)
	print(color_map)

def read_dist_from_file(file_name):
	f = open(file_name, "r")
	dist = []
	while (1):
		line = f.readline()
		if (len(line) == 0):
			break;
		dist.append(float(line.split(" ")[1]))
	sum = []
	s = 0
	for x in dist:
		s = s + x
		sum.append(s)
		if (s >= 0.99):
			break
	return sum

def read_pos(file_name):
	f = open(file_name, "r")
	x = -1
	pos = dict()
	while (1):
		line = f.readline()
		if (len(line) == 0):
			break;
		line = line.replace("\n", "")
		numbers = line.split(" ")
		y = 1
		if (len(numbers) == 1):
			y = 0
		step = 0
		if (len(numbers) > 1):
			step = 2 / (len(numbers) - 1)
		for number in numbers:
			number = int(number)
			pos[number] = [x, y]
			y -= step
		x += 0.4
	return pos

def read_module_names(file_name):
	return 0
