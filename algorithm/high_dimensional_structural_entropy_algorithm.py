"""
    author: wangyuxiang
    date: 2021-2-27

    结构熵极小化算法，包含：
        - 一维结构熵极小化算法
        - 二维结构熵极小化算法
        - 三维结构熵极小化算法
"""
from StructuralEntropy.algorithm.priority_tree import compute_structural_entropy_of_node, PriorityTree
from StructuralEntropy.algorithm.tree_node import TreeNode
from StructuralEntropy.algorithm.two_id import TwoID


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
                    gij = edge_dict_of_nodei[str(j)]       # 两个社区之间的割边数（这里就是两个节点之间所连边的权重）
                    self.cut_set.setdefault(two_community, gij)

    '''
        一维结构熵极小化算法：
            - 最大高度为1的编码树，也就是只有一层叶子节点，此时相当于整个图没有做划分
            - 一维结构熵等价于度分布的香农熵
    '''
    def one_dimension(self):
        SE = 0.0
        for i in range(1, self.vertice_number + 1):
            SE += compute_structural_entropy_of_node(self.vertice_degree_list[i],
                                                     self.degree_sum,
                                                     self.vertice_degree_list[i],
                                                     self.degree_sum)
        return SE

    '''
        二维结构熵极小化算法
    '''
    def two_dimension(self, output_filename):
        level = 0
        id = 0
        vi = self.degree_sum                    # 本节点体积
        vifa = 0                                # 父节点体积
        gi = 0.0                                # 割边数
        se = 0.0                                # 根节点的结构熵，为0
        children = list()                       # 当前节点的孩子节点list，[TreeNode, TreeNode, ...]
        entropy_of_childtree = list()           # 当前节点的子树的结构熵
        highest_level_of_childtree = list()     # 子树的最大高度
        iter_num = -1
        merge_detaH_of_children = dict()        # {TwoID: Float}
        combine_detaH_of_children = dict()      # {TwoID: Float}
        '''
            这里是创建编码树的根节点
                - 其中根节点的父节点为None
                - 根节点的子节点也都不是叶子节点，因为这是2维结构熵，所以叶子节点在第二层，所以三个保存叶子节点的参数也为None
        '''
        root = TreeNode(level, id, None, vi, vifa, gi, se, children, entropy_of_childtree, highest_level_of_childtree,
                        None, None, None, iter_num, merge_detaH_of_children, combine_detaH_of_children)
        big_tree = PriorityTree(root, self.vertice_degree_list, self.degree_sum)

        '''
            先为每一个图结点创建一个TreeNode，然后将其加入到根节点的子节点下作为叶子节点，后面再进行merge和combine
            对于每个TreeNode都需要初始化或计算所有参数值，并传入类
        '''
        for i in range(self.vertice_number):
            vertice_id = i + 1
            node_id = i
            tree_level = root.get_level() + 1

            # 计算当前节点的结构熵
            own_volumn = self.vertice_degree_list[vertice_id]
            father_volumn = root.get_own_volumn()
            cut = self.vertice_degree_list[vertice_id]
            structural_entropy_of_node = compute_structural_entropy_of_node(cut, self.degree_sum, own_volumn, father_volumn)

            children_of_leaf = list()
            entropy_of_leaf_children = list()
            highest_level_of_leaf_children = list()
            community_of_leaves1 = list()
            community_of_leaves2 = list()
            all_leaves = list()
            community_of_leaves1.append(str(vertice_id))
            all_leaves.append(str(vertice_id))

            iter_num = 0
            merge_detaH_of_children = dict()    # {TwoID: Float}
            combine_detaH_of_children = dict()  # {TwoID: Float}

            leaf = TreeNode(node_id, tree_level, root, own_volumn, father_volumn, cut, structural_entropy_of_node,
                            children_of_leaf, entropy_of_leaf_children, highest_level_of_leaf_children, community_of_leaves1,
                            community_of_leaves2, all_leaves, iter_num, merge_detaH_of_children, combine_detaH_of_children)
            children.append(leaf)
            entropy_of_childtree.append(structural_entropy_of_node)
            highest_level_of_childtree.append(tree_level)
        # 更新root节点的信息
        root.set_children(children)
        root.set_entropy_of_childtree(entropy_of_childtree)
        root.set_highest_level_of_childtree(highest_level_of_childtree)

        iter_num = 1
        while True:
            # 用来记录最大的结构熵变化量以及对应的划分节点
            max1 = None     # TreeNode
            max2 = None     # TreeNode
            g12 = 0.0
            maxdetaH = 0.0

            # root节点的子节点，目前为所有的图结点对应构建的TreeNode
            children_of_root = root.get_children()
            merge_detaH_of_root_children = root.get_merge_detaH_of_children()
            for i in range(self.vertice_number - 1):
                for j in range(i + 1, self.vertice_number):
                    if children_of_root[i] and children_of_root[j]:         # ???
                        rooti = children_of_root[i]
                        rootj = children_of_root[j]
                        cutij = self.get_cut(rooti.get_all_leaves(), rootj.get_all_leaves())
                        if cutij != 0:
                            two_id = TwoID(rooti.get_id(), rootj.get_id())
                            if merge_detaH_of_root_children.get(two_id):
                                detaH = merge_detaH_of_root_children.get(two_id)
                            else:
                                detaH = self.merge_same_level(rooti, rootj, root, cutij)
                                merge_detaH_of_root_children.setdefault(two_id, detaH)
                            if detaH > maxdetaH:
                                max1 = rooti
                                max2 = rootj
                                maxdetaH = detaH
                                g12 = cutij
            if maxdetaH > 0:
                new_node = big_tree.merge(max1, max2, g12, iter_num)
            else:
                break
            iter_num += 1

            # 更新merge后的节点（新的社区）与同层的其他节点（社区）之间的割边数
            update_cut_of_newnode_and_othernode = new_node.get_father().get_children()
            for node in update_cut_of_newnode_and_othernode:
                if node and node.get_id() != new_node.get_id():
                    cut = self.get_cut(node.get_all_leaves(), new_node.get_community_of_leaves1()) + \
                          self.get_cut(node.get_all_leaves(), new_node.get_community_of_leaves2())
                    if cut != 0.0:
                        self.set_cut(node.get_all_leaves(), new_node.get_all_leaves(), cut)
        # 输出划分结果，并对树做一个修正
        f = open(output_filename, 'w')
        self.output_twod_result(big_tree.get_root(), f)
        f.close()
        self.adjust_tree(big_tree)
        return big_tree

    def three_dimension(self):
        pass

    '''
        获取两个community的割边数，从self.cut_set中获得
        comi: [string, string, ...]
    '''
    def get_cut(self, comi, comj):
        comi = set(comi)
        comj = set(comj)
        two_community = self.TwoCommunity(comi, comj)
        if self.cut_set.get(two_community):
            return self.cut_set[two_community]
        return 0.0

    '''
        更新（新建）两个community的割边数
        comi: [string, string, ...]
    '''
    def set_cut(self, comi, comj, gij):
        comi = set(comi)
        comj = set(comj)
        two_community = self.TwoCommunity(comi, comj)
        if not self.cut_set.get(two_community):
            self.cut_set.setdefault(two_community, gij)

    '''
        计算merge同层的两个节点的结构熵的变化量
    '''
    def merge_same_level(self, nodei, nodej, father, cutij):
        entropy_before = father.get_entropy_of_childtree()[nodei.get_id()] + \
                         father.get_entropy_of_childtree()[nodej.get_id()]

        entropy_after = 0.0

        # 计算当前两个节点合并后的节点的结构熵
        v_new = nodei.get_own_volumn() + nodej.get_own_volumn()
        cut_new = nodei.get_cut() + nodej.get_cut() - 2 * cutij
        v_fa = nodei.get_father_volumn()
        entropy_after += compute_structural_entropy_of_node(cut_new, self.degree_sum, v_new, v_fa)

        # 分别计算两个节点的子节点的熵（因为他们所在社区的体积变化了）
        # 这里的leaf_id是节点i的叶子节点，其编号与对应图结点的编号一致
        leaves_of_nodei = nodei.get_all_leaves()
        for i in range(len(leaves_of_nodei)):
            leaf_id = int(leaves_of_nodei[i])
            entropy_after += compute_structural_entropy_of_node((self.vertice_degree_list[leaf_id]),
                                                                self.degree_sum,
                                                                self.vertice_degree_list[leaf_id],
                                                                v_new)
        leaves_of_nodej = nodej.get_all_leaves()
        for i in range(len(leaves_of_nodej)):
            leaf_id = int(leaves_of_nodej[i])
            entropy_after += compute_structural_entropy_of_node((self.vertice_degree_list[leaf_id]),
                                                                self.degree_sum,
                                                                self.vertice_degree_list[leaf_id],
                                                                v_new)
        return entropy_before - entropy_after

    # 递归输出
    def output_twod_result(self, node, file):
        if node.get_iterate_number() == 0:
            return node.get_all_leaves()[0] + ','
        else:
            s = ""
            for n in node.get_children():
                if n:
                    s += self.output_twod_result(n, file)
                    if n.get_level() == 1:
                        print(s)
                        file.write(s + "\n")
                        s = ""
            return s

    # 修正树的空节点和节点id
    def adjust_tree(self, tree):
        root = tree.get_root()
        self.delete_none(root)
        self.correct_id(root)

    def delete_none(self, root):
        if root.get_iterate_number() != 0:
            children = root.get_children()
            # 从一个list当中删除指定元素（这里是None）
            j = 0
            for i in range(len(children)):
                if not children[j]:
                    children.pop(j)
                else:
                    j += 1
            for i in children:
                self.delete_none(i)

    def correct_id(self, root):
        if root.get_iterate_number() != 0:
            children = root.get_children()
            for i in range(len(children)):
                children[i].set_id(i)
            for i in children:
                self.correct_id(i)

    '''
        构建存储两个社区的信息的类，用于割边的计算
    '''
    class TwoCommunity(object):

        def __init__(self, comi, comj):
            self.comi = comi        # set(string, string, ... , string)
            self.comj = comj

        def __str__(self):
            return "TwoCommunity [comi=" + str(self.comi) + ", comj=" + str(self.comj) + "]"

        # 重写hash值，判断两个对象是否相等
        def __hash__(self):
            t = tuple()
            for i in self.comi:
                t += (i,)
            for j in self.comj:
                t += (j,)
            return hash(t)

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                other_comi = other.__dict__.get("comi")
                other_comj = other.__dict__.get("comj")
                my_comi = self.__dict__.get("comi")
                my_comj = self.__dict__.get("comj")
                if len(other_comi) != len(my_comi) or len(other_comj) != len(my_comj):
                    return False
                else:
                    return other_comi == my_comi and other_comj == my_comj
            else:
                return False

    # 测试程序
    def print_cut_set(self):
        print("----------Test cut set-----------")
        print("Size of cut set: %d" % len(self.cut_set))
        for k, v in self.cut_set.items():
            print("Community = %s, weight = %f" % (k, v))

    # 打印出整个编码树
    def print_tree(self, root):
        print(root)
        print('  - ', root.get_merge_detaH_of_children())
        print('  - ', root.get_combine_detaH_of_children())
        for i in root.get_children():
            self.print_tree(i)
