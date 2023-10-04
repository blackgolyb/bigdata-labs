export DOCKER_DEFAULT_PLATFORM=linux/amd64

up:
	docker compose -f docker-compose-local.yaml up -d

down:
	docker compose -f docker-compose-local.yaml down --remove-orphans

up_deploy:
	docker compose -f docker-compose-deploy.yaml --env-file ./.env.default up -d

up_deploy_rebuild:
	docker compose -f docker-compose-deploy.yaml --env-file ./.env.default up --build -d

down_deploy:
	docker compose -f docker-compose-deploy.yaml --env-file ./.env.default down --remove-orphans
