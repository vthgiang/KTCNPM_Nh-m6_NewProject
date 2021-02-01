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
		u = numbers[0]
		v = numbers[1]
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

def read_result(result_group, result_dist, G, color_map, dist_all, dist_sum):
	f_group = open(result_group, "r")
	f_dist = open(result_dist, "r")
	num_groups = sum(1 for line in open(result_group))
	for i in range(num_groups):
		color_map.append('black')
		dist_sum.append(0)
		dist_all.append(0)
	print(len(color_map))

	color_id = 0
	list_node = list(G.nodes())
	prev = -1
	new_node = chr(ord('A') - 1)
	while (1):
		line = f_group.readline()
		if (len(line) == 0):
			break;
		new_node = chr(ord(new_node) + 1)
		new_node_id = len(list_node) + ord(new_node) - ord('A')
		color_map[new_node_id] = COLOR_STRING[color_id]
		if (prev != -1):
			G.add_edge(prev, new_node)
		prev = new_node
		line = line.rstrip().replace("\n", "")
		numbers = line.split(" ");
		for number in numbers:
			index = list_node.index(number)
			color_map[index] = COLOR_STRING[color_id]
		color_id = color_id + 1
		line = f_dist.readline()
		dist_all[new_node_id] = get_array(line)
		line = f_dist.readline()
		dist_sum[new_node_id] = get_array(line)
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
			y = -1
		step = 0
		if (len(numbers) > 1):
			step = 2 / (len(numbers) - 1)
		for number in numbers:
			pos[number] = [x, y]
			y -= step
		x += 0.4
	print(pos)
	return pos

def read_module_names(file_name):
	return 0
