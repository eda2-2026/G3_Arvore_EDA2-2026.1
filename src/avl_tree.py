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

    def _get_min_value_node(self, node: Node) -> Node:
        """
        Retorna o nó com o menor valor de chave (mais à esquerda) a partir de um dado nó.
        """
        current = node
        while current.left:
            current = current.left
        return current

    def _rebalance(self, node: Node) -> Node:
        """
        Calcula as alturas e rebalanceia a subárvore a partir do nó fornecido.
        Retorna a nova raiz da subárvore após o rebalanceamento.
        """
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Caso 1 - Left-Left (Esquerda-Esquerda)
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Caso 2 - Left-Right (Esquerda-Direita)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Caso 3 - Right-Right (Direita-Direita)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Caso 4 - Right-Left (Direita-Esquerda)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _delete_key(self, node: Optional[Node], key: int) -> Optional[Node]:
        """
        Deleta fisicamente o nó correspondente à chave informada e rebalanceia a subárvore.
        Método auxiliar usado principalmente no caso de deleção com dois filhos.
        """
        if not node:
            return None

        if key < node.key:
            node.left = self._delete_key(node.left, key)
        elif key > node.key:
            node.right = self._delete_key(node.right, key)
        else:
            # Encontrou o nó a ser deletado fisicamente
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Caso de dois filhos: sucessor em-ordem
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.tasks = temp.tasks
            node.right = self._delete_key(node.right, temp.key)

        return self._rebalance(node)

    def delete(self, priority: int, task_id: str) -> None:
        """
        Remove uma tarefa com base na sua prioridade e ID único.
        Se a lista de tarefas da prioridade informada esvaziar, o nó correspondente é deletado fisicamente.
        """
        self.root = self._delete(self.root, priority, task_id)

    def _delete(self, node: Optional[Node], priority: int, task_id: str) -> Optional[Node]:
        """
        Método recursivo interno para buscar a prioridade e remover a tarefa com o ID fornecido.
        """
        if not node:
            return None

        if priority < node.key:
            node.left = self._delete(node.left, priority, task_id)
        elif priority > node.key:
            node.right = self._delete(node.right, priority, task_id)
        else:
            # Encontramos o nó da prioridade correspondente. 
            # Procuramos a tarefa específica pelo ID.
            task_to_remove = None
            for t in node.tasks:
                if t.id == task_id:
                    task_to_remove = t
                    break

            if task_to_remove:
                node.tasks.remove(task_to_remove)

            # Se ainda existem tarefas restantes com essa prioridade, mantemos o nó
            if len(node.tasks) > 0:
                return node

            # Se a lista esvaziou, removemos este nó fisicamente
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Caso de dois filhos: sucessor em-ordem
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.tasks = temp.tasks
            node.right = self._delete_key(node.right, temp.key)

        return self._rebalance(node)

    def get_all_ordered(self, order: str = "desc") -> List[Task]:
        """
        Retorna todas as tarefas da árvore ordenadas por prioridade.
        :parametro order: "desc" para prioridade mais alta primeiro (decrescente), 
                           "asc" para prioridade mais baixa primeiro (crescente).
        """
        tasks_list: List[Task] = []
        self._inorder(self.root, tasks_list, order)
        return tasks_list

    def _inorder(self, node: Optional[Node], tasks_list: List[Task], order: str) -> None:
        """
        Realiza o percurso em-ordem (crescente ou decrescente) recursivamente.
        """
        if not node:
            return

        if order == "desc":
            # Direita -> Raiz -> Esquerda
            self._inorder(node.right, tasks_list, order)
            tasks_list.extend(node.tasks)
            self._inorder(node.left, tasks_list, order)
        else:
            # Esquerda -> Raiz -> Direita
            self._inorder(node.left, tasks_list, order)
            tasks_list.extend(node.tasks)
            self._inorder(node.right, tasks_list, order)



