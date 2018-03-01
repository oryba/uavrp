build-image:
	docker build -t hashcode:latest -f ./Dockerfile .

build: build-image clean

clean:
	docker rmi -f $$(docker images -f "dangling=true" -q) || true

up:
	docker-compose -f ./docker-compose.yml up -d hashcode_bash

stop:
	docker-compose -f ./docker-compose.yml stop hashcode_bash

rm:
	docker-compose -f ./docker-compose.yml rm -f hashcode_bash

down: stop rm

down-pycharm:
	docker-compose -f ./docker/docker-compose.yml stop hashcode
	docker-compose -f ./docker/docker-compose.yml rm -f hashcode

bash:
	docker exec -it data_lake_etl_bash_1 bash
