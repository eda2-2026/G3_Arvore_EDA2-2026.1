import json
import os
from src.task import Task
from src.avl_tree import AVLTree

def save_tasks(tree: AVLTree, filepath: str) -> None:
    """
    Salva todas as tarefas da árvore AVL em um arquivo JSON.
    """
    # Usamos o percurso ordenado ascendente para obter todas as tarefas de forma plana
    tasks = tree.get_all_ordered(order="asc")
    data = [task.to_dict() for task in tasks]
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_tasks(filepath: str) -> AVLTree:
    """
    Carrega as tarefas de um arquivo JSON e as insere em uma nova árvore AVL.
    Se o arquivo não existir, retorna uma árvore AVL vazia.
    """
    tree = AVLTree()
    if not os.path.exists(filepath):
        return tree

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Ordena os dados recuperados por 'created_at' antes de inserir para
    # garantir que a AVL seja reconstruída na ordem cronológica exata do estado anterior.
    data.sort(key=lambda x: x.get("created_at", 0))

    for item in data:
        task = Task.from_dict(item)
        tree.insert(task)

    return tree
