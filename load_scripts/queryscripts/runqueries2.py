# This Script Measures Time When Query : "Return All Friend Relationship Count In Graph.db"

 
from neo4j import GraphDatabase
import time


driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'benchmark'))

repeats = 10

with driver.session() as session:
    total_time = 0
    for repeat in range(repeats):
        with session.begin_transaction() as tx:
            
            
            result = tx.run("MATCH (u1:User)-[:Friend]->(u2:User) Return Count(*)")
            avail = result.summary().result_available_after
            cons = result.summary().result_consumed_after
                
            
            total_time += avail + cons
            

avg_time = total_time / (repeats)

print('Average execution time:', str(avg_time / 1000), 'seconds')

with open("/results-without-index/resultquery2.txt", "a") as file:
    file.write('Average execution time:' +  str(avg_time / 1000) + 'seconds')
