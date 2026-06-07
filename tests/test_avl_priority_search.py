from src.task import Task
from src.avl_tree import AVLTree

def test_priority_search_empty_tree():
    tree = AVLTree()
    assert tree.get_highest_priority() is None
    assert tree.get_lowest_priority() is None


def test_priority_search_highest_and_lowest():
    tree = AVLTree()
    t1 = Task("T20", 20)
    t2 = Task("T10", 10)
    t3 = Task("T30", 30)

    tree.insert(t1)
    tree.insert(t2)
    tree.insert(t3)

    assert tree.get_highest_priority() == t3
    assert tree.get_lowest_priority() == t2


def test_priority_search_duplicate_stability():
    tree = AVLTree()
    # Inserções repetidas para testar o retorno da mais antiga
    t1_10 = Task("T10 Primeira", 10)
    t2_10 = Task("T10 Segunda", 10)
    
    t1_50 = Task("T50 Primeira", 50)
    t2_50 = Task("T50 Segunda", 50)

    tree.insert(t1_10)
    tree.insert(t2_10)
    tree.insert(t1_50)
    tree.insert(t2_50)

    assert tree.get_highest_priority() == t1_50

    assert tree.get_lowest_priority() == t1_10
