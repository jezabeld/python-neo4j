from database.neo import NeoDB
from flask import current_app

def find_by_category(category):
    session = NeoDB().get_session()
    query = """ MATCH (n:Product {category: $category})
                OPTIONAL MATCH (n)<-[r:BOUGHT]-() 
                WITH n, count(r) as  purchases
                RETURN n {.*} as products
                ORDER BY purchases desc LIMIT 5"""
    result = session.run(query, category=category)
    nodes = []
    for item in result.data():
        nodes.append(item['products'])
    session.close()
    return nodes

def find_related_product(id):
    session = NeoDB().get_session()
    query = """MATCH (a:Product {id: $id})-[r:BOUGHT]-(u1:User)-[r2:BOUGHT]-(p:Product)
                WITH p, count(*) as purchases
                RETURN p {.*} as products
                ORDER BY purchases desc LIMIT 5"""
    result = session.run(query, id=id)
    nodes = []
    for item in result.data():
        nodes.append(item['products'])
    session.close()
    return nodes