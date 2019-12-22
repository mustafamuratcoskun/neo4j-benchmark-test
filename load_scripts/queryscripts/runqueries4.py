# This Script Measures Time When Query : "Find Friends Of Friends of 1000 users with ids"

from neo4j import GraphDatabase
import time
import get_random


driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'benchmark'))

repeats = 10

with driver.session() as session:
    total_time = 0
    random_ids = get_random.getRandomIds(1000)
    for repeat in range(repeats):
        with session.begin_transaction() as tx:
            
            for id in random_ids:
                result = tx.run("MATCH (user:User {user_id:" + str(id) + "})-[:Friend*2]->(fof:User)" +
                                "WHERE NOT (user:User)-[:Friend]->(fof:User)" + 
                                "RETURN count(distinct fof.user_id)")
                avail = result.summary().result_available_after
                cons = result.summary().result_consumed_after
                
                
                total_time += avail + cons

avg_time = total_time / (repeats)
print('Average execution time:' +  str(avg_time / 1000) + 'seconds')

with open("./results-without-index/resultquery4.txt", "a") as file:
    file.write('Average execution time: ' +  str(avg_time/ 1000) + ' seconds')