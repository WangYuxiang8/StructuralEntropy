from StructuralEntropy.algorithm.high_dimensional_structural_entropy_algorithm import HighDimensionalStructureEntropyAlgorithm
class TestDemo(object):

    def __init__(self, my_dict):
        self.my_dict = my_dict

    def get_dict(self):
        return self.my_dict

    def set_dict(self, my_dict):
        self.my_dict = my_dict


def test_1():
    t = TestDemo({1:'a', 2:'b'})
    print("t is: ", str(t.get_dict()))
    d = t.get_dict()
    d.pop(1)
    print("t is: ", str(t.get_dict()))


def test_hash():
    a = "abc"
    b = "abc"
    if hash(a) == hash(b):
        print("a hash: ", hash(a))
        print("b hash: ", hash(b))


def test_two_community_hash():
    d = dict()
    t1 = HighDimensionalStructureEntropyAlgorithm.TwoCommunity({"1", "2"}, {"3", "4"})
    t2 = HighDimensionalStructureEntropyAlgorithm.TwoCommunity({"1", "2"}, {"3", "4"})
    d.setdefault(t1, 1.2)
    if d.get(t2):
        print(d.get(t2))


if __name__ == '__main__':
    test_two_community_hash()