Neo4j Benchmark with Pokec Data Set

Data Set Available On : https://snap.stanford.edu/data/soc-Pokec.html

Dataset is not available in this repository because the size is huge. 
--------------------------------------
Pokec Social Network Benchmark Dataset

Hardware & Major environment
---------------------------------------
Model Name:	MacBook Pro
Model Identifier:	MacBookPro11,3
Processor Name:	Intel Core i7
Processor Speed:	2,3 GHz
Number of Processors:	1
Total Number of Cores:	4
L2 Cache (per Core):	256 KB
L3 Cache:	6 MB
Hyper-Threading Technology:	Enabled
Memory:	16 GB

Java build 1.8.0_191

Following python modules are required

sudo pip install tornado
sudo pip install neo4j-driver
sudo pip install requests

Install Neo4j
---------------------------------------
Make sure you have already install Neo4j and arrange your system paths to use Neo4j commands through the terminal.

Comfigure Neo4j memory
$NEO4J_HOME/bin/neo4j-admin memrec

For this benchmark, I use the initial memory configuration of Neo4j.

In order to warm up the cache before executing any queries, first make sure you have called "CALL apoc.warmup.run()" command
from cypher-shell. cypher-shell came with Neo4j and you can execute this command after arranging your $NEO4J_HOME.

Append the 3 lines to $NEO4J_HOME/conf/neo4j.conf

Move apoc-3.5.0.2-all.jar to $NEO4J_HOME/plugins/
mv apoc-3.5.0.2-all.jar $NEO4J_HOME/plugins/

Append following lines $NEO4J_HOME/conf/neo4j.conf/neo4j.conf
dbms.security.procedures.unrestricted=apoc.*

Start server
$NEO4J_HOME/bin/neo4j start 

Stop server
$NEO4J_HOME/bin/neo4j stop

Create/change username and password cypher-shell, then exit
$NEO4J_HOME/bin/cypher-shell
user:neo4j
pass:neo4j

#change password
neo4j> CALL dbms.changePassword('benchmark')

#exit shell

neo4j> :exit

#log in again
$NEO4J_HOME/bin/cypher-shell -u neo4j -p benchmark

Bulk Loading Raw Data
----------------------------------------
I load all nodes and relationships with Neo4j Import API. 
If you want to load all raw data and create your graph database with this API,
you can view /queryscripts/import-data-from-csv.sh file.

If you want to reload all raw data again, you can simply execute ./load_scripts/load-in-one-step.sh file.
This script delete all graph.db data, stop the Neo4j server, import again and start Neo4j again in one step.

Statistics While Loading All Raw Data

# These statistics come directly from console log.
--------------------------------------------------------
Available resources:
  Total machine memory: 16.00 GB
  Free machine memory: 8.25 GB
  Max heap memory : 3.56 GB
  Processors: 8
  Configured max memory: 11.20 GB
  High-IO: true
--------------------------------------------------------
(1/4) Node import 2019-12-21 16:30:56.588+0300
  Estimated number of nodes: 1.08 M
  Estimated disk space usage: 2.39 GB
  Estimated required memory usage: 1.01 GB
--------------------------------------------------------
(2/4) Relationship import 2019-12-21 16:31:06.925+0300
  Estimated number of relationships: 40.27 M
  Estimated disk space usage: 1.28 GB
  Estimated required memory usage: 1.02 GB
--------------------------------------------------------
(3/4) Relationship linking 2019-12-21 16:31:19.253+0300
  Estimated required memory usage: 1.01 GB
--------------------------------------------------------
(4/4) Post processing 2019-12-21 16:31:30.019+0300
  Estimated required memory usage: 1020.01 MB
--------------------------------------------------------
IMPORT DONE in 36s 435ms. (Total Time)

Imported:
  1630472 nodes
  30524918 relationships
  39217359 properties
Peak memory usage: 1.05 GB

Measure Neo4j Loaded Data Size

#Execute This Command

sudo du -hc $NEO4J_HOME/data/databases/graph.db/*store*
------------------------------------------------------------------------
Creating Index on User(user_id) Property

In this dataset, we have only node type Profile (imported as User ). Therefore,
I created index on user_id property of Node Type User.

# Execute The Following Command Through cypher-shell
CREATE INDEX ON :User(user_id);

0 rows available after 964 ms, consumed after another 0 ms
Added 1 indexes

# If you want to drop index from :User(user_id) , you can execute following command.
DROP INDEX ON :User(user_id)

Total Index Size Of The Database: 404Kb. You can measure this size executing the command 
that we use while measuring graph.db size before.
------------------------------------------------------------------------

Run benchmark
----------------------------------------
# Warm up NEO4J, wait until finished and keep the cypher-shell open(warm up may take a long time)
neo4j>call apoc.warmup.run(true, true);

After warming up, I test different queriest for 10 times and calculate their averages, output results to
./load_scripts/queryscripts/result-with-index/*resultquery*.txt and 
./load_scripts/queryscripts/result-without-index/*resultquery*.txt.
---------------------------------------------------------------------------
Results Without Index

# Query 1
"Find 10000 users with ids and get their ages"
Average execution time: 2.3032222222222223 seconds

# Query 2
"Return All Friend Relationship Count In Graph.db"
Average execution time: 87.831 seconds

# Query 3
"Find Friends Of 1000 users with ids and get friends' user_id"
Average execution time: 4.0456999999999996 seconds

# Query 4
"Find Friends Of Friends of 1000 users with ids"
Average execution time: 45.91822222222222 seconds

# Query 5
"Find 10000 users with ids and update their age by 1"
Average execution time: 20.3614444444444445 seconds

# Query 6
"Find Between Shortest Path Of 1000 Different Users"
Average execution time: 14.773444444444445 seconds
---------------------------------------------------------------------------

Results With Index

# Query 1
"Find 10000 users with ids and get their ages"
Average execution time: 1.2232432 seconds

# Query 2
"Return All Friend Relationship Count In Graph.db"
Average execution time: 56.831 seconds

# Query 3
"Find Friends Of 1000 users with ids and get friends' user_id"
Average execution time: 3.27726 seconds

# Query 4
"Find Friends Of Friends of 1000 users with ids"
Average execution time: 32.63756 seconds

# Query 5
"Find 10000 users with ids and update their age by 1"
Average execution time: 17.86121 seconds

# Query 6
"Find Between Shortest Path Of 1000 Different Users"
Average execution time: 8.723723232 seconds
---------------------------------------------------------------------------

Detailed Benchmark Report can be found in ./benchmark-report.pdf

