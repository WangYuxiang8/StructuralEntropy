"""
    author: wangyuxiang
    date: 2021-2-27

    结构熵极小化算法，包含：
        - 一维结构熵极小化算法
        - 二维结构熵极小化算法
        - 三维结构熵极小化算法
"""
from StructuralEntropy.algorithm.priority_tree import compute_structural_entropy_of_node

class HighDimensionalStructureEntropyAlgorithm(object):

    def __init__(self, graph):
        self.vertice_degree_list = graph.get_vertice_degree_list()
        self.degree_sum = graph.get_degree_sum()
        self.vertice_number = graph.get_vertices_number()
        self.cut_set = dict()                           # {TwoCommunity: Float}
        self.vertice_connect_edge_list = list()         # [{string: Float}, {string: Float}]

        for i in range(self.vertice_number + 1):
            self.vertice_connect_edge_list.append(dict())

        for i in range(1, self.vertice_number + 1):
            edge_of_node_i = graph.get_vertice_connect_edge_list()[i]       # 结点i所连边的set
            '''
            每个结点i对应一个dict，保存了结点i的邻居结点以及对应边的权重
                i: {
                    "k_1": w1,
                    "k_2": w2,
                    ...
                    "k_n": wn
                } 
            其中k_1表示结点i的邻居结点，w1表示对应edge_i_to_k_1边的权重
            '''
            d = dict()
            for e in edge_of_node_i:
                d[str(e.get_dst_id())] = e.get_weight()
            self.vertice_connect_edge_list[i] = d

        '''
        初始化cut_set，获取所有只包含两个结点的community，以及对应的weight（前提是两个结点相连）
        '''
        for i in range(1, self.vertice_number):
            edge_dict_of_nodei = self.vertice_connect_edge_list[i]
            for j in range(i + 1, self.vertice_number + 1):
                if edge_dict_of_nodei.get(str(j)):
                    comi = set()
                    comi.add(str(i))
                    comj = set()
                    comj.add(str(j))
                    two_community = self.TwoCommunity(comi, comj)
                    gij = edge_dict_of_nodei[str(j)]       # 两个社区之间的割边数
                    self.cut_set.setdefault(two_community, gij)

    '''
        最大高度为1的编码树，也就是只有一层叶子节点，此时相当于整个图没有做划分
        一维结构熵等价于度分布的香农熵
    '''
    def one_dimension(self):
        SE = 0.0
        for i in range(1, self.vertice_number + 1):
            SE += compute_structural_entropy_of_node(self.vertice_degree_list[i],
                                                     self.degree_sum,
                                                     self.vertice_degree_list[i],
                                                     self.degree_sum)
        return SE

    def two_dimension(self):
        pass

    def three_dimension(self):
        pass

    class TwoCommunity(object):

        def __init__(self, comi, comj):
            self.comi = comi        # set(string, string, ... , string)
            self.comj = comj

        def __str__(self):
            return "TwoCommunity [comi=" + str(self.comi) + ", comj=" + str(self.comj) + "]"

    # 测试程序
    def print_cut_set(self):
        print("----------Test cut set-----------")
        print("Size of cut set: %d" % len(self.cut_set))
        for k, v in self.cut_set.items():
            print("Community = %s, weight = %f" % (k, v))
