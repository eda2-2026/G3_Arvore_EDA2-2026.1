from typing import List, Optional
from src.task import Task

#Observação: mantivemos os comentários para fins de documentação e facilitar a nossa compreensão

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

    def _rotate_right(self, y: Node) -> Node:
        """
        Executa uma rotação simples à direita no nó y.
        Retorna a nova raiz da subárvore (x).
        """
        x = y.left
        T2 = x.right

        # Realiza a rotação
        x.right = y
        y.left = T2

        # Atualiza as alturas
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def _rotate_left(self, x: Node) -> Node:
        """
        Executa uma rotação simples à esquerda no nó x.
        Retorna a nova raiz da subárvore (y).
        """
        y = x.right
        T2 = y.left

        # Realiza a rotação
        y.left = x
        x.right = T2

        # Atualiza as alturas
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, task: Task) -> None:
        """
        Insere uma nova tarefa na árvore AVL.
        A inserção é feita com base na prioridade da tarefa.
        """
        self.root = self._insert(self.root, task)

    def _insert(self, node: Optional[Node], task: Task) -> Node:
        """
        Insere recursivamente e rebalanceia a árvore AVL.
        """
        if not node:
            return Node(task.priority, task)

        # Inserção clássica da árvore binária de busca
        if task.priority < node.key:
            node.left = self._insert(node.left, task)
        elif task.priority > node.key:
            node.right = self._insert(node.right, task)
        else:
            # Prioridade já existe: adiciona a tarefa à lista do nó correspondente
            node.tasks.append(task)
            return node

        # Atualiza a altura do nó pai atual
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Obtém o fator de balanceamento
        balance = self.get_balance(node)

        # os 4 casos para tratamento de balanceamento:

        # Caso 1 - Left-Left (Esquerda-Esquerda)
        if balance > 1 and task.priority < node.left.key:
            return self._rotate_right(node)

        # Caso 2 - Right-Right (Direita-Direita)
        if balance < -1 and task.priority > node.right.key:
            return self._rotate_left(node)

        # Caso 3 - Left-Right (Esquerda-Direita)
        if balance > 1 and task.priority > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Caso 4 - Right-Left (Direita-Esquerda)
        if balance < -1 and task.priority < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

