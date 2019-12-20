$NEO4J_HOME/bin/neo4j-admin import $NEO4J_DB_DIR \
  --id-type=INTEGER \
  --nodes:User "../data/profiles-header.csv,../data/soc-pokec-profiles-new.csv" \
  --relationships:Friend "../data/relationships-header.csv,../data/soc-pokec-relationships-new.csv" \
  --delimiter '|'
  