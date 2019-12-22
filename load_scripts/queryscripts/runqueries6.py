# This Script Measures Time When Query : "Find 10000 users with random ids and get their ages"
 
from neo4j import GraphDatabase
import time
import get_random

#cypher_query = """MATCH (user1:User {user_id:14}),(user2:User {user_id: 1000}),
#p = shortestPath((user1)-[*..15]-(user2))
#RETURN length(p)"""


driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'benchmark'))

repeats = 10

with driver.session() as session:
    total_time = 0
    randomShortestIds = get_random.getRandomShortestPathIds(1000)
    for repeat in range(repeats):
        with session.begin_transaction() as tx:
            
            for startId,endId in randomShortestIds:
                result = tx.run("MATCH (user1:User {user_id:" + str(startId) + "}),(user2:User {user_id: " + str(endId) + "})," + 
                "p = shortestPath((user1)-[*..15]-(user2))" + 
                "RETURN length(p)")
                avail = result.summary().result_available_after
                cons = result.summary().result_consumed_after
                
                
                total_time += avail + cons

avg_time = total_time / (repeats)
print('Average execution time:' +  str(avg_time / 1000) + 'seconds')

with open("./results-without-index/resultquery6.txt", "a") as file:
    file.write('Average execution time: ' +  str(avg_time/ 1000) + ' seconds')