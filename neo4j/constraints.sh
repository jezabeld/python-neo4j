#!/bin/bash

sleep 15
echo '[NEO4J dbConfig] Creating constraints for User.id'
until cypher-shell -a neo4j 'CREATE CONSTRAINT user_id IF NOT EXISTS ON (n:User) ASSERT n.id IS UNIQUE;'
do
  echo "[NEO4J dbConfig] CREATE CONSTRAINT user_id failed. Waiting 10 seconds to retry."
  sleep 10
done
echo "[NEO4J dbConfig] CREATE CONSTRAINT user_id succeed."

echo '[NEO4J dbConfig] Creating constraints for Product.id'
until cypher-shell -a neo4j 'CREATE CONSTRAINT product_id IF NOT EXISTS ON (n:Product) ASSERT n.id IS UNIQUE;'
do
  echo "[NEO4J dbConfig] CREATE CONSTRAINT product_id failed. Waiting 10 seconds to retry."
  sleep 10
done
echo "[NEO4J dbConfig] CREATE CONSTRAINT product_id succeed."
