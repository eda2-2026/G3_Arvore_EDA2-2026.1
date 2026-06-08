import time
import uuid

class Task:
    def __init__(self, description: str, priority: int, task_id: str = None, created_at: float = None, completed: bool = False):
        """
        Representa uma tarefa individual no sistema.
        - description: Breve descrição da tarefa.
        - priority: Valor inteiro de 1 a 100 indicando a urgência da tarefa.
        - task_id: Identificador único opcional (caso não fornecido, gera um UUID).
        - completed: Status de conclusão da tarefa.
        """
        self.id = task_id if task_id else uuid.uuid4().hex[:8] # id até 8 caract
        self.description = description
        self.priority = priority
        self.created_at = created_at if created_at else time.time() # tempo para ordenação secundária, se necessárria
        self.completed = completed

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority,
            "created_at": self.created_at,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        return cls(
            description=data["description"],
            priority=data["priority"],
            task_id=data["id"],
            created_at=data["created_at"],
            completed=data.get("completed", False)
        )

    def __repr__(self):
        return f"Task(id='{self.id}', description='{self.description}', priority={self.priority}, completed={self.completed})"
