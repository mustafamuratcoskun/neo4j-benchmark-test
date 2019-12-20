# This Script Measures Time When Query : "Find 10000 users with random ids and get their ages"
 
from neo4j import GraphDatabase
import time
import random
def getRandomIds():
    random_ids = list()
    for i in range(1,10000):
        random_ids.append(random.randint(1,1630000))
    return random_ids
    
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'benchmark'))

repeats = 3
cypher = "MATCH (u:User {user_id : 13}) RETURN u.AGE"

with driver.session() as session:
    total_time = 0
    for repeat in range(repeats):
        with session.begin_transaction() as tx:
            start = time.time()
            random_ids = getRandomIds()

            for id in random_ids:
                tx.run("MATCH (u:User {user_id :" + str(id) + "}) RETURN u.AGE")
            if (repeat != 0):
                total_time += time.time() - start

avg_time = total_time / (repeats - 1)

print('Average execution time:', avg_time, 'seconds')