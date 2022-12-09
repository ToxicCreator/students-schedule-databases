# Микросервисы
## Docker Compose
Чтобы собрать и запустить docker compose нужно выполнить следующую команду:
```sh
docker-compose --env-file ./.env up -d --build
```
## IP контейнеров:
MainHub - `10.5.0.10:9000`
Mongo - `10.5.0.11:9001`
Neo4j - `10.5.0.12:9002`
Redis - `10.5.0.13:9003`
ElasticSearch - `10.5.0.14:9004`
PostgreSql - `10.5.0.15:9005`

![img.png](MainHub/img.png)

![image](https://user-images.githubusercontent.com/87932748/206470641-0fea3b3f-b570-4bc1-a717-153edb633ff3.png)
