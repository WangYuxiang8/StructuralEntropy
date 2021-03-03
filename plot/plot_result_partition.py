"""
    author: wangyuxiang
    date: 2021-3-3

    对划分结果进行可视化
"""
from graphviz import *

color_list = ['#FFB6C1', '#DC143C', '#0000FF', '#00BFFF', '#32CD32', '#FFA500',
              '#B22222', '#696969', '#FFDEAD', '#00FFFF', '#00008B']


def plot_graph(graph, filename):
    vertice_list = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(',')[:-1]
            vertice_list.append(line)
    edges_list = set()
    for i in range(1, graph.vertices_number + 1):
        edges_of_nodei = graph.vertice_connect_edge_list[i]
        for edge in edges_of_nodei:
            e = (str(edge.get_dst_id()), str(i), str(edge.get_weight())[:4])
            if e not in edges_list:
                edges_list.add((str(i), str(edge.get_dst_id()), str(edge.get_weight())[:4]))
    g = Graph("partition result")

    for i in range(len(vertice_list)):
        vertice = vertice_list[i]
        color = color_list[i]
        for v in vertice:
            g.node(v, color=color, style='filled')
    # g.edges(list(edges_list))
    for e in edges_list:
        g.edge(e[0], e[1], label=e[2], color='gray')
    g.view()