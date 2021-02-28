"""
    author: wangyuxiang
    date: 2021-2-26

    结构熵算法测试程序，输入图数据，调用二维结构熵和三维结构熵极小化算法，
    最终得到极小熵结果和编码树（即划分结果）。
"""
from StructuralEntropy.graph.get_real_network import GetRealNetwork
from StructuralEntropy.algorithm.high_dimensional_structural_entropy_algorithm import HighDimensionalStructureEntropyAlgorithm

'''
    程序入口
'''
def main():
    graph = GetRealNetwork('../data/Lymph6Graph').get_graph()
    algorithm = HighDimensionalStructureEntropyAlgorithm(graph)
    tree = algorithm.two_dimension("../data/LymphTwod.txt")
    algorithm.print_tree(tree.get_root())


if __name__ == '__main__':
    main()