#!bin/bash

sudo sysctl -w vm.max_map_count=262144
sudo docker rm -f elastic_c || true
sudo docker run -d --name elastic_c -p 8003:9200 -e "xpack.security.enabled=false" -e "discovery.type=single-node" elasticsearch:8.4.2
