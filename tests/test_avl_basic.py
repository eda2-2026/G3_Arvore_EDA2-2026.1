from src.task import Task
from src.avl_tree import Node, AVLTree

def test_task_creation():
    task = Task(description="Estudar EDA2", priority=10)
    assert task.description == "Estudar EDA2"
    assert task.priority == 10
    assert task.id is not None
    assert len(task.id) == 8
    assert task.created_at is not None

def test_node_creation():
    task = Task(description="Estudar EDA2", priority=10)
    node = Node(priority=10, task=task)
    assert node.key == 10
    assert len(node.tasks) == 1
    assert node.tasks[0] == task
    assert node.left is None
    assert node.right is None
    assert node.height == 1

def test_avl_tree_initialization():
    tree = AVLTree()
    assert tree.root is None
    assert tree.get_height(None) == 0
    assert tree.get_balance(None) == 0
