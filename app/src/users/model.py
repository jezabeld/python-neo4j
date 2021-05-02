from uuid import uuid1
from database.neo4j import NeoDB
from flask import current_app

def user_serializer(record):
    return {'id': record['id'], 
            'name': record['name'], 
            'lastname': record['lastname'], 
            'email': record['email'] 
    }

def find_db(id):
    session = NeoDB().get_session()
    query = """ MATCH (n:User {id: $id}) 
                RETURN n.id as id, n.name as name, n.lastname as lastname, n.email as email """
    result = session.run(query, id=id).single()
    user = result.data() if result != None else result
    session.close()
    return user 

def get_db():
    session = NeoDB().get_session()
    query = """ MATCH (n:User) 
                RETURN n.id as id, n.name as name, n.lastname as lastname, n.email as email"""
    result = session.run(query)
    nodes = result.data()
    session.close()
    return nodes

def save_db(user):
    user['id'] = str(uuid1())
    query = """ CREATE (n:User {id: $id, name: $name, lastname: $lastname, email: $email}) 
                RETURN n.id as id, n.name as name, n.lastname as lastname, n.email as email"""
    session = NeoDB().get_session()
    result = session.write_transaction(lambda tx: tx.run(query, user_serializer(user)).single())
    user = result.data() if result != None else result
    session.close()
    return user

def delete_db(id):
    user = find_db(id) 
    query = """ MATCH (n:User {id: $id}) 
                DETACH DELETE n"""
    session = NeoDB().get_session()
    result = session.write_transaction(lambda tx: tx.run(query, id = id))
    current_app.logger.info(result.data())
    session.close()
    return user

def update_db(user):
    id = user['id']
    query = """ MATCH (n:User {id: $id}) 
                SET n.name = $name, n.lastname = $lastname, n.email = $email
                RETURN n.id as id, n.name as name, n.lastname as lastname, n.email as email"""
    session = NeoDB().get_session()
    result = session.write_transaction(lambda tx: tx.run(query, user_serializer(user)).single())
    user = result.data() if result != None else result
    session.close()
    return user

