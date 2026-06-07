from src.task import Task
from src.avl_tree import AVLTree

def test_simple_insertion():
    tree = AVLTree()
    task = Task("Estudar EDA2", 50)
    tree.insert(task)

    assert tree.root is not None
    assert tree.root.key == 50
    assert len(tree.root.tasks) == 1
    assert tree.root.tasks[0] == task
    assert tree.root.height == 1


def test_duplicate_priorities():
    tree = AVLTree()
    t1 = Task("Comprar arroz", 10)
    t2 = Task("Estudar APC", 10)

    tree.insert(t1)
    tree.insert(t2)

    # Não deve criar um novo nó, mas sim colocar na lista 'tasks' do nó com chave 10
    assert tree.root is not None
    assert tree.root.key == 10
    assert len(tree.root.tasks) == 2
    assert tree.root.tasks[0] == t1
    assert tree.root.tasks[1] == t2
    assert tree.root.left is None
    assert tree.root.right is None


def test_balance_left_left():
    # Inserção LL: 30 -> 20 -> 10. Deve resultar em 20 na raiz.
    tree = AVLTree()
    tree.insert(Task("T30", 30))
    tree.insert(Task("T20", 20))
    tree.insert(Task("T10", 10))

    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 30
    assert tree.root.height == 2
    assert tree.root.left.height == 1
    assert tree.root.right.height == 1


def test_balance_right_right():
    # Inserção RR: 10 -> 20 -> 30. Deve resultar em 20 na raiz.
    tree = AVLTree()
    tree.insert(Task("T10", 10))
    tree.insert(Task("T20", 20))
    tree.insert(Task("T30", 30))

    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 30
    assert tree.root.height == 2
    assert tree.root.left.height == 1
    assert tree.root.right.height == 1


def test_balance_left_right():
    # Inserção LR: 30 -> 10 -> 20. Deve resultar em 20 na raiz.
    tree = AVLTree()
    tree.insert(Task("T30", 30))
    tree.insert(Task("T10", 10))
    tree.insert(Task("T20", 20))

    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 30
    assert tree.root.height == 2
    assert tree.root.left.height == 1
    assert tree.root.right.height == 1


def test_balance_right_left():
    # Inserção RL: 10 -> 30 -> 20. Deve resultar em 20 na raiz.
    tree = AVLTree()
    tree.insert(Task("T10", 10))
    tree.insert(Task("T30", 30))
    tree.insert(Task("T20", 20))

    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 30
    assert tree.root.height == 2
    assert tree.root.left.height == 1
    assert tree.root.right.height == 1
