# StructuralEntropy
Structural Entropy algorithm in Python


## process
_2021-3-1_
1. 完成二维结构熵算法，但是划分结果与预期不一致。

_2021-3-2_
1. get_real_network可以正确构建graph模型。
2. cut_set可以正确构建只包含两个节点的所有社区。
3. root成功创建，第一层节点（每个节点对应图结点）成功创建。

* 找到错误所在：
在于TwoCommunity类和TwoID类的__hash__和__eq__逻辑错误，
对于一个TwoCommunity对象或TwoID对象，它们存储了两个社区，
判断它们相等的逻辑应该考虑到不同顺序的社区有可能表示的是同一个集合。
例如t1 = {comi, comj}，t2 = {comj, comi}，t1和t2的hash值应当是
相等的，并且判断t1和t2也应该是相等的。

_2021-3-5_
1. 完成三维结构熵极小化算法
