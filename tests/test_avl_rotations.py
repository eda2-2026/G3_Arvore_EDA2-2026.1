from src.task import Task
from src.avl_tree import Node, AVLTree

def test_rotate_right():
    # Monta uma subárvore desbalanceada para a esquerda (Left-Left):

    y = Node(30, Task("Tarefa Y", 30))
    x = Node(20, Task("Tarefa X", 20))
    z = Node(10, Task("Tarefa Z", 10))

    y.left = x
    x.left = z

    # Define alturas iniciais
    z.height = 1
    x.height = 2
    y.height = 3

    tree = AVLTree()
    
    # Aplica rotação à direita no topo (y)
    new_root = tree._rotate_right(y)

    # Verifica se a nova estrutura está correta:

    assert new_root == x
    assert new_root.left == z
    assert new_root.right == y

    # Verifica se as alturas foram recalculadas corretamente
    assert z.height == 1
    assert y.height == 1
    assert x.height == 2


def test_rotate_left():
    # Monta uma subárvore desbalanceada para a direita (Right-Right):
    x = Node(10, Task("Tarefa X", 10))
    y = Node(20, Task("Tarefa Y", 20))
    z = Node(30, Task("Tarefa Z", 30))

    x.right = y
    y.right = z

    # Define alturas iniciais
    z.height = 1
    y.height = 2
    x.height = 3

    tree = AVLTree()
    
    # Aplica rotação à esquerda no topo (x)
    new_root = tree._rotate_left(x)

    # Verifica se a nova estrutura está correta:

    assert new_root == y
    assert new_root.left == x
    assert new_root.right == z

    # Verifica se as alturas foram recalculadas corretamente
    assert x.height == 1
    assert z.height == 1
    assert y.height == 2
