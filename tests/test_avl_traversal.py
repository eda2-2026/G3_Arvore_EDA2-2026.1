from src.task import Task
from src.avl_tree import AVLTree

def test_traversal_empty_tree():
    tree = AVLTree()
    assert tree.get_all_ordered() == []


def test_traversal_descending():
    # Padrão: prioridade mais alta primeiro
    tree = AVLTree()
    t1 = Task("T20", 20)
    t2 = Task("T10", 10)
    t3 = Task("T30", 30)

    tree.insert(t1)
    tree.insert(t2)
    tree.insert(t3)

    ordered = tree.get_all_ordered(order="desc")
    assert len(ordered) == 3
    assert ordered[0] == t3
    assert ordered[1] == t1
    assert ordered[2] == t2


def test_traversal_ascending():
    # Prioridade mais baixa primeiro
    tree = AVLTree()
    t1 = Task("T20", 20)
    t2 = Task("T10", 10)
    t3 = Task("T30", 30)

    tree.insert(t1)
    tree.insert(t2)
    tree.insert(t3)

    ordered = tree.get_all_ordered(order="asc")
    assert len(ordered) == 3
    assert ordered[0] == t2
    assert ordered[1] == t1
    assert ordered[2] == t3


def test_traversal_duplicate_stability():
    # Tarefas com mesma prioridade devem manter a ordem temporal de inserção
    tree = AVLTree()
    t1 = Task("Tarefa A (Primeira)", 15)
    t2 = Task("Tarefa B (Segunda)", 15)
    t3 = Task("Tarefa C (Urgente)", 50)

    tree.insert(t1)
    tree.insert(t2)
    tree.insert(t3)

    # Decrescente
    ordered_desc = tree.get_all_ordered(order="desc")
    assert ordered_desc == [t3, t1, t2]

    # Crescente
    ordered_asc = tree.get_all_ordered(order="asc")
    assert ordered_asc == [t1, t2, t3]
