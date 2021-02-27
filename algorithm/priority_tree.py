"""
    author: wangyuxiang
    date: 2021-2-27

    编码树类，包含：
        - 根节点
        - 每个节点的度（是一个list，一个节点的度是由其划分中所有图结点度求和得到）
        - 总度数
"""
import math

'''
    计算Tree中某个节点的结构熵
        - gi，割边数
        - degree_sum，度数总和、对应公式中的2*m（即所有边数乘2，用于无向图）
        - vi，本节点体积
        - vifa，父节点体积
'''
def compute_structural_entropy_of_node(gi, degree_sum, vi, vifa):
    w1 = gi / degree_sum
    w2 = vi / vifa
    w3 = w1 * (math.log2(w2))
    return -w3


class PriorityTree(object):

    def __init__(self, root, degree_of_each_node, degree_sum):
        self.root = root
        self.degree_of_each_node = degree_of_each_node
        self.degree_sum = degree_sum

    '''
        融合算子
    '''

    def merge(self):
        pass

    '''
        联合算子
    '''

    def combine(self):
        pass

    def get_root(self):
        return self.root

    def set_root(self, root):
        self.root = root
