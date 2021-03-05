"""
    author: wangyuxiang
    date: 2021-2-26

    结构熵算法测试程序，输入图数据，调用二维结构熵和三维结构熵极小化算法，
    最终得到极小熵结果和编码树（即划分结果）。
"""
from StructuralEntropy.graph.get_real_network import GetRealNetwork
from StructuralEntropy.algorithm.high_dimensional_structural_entropy_algorithm import HighDimensionalStructureEntropyAlgorithm
from StructuralEntropy.plot.plot_result_partition import plot_graph
'''
    程序入口
'''
def main():
    graph = GetRealNetwork('../data/Lymph6Graph').get_graph()
    algorithm = HighDimensionalStructureEntropyAlgorithm(graph)
    # algorithm.print_cut_set()
    tree_2 = algorithm.two_dimension("../data/LymphTwod.txt")
    tree_3 = algorithm.three_dimension("../data/LymphThreed.txt")
    # algorithm.print_tree(tree_2.get_root())
    # algorithm.print_tree(tree_3.get_root())
    # plot_graph(graph, '../data/LymphTwod.txt')

if __name__ == '__main__':
    main()