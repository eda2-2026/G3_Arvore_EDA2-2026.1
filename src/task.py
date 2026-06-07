import time
import uuid

class Task:
    def __init__(self, description: str, priority: int, task_id: str = None):
        """
        Representa uma tarefa individual no sistema.
        - description: Breve descrição da tarefa.
        - priority: Valor inteiro de 1 a 100 indicando a urgência da tarefa.
        - task_id: Identificador único opcional (caso não fornecido, gera um UUID).
        """
        self.id = task_id if task_id else uuid.uuid4().hex[:8] # id até 8 caract
        self.description = description
        self.priority = priority
        self.created_at = time.time() # tempo para ordenação secundária, se necessárria

    def __repr__(self):
        return f"Task(id='{self.id}', description='{self.description}', priority={self.priority})"
