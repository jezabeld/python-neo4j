from uuid import uuid1

# usuarios de prueba
usuarios = [
{"name": "Tom", "age": 10, "id":"106e9920-9ff4-11eb-8d79-0242ac160002"},
{"name": "Mark", "age": 5, "id":"17b9dbd6-9ff4-11eb-9895-0242ac160002"},
{"name": "Pam", "age": 7, "id":"1ce1eeaa-9ff4-11eb-b5c6-0242ac160002"}
]

def save_db(user):
    user['id'] = str(uuid1())
    usuarios.append(user)
    return user

def find_db(id):
    user = next((item for item in usuarios if item["id"] == id), None)
    print(usuarios)
    return user

def get_db():
    return usuarios

def update_db(user):
    global usuarios
    id = user['id']
    usuarios = [item if item["id"] != id else user for item in usuarios] 
    user = next((item for item in usuarios if item["id"] == id), None)
    return user

def delete_db(id):
    global usuarios
    user = next((item for item in usuarios if item["id"] == id), None)
    usuarios = list(filter(lambda item: item['id'] != id, usuarios))
    return user