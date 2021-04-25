from uuid import uuid1
from database.neo4j import NeoDB
from flask import current_app

def product_serializer(record):
    return {'id': record['id'], 
            'title': record['title'], 
            'category': record['category'], 
            'price': record['price'] ,
            'author': record['author'] 
    }

def filter_products(author, category):
    filter = []
    if (author != None):
        filter.append("author:$author")
    if (category != None):
        filter.append("category:$category")
    return "{" + ",".join(filter) + "}"

def find_db(id):
    session = NeoDB().get_session()
    query = """ MATCH (n:Product {id: $id}) 
                RETURN n.id as id, n.title as title, n.category as category, n.price as price, n.author as author """
    result = session.run(query, id=id).single()
    product = result.data() if result != None else result
    session.close()
    return product 

def get_db(author,category):
    filt = filter_products(author, category)
    current_app.logger.info({'filt': filt})

    session = NeoDB().get_session()
    query = f""" MATCH (n:Product {filt}) 
                RETURN n.id as id, n.title as title, n.category as category, n.price as price, n.author as author """
    result = session.run(query, {'author':author,'category':category})
    nodes = result.data()
    session.close()
    return nodes

def save_db(product):
    product['id'] = str(uuid1())
    query = """ CREATE (n:Product {id: $id, title: $title, category: $category, price: $price, author: $author }) 
                RETURN n.id as id, n.title as title, n.category as category, n.price as price, n.author as author """
    session = NeoDB().get_session()
    result = session.write_transaction(lambda tx: tx.run(query, product_serializer(product)).single())
    product = result.data() if result != None else result
    session.close()
    return product

def delete_db(id):
    product = find_db(id) 
    query = """ MATCH (n:Product {id: $id}) 
                DETACH DELETE n"""
    session = NeoDB().get_session()
    result = session.write_transaction(lambda tx: tx.run(query, id = id))
    current_app.logger.info(result.data())
    session.close()
    return product

def update_db(product):
    id = product['id']
    query = """ MATCH (n:Product {id: $id}) 
                SET n.title = $title, n.category = $category, n.price = $price, n.author = $author
                RETURN n.id as id, n.title as title, n.category as category, n.price as price, n.author as author """
    session = NeoDB().get_session()
    result = session.write_transaction(lambda tx: tx.run(query, product_serializer(product)).single())
    product = result.data() if result != None else result
    session.close()
    return product

