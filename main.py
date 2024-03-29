import math
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.w_in = 0
        self.w_out = 0

    def __repr__(self):
        return "(" + str(self.x) + "; " + str(self.y) + ")"

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.weight = 0
        self.to = end.x
        self.rotation = math.atan2(end.y - start.y, end.x - start.x)

    def __repr__(self):
        return str(edges.index(self))

def read_points(file_name):
    points = []
    input_array = open(file_name).read().split()

    i = 0
    while i < len(input_array):
        points.append(Point(int(input_array[i]), int(input_array[i + 1])))
        i += 2
    return points

def read_edges(file_name):
    edgs = []
    input_array = open(file_name).read().split()

    i = 0
    while i < len(input_array):
        edgs.append(Edge(vertices[int(input_array[i])], vertices[int(input_array[i + 1])]))
        i += 2
    return edgs

def plot_graph(vertices, edges, chains, point_to_find, point=None):
    p = find(point_to_find)
    if p == -1:
        for edge in edges:
            plt.plot([edge.start.x, edge.end.x], [edge.start.y, edge.end.y], color='black')
    else:
        for edge in edges:
            if edge in chains[p-1] or edge in chains[p]:
                plt.plot([edge.start.x, edge.end.x], [edge.start.y, edge.end.y], color='blue')  # Використовуємо синій колір для першого та другого ланцюгів
            else:
                plt.plot([edge.start.x, edge.end.x], [edge.start.y, edge.end.y], color='black')  # Решту ребер малюємо чорним

    for vertex in vertices:
        plt.scatter(vertex.x, vertex.y, color='red')

    if point:
        if point.x < vertices[0].x or point.x > vertices[-1].x or point.y < vertices[0].y or point.y > vertices[-1].y:
            plt.scatter(point.x, point.y, color='green')  # Якщо точка знаходиться поза графом - зелений
        else:
            plt.scatter(point.x, point.y, color='blue')  # Якщо точка знаходиться в межах графу - синій

    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graph')
    plt.grid(True)
    plt.show()




def sum_weight(array):
    result = 0
    for edge in array:
        result = result + edge.weight
    return result

def leftmost_edge(array):
    array = sort_edges(array)
    return array[0]

def leftmost_unused(array):
    i = 0
    result = array[0]
    while i < len(array):
        if array[i].weight > 0:
            result = array[i]
            break
        i += 1
    return result

def sort_edges(array):
    return sorted(array, key=lambda edge: edge.rotation, reverse=True)

def create_chain(chain_num):
    current_v = 0
    while current_v != n - 1:
        new_in_chain = leftmost_unused(ordered_edges_out[current_v])
        chains[chain_num].append(new_in_chain)
        new_in_chain.weight -= 1
        current_v = vertices.index(new_in_chain.end)

def find(point):
    for p in range(0, num_chains, 1):
        for e in chains[p]:
            if e.start.y < point.y < e.end.y:
                point_vector = Point(point.x - e.start.x, point.y - e.start.y)
                edge_vector = Point(e.end.x - e.start.x, e.end.y - e.start.y)
                if math.atan2(point_vector.y, point_vector.x) > math.atan2(edge_vector.y, edge_vector.x):
                    if p - 1 == -1:
                        return -1
                    else:
                        return p
    return -1


# Main code starts here
vertices = read_points("vertices.txt")
edges = read_edges("edges.txt")

# Sort vertices by y
vertices = sorted(vertices, key=lambda point: point.y)

# For every vertex, create a list of in- and outgoing edges
edges_in = []
edges_out = []

for v in vertices:
    edges_in.insert(vertices.index(v), [])
    edges_out.insert(vertices.index(v), [])

for e in edges:
    from_idx = vertices.index(e.start)
    to_idx = vertices.index(e.end)
    edges_out[from_idx].append(e)
    edges_in[to_idx].append(e)
    e.weight = 1

# Weight balancing
n = len(vertices)

# Bottom to top -------- first round
for i in range(1, n - 1):
    vertices[i].w_in = sum_weight(edges_in[i])
    vertices[i].w_out = sum_weight(edges_out[i])
    edges_out[i] = sort_edges(edges_out[i])
    # leftmost_from = leftmost_edge(edges_out[i])
    if vertices[i].w_in > vertices[i].w_out:
        edges_out[i][0].weight = vertices[i].w_in - vertices[i].w_out + 1

# Top to bottom -------- second round
for i in range(n - 1, 1, -1):
    vertices[i].w_in = sum_weight(edges_in[i])
    vertices[i].w_out = sum_weight(edges_out[i])
    edges_in[i] = sort_edges(edges_in[i])
    if vertices[i].w_out > vertices[i].w_in:
        edges_in[i][0].weight = vertices[i].w_out - vertices[i].w_in + edges_in[i][0].weight

# Chains creation
chains = []
num_chains = sum_weight(edges_out[0])

ordered_edges_out = []  # List of ordered outgoing edges for every vertex
for v in edges_out:
    v = sort_edges(v)
    ordered_edges_out.append(v)

for j in range(num_chains):
    chains.insert(j, [])
    create_chain(j)

point_to_find = Point(7, 10)
if find(point_to_find) == -1:
    print("point not in graph")
plot_graph(vertices, edges, chains, point_to_find, point_to_find)

