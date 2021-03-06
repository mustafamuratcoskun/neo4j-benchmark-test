# This Script Measures Time When Query : "Find 10000 users with ids and update their age by 1"

from neo4j import GraphDatabase
import time
import get_random


driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'benchmark'))

repeats = 10

with driver.session() as session:
    total_time = 0
    random_ids = get_random.getRandomIds(10000)
    for repeat in range(repeats):
        with session.begin_transaction() as tx:
            
            for id in random_ids:
                result = tx.run("MATCH (u:User {user_id :" + str(id) + "}) SET u.AGE = u.AGE + 1")
                avail = result.summary().result_available_after
                cons = result.summary().result_consumed_after
                
                
                total_time += avail + cons

avg_time = total_time / (repeats)
print('Average execution time:' +  str(avg_time / 1000) + 'seconds')

with open("./results-without-index/resultquery5.txt", "a") as file:
    file.write('Average execution time: ' +  str(avg_time/ 1000) + ' seconds')