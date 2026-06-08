from flask import Flask, render_template, request, jsonify
import os
from src.avl_tree import AVLTree
from src.task import Task
from src.persistence import save_tasks, load_tasks

app = Flask(__name__)
DATA_FILE = "tasks.json"

# Carrega as tarefas ao iniciar
tree = load_tasks(DATA_FILE)

@app.route('/')
def index():
    """Retorna a página principal do frontend"""
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Retorna todas as tarefas ordenadas por prioridade (descendente)"""
    tasks = tree.get_all_ordered(order="desc")
    return jsonify([task.to_dict() for task in tasks])

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

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Remove uma tarefa específica pelo ID"""
    tasks = tree.get_all_ordered(order="asc")
    
    # Encontra a tarefa com o ID fornecido
    target_task = None
    for task in tasks:
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
    tasks = tree.get_all_ordered(order="asc")
    
    if not tasks:
        return jsonify({
            "total": 0,
            "max_priority": None,
            "min_priority": None,
            "avg_priority": 0
        })
    
    priorities = [task.priority for task in tasks]
    
    return jsonify({
        "total": len(tasks),
        "max_priority": max(priorities),
        "min_priority": min(priorities),
        "avg_priority": round(sum(priorities) / len(priorities), 2),
        "tree_height": tree.get_height(tree.root)
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
