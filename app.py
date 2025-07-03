from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'],description=data.get('description', ''))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({'message': 'Nova tarefa criada com sucesso', 'id': new_task.id})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    output = {
        "tasks": [task.to_dict() for task in tasks],
        "total": len(tasks)
    }
    return jsonify(output)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        return jsonify(task.to_dict())
    return jsonify({'message': 'Tarefa não encontrada'}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = next((task for task in tasks if task.id == task_id), None)
    if not task:
        return jsonify({'message': 'Tarefa não encontrada'}), 404
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    return jsonify({'message': 'Tarefa atualizada com sucesso'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return jsonify({'message': 'Tarefa excluída com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)