ifeq ($(env),)
	env := local
endif

project_base_name = voladi

ifeq ($(project_suffix),)
	project_name := $(project_base_name)-$(env)
else
	project_name := $(project_base_name)-$(project_suffix)
endif

ifeq ($(service),)
	service := web
endif

USER_ID=$(shell id -u)
GROUP_ID=$(shell id -g)
COMPOSE_PROJECT_NAME=$(project_name)
export

compose_files = -f docker-compose.yml -f docker-compose.$(env).yml

private_compose_file = docker-compose.private.yml

ifneq ("$(wildcard $(private_compose_file))","")
	compose_files := $(compose_files) -f $(private_compose_file)
endif

ifeq ($(secrets),)
	secrets = secrets.yml
endif

ifneq ("$(wildcard $(secrets))","")
	compose_files := $(compose_files) -f $(secrets)
endif

build:
	@docker-compose $(compose_files) build

run:
	@docker-compose $(compose_files) up --force-recreate

run-d:
	@docker-compose $(compose_files) up -d

backup:
	@./db_dump.sh $(env)

backup-to-storage:
	@docker exec $(project_base_name)-web-$(env) bash -c "gosu www-data python /app/manage.py db_backup -c"

push:
	@docker-compose $(compose_files) push web

pull:
	@docker-compose $(compose_files) pull

connect:
	@docker exec -it $(project_base_name)-$(service)-$(env) bash

cs:
	@docker exec -it $(project_base_name)-web-$(env) bash -c "gosu www-data python manage.py collectstatic --no-input"

tailwind-dev:
	@docker exec -it voladi-$(service)-$(env) bash -c "python manage.py povulo dev"

stop:
	@docker-compose $(compose_files) stop

down:
	@docker-compose $(compose_files) down

destroy:
	@docker-compose -f docker-compose.yml -f docker-compose.local.yml down -v

logs:
	@docker-compose $(compose_files) logs -f --tail=200

default: build