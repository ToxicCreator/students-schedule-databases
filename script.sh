docker run -d --name psql_c -p 27017:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password postgres
docker run -d --name mongo_c -p 27015:27017 mongo
docker rm neo4j_c
docker run -d --name neo4j_c -p 7474:7474 -p 27018:7687 -e NEO4J_AUTH=neo4j/password neo4j
docker run -d --name elastic_c -p 27019:9200 -e "xpack.security.enabled=false" -e "discovery.type=single-node" elasticsearch:8.4.3
docker run -d --name redis_c -p 27016:6379 redis


python3.9  fill/fill_manager.py

docker container stop redis_c
docker rm redis_c
docker container stop psql_c
docker rm psql_c
#docker container stop neo4j_c
#docker rm neo4j_c
docker container stop mongo_c
docker rm mongo_c
docker container stop elastic_c
docker rm elastic_c
