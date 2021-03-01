"""
    author: wangyuxiang
    date: 2021-2-27

    编码树类，包含：
        - 根节点
        - 每个节点的度（是一个list，一个节点的度是由其划分中所有图结点度求和得到）
        - 总度数
"""
import math
from StructuralEntropy.algorithm.tree_node import TreeNode
from StructuralEntropy.algorithm.two_id import TwoID

'''
    计算Tree中某个节点的结构熵
        - gi，割边数
        - degree_sum，度数总和、对应公式中的2*m（即所有边数乘2，用于无向图）
        - vi，本节点体积
        - vifa，父节点体积
        
    结构熵计算公式：
        H^T(G) = - sigma( (gi/2m) * log2(Vi/Vifa) )
'''
def compute_structural_entropy_of_node(gi, degree_sum, vi, vifa):
    w1 = gi / degree_sum
    w2 = vi / vifa
    w3 = w1 * (math.log2(w2))
    return -w3


class PriorityTree(object):

    def __init__(self, root, vertice_degree_list, degree_sum):
        self.root = root
        self.vertice_degree_list = vertice_degree_list
        self.degree_sum = degree_sum

    '''
        融合算子
            - child_one，第一个节点（表示需要merge的第一个社区）- TreeNode
            - child_two，第二个节点（表示需要merge的第二个社区）- TreeNode
            - cutij，表示两个社区之间的割边数
            - iter_num当前迭代次数
    '''
    def merge(self, child_one, child_two, cutij, iter_num):
        id1 = child_one.get_id()
        id2 = child_two.get_id()

        '''
            这里用两个新的list（new_com1和new_com2）来存储merge后新的社区的结点
            用all_leaves来存储merge后的所有节点
        '''
        all_leaves = list()
        new_com1 = list()
        new_com2 = list()
        old_child_one_com1 = child_one.get_community_of_leaves1()
        old_child_one_com2 = child_one.get_community_of_leaves2()
        old_child_two_com1 = child_two.get_community_of_leaves1()
        old_child_two_com2 = child_two.get_community_of_leaves2()
        for i in old_child_one_com1:
            new_com1.append(i)
            all_leaves.append(i)
        for i in old_child_one_com2:
            new_com1.append(i)
            all_leaves.append(i)
        for i in old_child_two_com1:
            new_com2.append(i)
            all_leaves.append(i)
        for i in old_child_two_com2:
            new_com2.append(i)
            all_leaves.append(i)

        # 更新父节点对于child_two的所有信息，清除child_two的所有信息
        child_one.get_father().get_children()[id2] = None
        child_one.get_father().get_entropy_of_childtree()[id2] = 0.0
        child_one.get_father().get_highest_level_of_childtree()[id2] = 0
        child_two.set_father(None)
        child_two.set_all_leaves(None)
        child_two.set_community_of_leaves1(None)
        child_two.set_community_of_leaves2(None)

        # 更新child_one，将其作为merge之后的父节点
        child_one.set_own_volumn(child_one.get_own_volumn() + child_two.get_own_volumn())
        child_one.set_cut(child_one.get_cut() + child_two.get_cut() - 2 * cutij)
        se = compute_structural_entropy_of_node(child_one.get_cut(), self.degree_sum, child_one.get_own_volumn(),
                                                child_one.get_father_volumn())
        child_one.set_structural_entropy_of_node(se)
        child_one.set_community_of_leaves1(new_com1)
        child_one.set_community_of_leaves2(new_com2)
        child_one.set_all_leaves(all_leaves)
        child_one.set_iterate_number(iter_num)

        '''
            更新child_one的子节点，此时child_one是merge后新的社区，因此子节点的结构熵等信息需要进行修改和更新
            这里采用的方法是不管之前创建的节点，所有再重新构建一遍 -> 需要优化
        '''
        children = list()
        entropy_of_childtree = list()
        highest_level_of_childtree = list()
        merge_detaH_of_children = dict()            # {TwoID: float}
        combine_detaH_of_children = dict()
        for i in range(len(all_leaves)):
            vertice_id = int(all_leaves[i])
            node_id = i
            tree_level = child_one.get_level() + 1

            # 计算当前节点的结构熵
            own_volumn = self.vertice_degree_list[vertice_id]
            father_volumn = child_one.get_own_volumn()
            cut = self.vertice_degree_list[vertice_id]
            structural_entropy_of_node = compute_structural_entropy_of_node(cut, self.degree_sum, own_volumn,
                                                                            father_volumn)
            children_of_leaf = list()
            entropy_of_leaf_children = list()
            highest_level_of_leaf_children = list()
            community_of_leaves1 = list()
            community_of_leaves2 = list()
            all_leaves_of_node = list()
            community_of_leaves1.append(str(vertice_id))
            all_leaves_of_node.append(str(vertice_id))

            iter_num = 0
            merge_detaH_of_children = dict()    # {TwoID: Float}
            combine_detaH_of_children = dict()  # {TwoID: Float}

            leaf = TreeNode(node_id, tree_level, child_one, own_volumn, father_volumn, cut, structural_entropy_of_node,
                            children_of_leaf, entropy_of_leaf_children, highest_level_of_leaf_children, community_of_leaves1,
                            community_of_leaves2, all_leaves_of_node, iter_num, merge_detaH_of_children, combine_detaH_of_children)
            children.append(leaf)
            entropy_of_childtree.append(structural_entropy_of_node)
            highest_level_of_childtree.append(tree_level)
        # 更新root节点的信息
        child_one.set_children(children)
        child_one.set_entropy_of_childtree(entropy_of_childtree)
        child_one.set_highest_level_of_childtree(highest_level_of_childtree)
        child_one.set_merge_detaH_of_children(merge_detaH_of_children)
        child_one.set_combine_detaH_of_children(combine_detaH_of_children)

        '''
            更新祖先节点的子树结构熵数组和子树最高层级数组
        '''
        curr = child_one
        father = curr.get_father()
        while True:
            curr_id = curr.get_id()
            curr_tree_entropy = 0.0
            curr_tree_highest_level = 0
            for i in range(len(curr.get_entropy_of_childtree())):
                curr_tree_entropy += curr.get_entropy_of_childtree()[i]
                if curr.get_highest_level_of_childtree()[i] > curr_tree_highest_level:
                    curr_tree_highest_level = curr.get_highest_level_of_childtree()[i]
            curr_tree_entropy += curr.get_structural_entropy_of_node()      # 还要加上当前根节点的结构熵
            father.get_entropy_of_childtree()[curr_id] = curr_tree_entropy
            father.get_highest_level_of_childtree()[curr_id] = curr_tree_highest_level

            # 继续往祖先更新
            curr = father
            father = father.get_father()
            if not father:
                break

        # 把childone的父亲节点的detaHofChildren中所有和id1和id2相关的都删掉
        merge_detaH_of_childone_father = child_one.get_father().get_merge_detaH_of_children()
        merge_detaH_of_childone_father.pop(TwoID(id1, id2))         # 删除child_one和child_two这两个社区的TwoID删除
        # 删除与child_one或child_two有联合的TwoID都删了
        for i in range(len(child_one.get_father().get_children())):
            if merge_detaH_of_childone_father.get(TwoID(i, id1)):
                merge_detaH_of_childone_father.pop(TwoID(i, id1))
            if merge_detaH_of_childone_father.get(TwoID(i, id2)):
                merge_detaH_of_childone_father.pop(TwoID(i, id2))

        # 继续往祖宗节点更新，删除相关的detah值
        curr = child_one.get_father()
        father = curr.get_father()
        while father:
            curr_id = curr.get_id()
            merge_detaH_of_childone_father = father.get_merge_detaH_of_children()
            for i in range(len(father.get_children())):
                if merge_detaH_of_childone_father.get(TwoID(i, curr_id)):
                    merge_detaH_of_childone_father.pop(TwoID(i, curr_id))
            curr = father
            father = father.get_father()

        return child_one

    '''
        联合算子
    '''

    def combine(self):
        pass

    def get_root(self):
        return self.root

    def set_root(self, root):
        self.root = root
