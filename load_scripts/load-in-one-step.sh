#!/bin/bash

./delete-neo4j-graphdb.sh && ./import-data-from-csv.sh && ./restart-neo4j.sh