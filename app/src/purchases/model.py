from uuid import uuid1
from database.neo import NeoDB
from flask import current_app
from errors import ProductNotFound

def find_db(user_id,id):
    session = NeoDB().get_session()
    query = """ MATCH (u:User {id: $user_id})-[r:BOUGHT {id: $id}]-(p:Product)
                WITH r.id as purchase_id,u.id as user_id, r.date as date, sum(r.quantity) as qty, collect( r{.item, .price, .quantity}) as items
                RETURN {purchase_id: purchase_id, user_id: user_id, date: date, total: round(reduce(t=0, i in items | t + (i.price * i.quantity)),2),  qty:qty, items:items} as purchase"""
    result = session.run(query, {'id':id, 'user_id': user_id}).single()
    purchase = result.data()['purchase'] if result != None else result
    session.close()
    return purchase 

def get_db(user_id):
    session = NeoDB().get_session()
    query = """ MATCH (u:User {id: $user_id})-[r:BOUGHT ]-(p:Product)
                WITH r.id as purchase_id,u.id as user_id, r.date as date, sum(r.quantity) as qty, collect( r{.item, .price, .quantity}) as items
                RETURN {purchase_id: purchase_id, user_id: user_id, date: date, total: round(reduce(t=0, i in items | t + (i.price * i.quantity)),2),  qty:qty, items:items} as purchase"""
    result = session.run(query, {'user_id':user_id})
    purchases = []
    for item in result.data():
        purchases.append(item['purchase'])
    session.close()
    return purchases

def save_db(user,products):
    purchase_id = str(uuid1())

    query = f"MATCH (u:User {{id: '{user['id']}'}}) "
    i = 0
    for item in products:
        i += 1
        query += f", (p{i}:Product {{id: '{item['id']}'}}) "
    query += " CREATE "
    creadores = []
    i = 0
    for item in products:
        i += 1
        creadores.append(f""" (u)-[r{i}:BOUGHT {{id: '{purchase_id}', item: '{item['title']}', quantity: {item['quantity']}, price: {item['price']}, date: timestamp()}}]->(p{i}) """)
    query += ",".join(creadores) 
    session = NeoDB().get_session()
    session.write_transaction(lambda tx: tx.run(query).single())
    session.close()
    purchase = find_db(user['id'],purchase_id)
    return purchase

