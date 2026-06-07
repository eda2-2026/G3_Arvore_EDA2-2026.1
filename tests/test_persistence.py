from src.task import Task
from src.avl_tree import AVLTree
from src.persistence import save_tasks, load_tasks

def test_persistence_empty_file(tmp_path):
    filepath = str(tmp_path / "empty.json")
    # Tentar carregar de arquivo que não existe deve retornar árvore vazia
    tree = load_tasks(filepath)
    assert tree.root is None


def test_persistence_save_and_load(tmp_path):
    filepath = str(tmp_path / "tasks_test.json")

    # Monta a árvore inicial
    tree = AVLTree()
    t1 = Task("Exercício de EDA 2", 10)
    t2 = Task("Prova de EDA2", 80)
    t3 = Task("Trabalho de Calculo 2", 90) 
    t4 = Task("Projeto de Banco de Dados", 50)

    tree.insert(t1)
    tree.insert(t2)
    tree.insert(t3)
    tree.insert(t4)

    # Salva no arquivo temporário
    save_tasks(tree, filepath)

    # Carrega em uma nova árvore
    loaded_tree = load_tasks(filepath)

    # Lista ordenada decrescente para comparação
    original_tasks = tree.get_all_ordered(order="desc")
    loaded_tasks = loaded_tree.get_all_ordered(order="desc")

    assert len(loaded_tasks) == 4
    
    # Valida se os campos foram reconstruídos idênticos
    for orig, load in zip(original_tasks, loaded_tasks):
        assert orig.id == load.id
        assert orig.description == load.description
        assert orig.priority == load.priority
        assert orig.created_at == load.created_at

    # Verifica a ordem decrescente de prioridades
    assert loaded_tasks[0].id == t3.id
    assert loaded_tasks[1].id == t4.id
    assert loaded_tasks[2].id == t2.id
    assert loaded_tasks[3].id == t1.id
