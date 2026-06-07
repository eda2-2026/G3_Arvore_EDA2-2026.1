from src.task import Task
from src.avl_tree import AVLTree

def test_delete_logical_duplicate():
    tree = AVLTree()
    t1 = Task("Tarefa APC", 20)
    t2 = Task("Tarefa BANCOS", 20)
    tree.insert(t1)
    tree.insert(t2)

    # Verifica se foram agrupadas
    assert len(tree.root.tasks) == 2

    # Remove apenas t1
    tree.delete(20, t1.id)

    # O nó 20 ainda deve existir, mas apenas com a Tarefa B
    assert tree.root is not None
    assert tree.root.key == 20
    assert len(tree.root.tasks) == 1
    assert tree.root.tasks[0] == t2


def test_delete_physical_zero_children():
    tree = AVLTree()
    t1 = Task("tarefa 50", 50)
    tree.insert(t1)

    assert tree.root.key == 50

    # Deleta a única tarefa
    tree.delete(50, t1.id)

    # A árvore deve ficar vazia
    assert tree.root is None


def test_delete_physical_one_child():
    tree = AVLTree()
    t1 = Task("Raiz", 50)
    t2 = Task("Filho Esquerdo", 30)
    tree.insert(t1)
    tree.insert(t2)

    # Deleta a raiz
    tree.delete(50, t1.id)

    # O filho esquerdo deve assumir a raiz
    assert tree.root is not None
    assert tree.root.key == 30
    assert tree.root.height == 1
    assert tree.root.left is None
    assert tree.root.right is None


def test_delete_physical_two_children():
    tree = AVLTree()
    t1 = Task("Raiz", 50)
    t2 = Task("Esquerda", 30)
    t3 = Task("Direita", 70)
    tree.insert(t1)
    tree.insert(t2)
    tree.insert(t3)

    # Deleta o nó raiz (50) que possui dois filhos
    tree.delete(50, t1.id)

    # O sucessor em-ordem (70) deve subir para a raiz
    assert tree.root is not None
    assert tree.root.key == 70
    assert tree.root.left.key == 30
    assert tree.root.right is None
    assert tree.root.height == 2


def test_delete_with_rebalance():
    # Monta árvore balanceada:

    tree = AVLTree()
    t_30 = Task("T30", 30)
    t_20 = Task("T20", 20)
    t_40 = Task("T40", 40)
    t_10 = Task("T10", 10)

    tree.insert(t_30)
    tree.insert(t_20)
    tree.insert(t_40)
    tree.insert(t_10)

    # Altura inicial deve ser 3
    assert tree.root.height == 3

    # Deleta a tarefa 40 (folha direita). A árvore fica pesada para a esquerda e deve rodar.
    tree.delete(40, t_40.id)

    # Nova estrutura após rotação LL (à direita em 30):

    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 30
    assert tree.root.height == 2
    assert tree.root.left.height == 1
    assert tree.root.right.height == 1
