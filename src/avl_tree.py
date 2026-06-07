from typing import List, Optional
from src.task import Task

class Node:
    def __init__(self, priority: int, task: Task):
        """
        Representa um nó na árvore AVL. A chave de busca é a prioridade.
        Cada nó armazena uma lista de tarefas com a mesma prioridade.
        """
        self.key: int = priority
        self.tasks: List[Task] = [task]  # Permite tarefas duplicadas com a mesma prioridade
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.height: int = 1

    def __repr__(self):
        return f"Node(key={self.key}, height={self.height}, tasks_count={len(self.tasks)})"


class AVLTree:
    def __init__(self):
        self.root: Optional[Node] = None

    def get_height(self, node: Optional[Node]) -> int:
        """Retorna a altura de um nó (0 se for None)."""
        if not node:
            return 0
        return node.height

    def get_balance(self, node: Optional[Node]) -> int:
        """Retorna o fator de balanceamento de um nó."""
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
