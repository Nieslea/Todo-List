#######################################################
# Todo-Listen-Verwaltung mit Flask                    #
#                                                     #
# Lizenziert durch die Apache 2.0 Lizenz.             #
# Verwendung der Datei nur unter der Berücksichtigung #
# der Lizenzbedingungen erlaubt.                      #
#                                                     #
#######################################################

import uuid

from flask import Flask, request, jsonify, abort

# initialisiere Flask Server
app = Flask(__name__)

# Aufbau von Beispiel Listen
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'

todo_1_id = str(uuid.uuid4())
todo_2_id = str(uuid.uuid4())
todo_3_id = str(uuid.uuid4())
todo_4_id = str(uuid.uuid4())

# Aufbau der weiteren Struktur
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]

# Erstellen von Einträgen
todos = [
    {
        'id': todo_1_id,
        'name': 'Milch',
        'description': '',
        'list': todo_list_1_id
    },
    {
        'id': todo_2_id,
        'name': 'Arbeitsblätter ausdrucken',
        'description': '',
        'list': todo_list_2_id
    },
    {
        'id': todo_3_id,
        'name': 'Kinokarten kaufen',
        'description': '',
        'list': todo_list_3_id
    },
    {
        'id': todo_4_id,
        'name': 'Eier',
        'description': '',
        'list': todo_list_1_id
    }
]


# CORS headers für Swagger Editor
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PATCH,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# Funktion um alle Listen auszugeben
@app.route('/todo-list', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists), 200


# Funktion um eine neue Liste zu erstellen
@app.route('/todo-list', methods=['POST'])
def add_new_list():

    new_list = request.get_json(force=True)

    if not new_list or 'name' not in new_list:
        abort(400)

    new_list['id'] = str(uuid.uuid4())

    todo_lists.append(new_list)

    print(f'Created list: {new_list}')

    return jsonify(new_list), 201


# Funktionen um 1. eine bestimmte Liste auszugeben
# und um 2. eine bestimmte Liste zu löschen
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    global todos

    list_item = None

    for l in todo_lists:
        if str(l['id']) == list_id:
            list_item = l
            break

    if not list_item:
        abort(404)

    if request.method == 'GET':

        print('Returning todo list...')

        list_entries = [
            entry for entry in todos
            if entry['list'] == list_id
        ]

        return jsonify(list_entries), 200

    elif request.method == 'DELETE':

        print('Deleting todo list...')

        todo_lists.remove(list_item)

        todos = [
            todo for todo in todos
            if todo['list'] != list_id
        ]

        return '', 204


# Funktion um einen neuen Eintrag zu ergänzen
@app.route('/todo-list/<list_id>', methods=['POST'])
def add_new_entry(list_id):

    list_exists = False

    for todo_list in todo_lists:
        if str(todo_list['id']) == list_id:
            list_exists = True
            break

    if not list_exists:
        abort(404)

    new_entry = request.get_json(force=True)

    if not new_entry or 'name' not in new_entry:
        abort(400)

    new_entry['id'] = str(uuid.uuid4())
    new_entry['list'] = list_id

    if 'description' not in new_entry:
        new_entry['description'] = ''

    todos.append(new_entry)

    print(f'Added entry to list {list_id}: {new_entry}')

    return jsonify(new_entry), 201


# Funktionen um einen Eintrag zu Updaten
# und einen Eintrag zu löschen
@app.route('/todo-list/entry/<entry_id>', methods=['PATCH', 'DELETE'])
def handle_entry(entry_id):

    entry = None

    for todo in todos:
        if str(todo['id']) == entry_id:
            entry = todo
            break

    if not entry:
        abort(404)

    if request.method == 'PATCH':

        data = request.get_json(force=True)

        if not data:
            abort(400)

        if 'name' in data:
            entry['name'] = data['name']

        if 'description' in data:
            entry['description'] = data['description']

        print(f'Updated entry: {entry}')

        return jsonify(entry), 200

    elif request.method == 'DELETE':

        print(f'Deleting entry: {entry_id}')

        todos.remove(entry)

        return '', 204


# mögliche Fehlerausgaben
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad Request'
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error'
    }), 500


# Server starten
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)