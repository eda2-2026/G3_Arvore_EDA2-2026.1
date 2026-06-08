from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from src.avl_tree import AVLTree
from src.task import Task
from src.persistence import save_tasks, load_tasks

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas
DATA_FILE = "tasks.json"

# Carrega as tarefas ao iniciar
tree = load_tasks(DATA_FILE)

@app.route('/')
def index():
    """Retorna a página principal do frontend"""
    return render_template('index.html')

@app.route('/tree-info')
def tree_info():
    """Retorna a página com informações sobre a Árvore AVL"""
    return render_template('tree_info.html')

@app.route('/tree-visualization')
def tree_visualization():
    """Retorna a página de visualização da árvore AVL"""
    return render_template('tree_visualization.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Retorna apenas tarefas ativas (não concluídas)"""
    all_tasks = tree.get_all_ordered(order="desc")
    active_tasks = [task.to_dict() for task in all_tasks if not task.completed]
    return jsonify(active_tasks)

@app.route('/api/tasks/completed', methods=['GET'])
def get_completed_tasks():
    """Retorna apenas tarefas concluídas"""
    all_tasks = tree.get_all_ordered(order="desc")
    completed_tasks = [task.to_dict() for task in all_tasks if task.completed]
    return jsonify(completed_tasks)

@app.route('/api/tasks/all', methods=['GET'])
def get_all_tasks():
    """Retorna todas as tarefas (ativas e concluídas)"""
    all_tasks = tree.get_all_ordered(order="desc")
    return jsonify([task.to_dict() for task in all_tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Adiciona uma nova tarefa"""
    data = request.get_json()
    
    if not data or 'description' not in data or 'priority' not in data:
        return jsonify({"error": "description e priority são obrigatórios"}), 400
    
    try:
        priority = int(data['priority'])
        if priority < 1 or priority > 100:
            return jsonify({"error": "priority deve estar entre 1 e 100"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "priority deve ser um número inteiro"}), 400
    
    description = data['description'].strip()
    if not description:
        return jsonify({"error": "description não pode estar vazia"}), 400
    
    task = Task(description=description, priority=priority)
    tree.insert(task)
    save_tasks(tree, DATA_FILE)
    
    return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    """Marca uma tarefa como concluída"""
    all_tasks = tree.get_all_ordered(order="asc")
    
    # Encontra a tarefa
    target_task = None
    for task in all_tasks:
        if task.id == task_id:
            target_task = task
            break
    
    if not target_task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    
    target_task.completed = True
    save_tasks(tree, DATA_FILE)
    
    return jsonify(target_task.to_dict()), 200

@app.route('/api/tasks/<task_id>/uncomplete', methods=['PUT'])
def uncomplete_task(task_id):
    """Marca uma tarefa como não concluída"""
    all_tasks = tree.get_all_ordered(order="asc")
    
    # Encontra a tarefa
    target_task = None
    for task in all_tasks:
        if task.id == task_id:
            target_task = task
            break
    
    if not target_task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    
    target_task.completed = False
    save_tasks(tree, DATA_FILE)
    
    return jsonify(target_task.to_dict()), 200

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def edit_task(task_id):
    """Edita uma tarefa existente"""
    data = request.get_json()
    all_tasks = tree.get_all_ordered(order="asc")
    
    # Encontra a tarefa
    target_task = None
    for task in all_tasks:
        if task.id == task_id:
            target_task = task
            break
    
    if not target_task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    
    # Valida e atualiza descrição
    if 'description' in data:
        description = data['description'].strip()
        if not description:
            return jsonify({"error": "description não pode estar vazia"}), 400
        target_task.description = description
    
    # Valida e atualiza prioridade
    if 'priority' in data:
        try:
            priority = int(data['priority'])
            if priority < 1 or priority > 100:
                return jsonify({"error": "priority deve estar entre 1 e 100"}), 400
            
            # Se a prioridade mudou, precisamos reconstruir a árvore
            if priority != target_task.priority:
                # Remove a tarefa antiga
                tree.delete(target_task.priority, task_id)
                # Atualiza prioridade
                target_task.priority = priority
                # Reinsere com nova prioridade
                tree.insert(target_task)
        except (ValueError, TypeError):
            return jsonify({"error": "priority deve ser um número inteiro"}), 400
    
    save_tasks(tree, DATA_FILE)
    
    return jsonify(target_task.to_dict()), 200

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Remove uma tarefa específica pelo ID"""
    all_tasks = tree.get_all_ordered(order="asc")
    
    # Encontra a tarefa com o ID fornecido
    target_task = None
    for task in all_tasks:
        if task.id == task_id:
            target_task = task
            break
    
    if not target_task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    
    tree.delete(target_task.priority, task_id)
    save_tasks(tree, DATA_FILE)
    
    return jsonify({"message": "Tarefa removida com sucesso"}), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Retorna estatísticas sobre as tarefas"""
    all_tasks = tree.get_all_ordered(order="asc")
    active_tasks = [t for t in all_tasks if not t.completed]
    completed_tasks = [t for t in all_tasks if t.completed]
    
    if not all_tasks:
        return jsonify({
            "total": 0,
            "active": 0,
            "completed": 0,
            "max_priority": None,
            "min_priority": None,
            "avg_priority": 0,
            "tree_height": 0
        })
    
    if active_tasks:
        priorities = [task.priority for task in active_tasks]
        max_priority = max(priorities)
        min_priority = min(priorities)
        avg_priority = round(sum(priorities) / len(priorities), 2)
    else:
        max_priority = None
        min_priority = None
        avg_priority = 0
    
    return jsonify({
        "total_count": len(all_tasks),
        "active_count": len(active_tasks),
        "completed_count": len(completed_tasks),
        "max_priority": max_priority,
        "min_priority": min_priority,
        "avg_priority": avg_priority,
        "tree_height": tree.get_height(tree.root)
    })

@app.route('/api/tree-structure', methods=['GET'])
def get_tree_structure():
    """Retorna a estrutura da árvore para visualização"""
    def build_tree_json(node):
        if not node:
            return None
        
        # Calcula o balance factor
        left_height = node.left.height if node.left else -1
        right_height = node.right.height if node.right else -1
        balance_factor = left_height - right_height
        
        return {
            "priority": node.key,
            "tasks_count": len(node.tasks),
            "height": node.height,
            "balance_factor": balance_factor,
            "left": build_tree_json(node.left),
            "right": build_tree_json(node.right)
        }
    
    return jsonify(build_tree_json(tree.root))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
