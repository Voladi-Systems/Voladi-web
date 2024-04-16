import sys
from pathlib import Path
from time import sleep

from dotenv import dotenv_values
from fabric.connection import Connection
from fabric.tasks import task
from munch import Munch


env = Munch({
    **dotenv_values('.env'),
})

env.GIT_REPO_URL = env.REPOSITORY_URL
env.BRANCH = env.COMMIT_REF_NAME
env.APP_PATH = Path(env.get('PROJECT_ROOT_PATH', '/projects')) / env.PROJECT_NAME
CHECK_AFTER_SECONDS = env.get('CHECK_AFTER_SECONDS')


@task
def deploy(context):
    if not env.GCR_AUTH_TOKEN:
        raise ValueError('No CI token set')

    with Connection(env.HOST, user=env.USER, port=int(env.get('PORT', 22))) as c:
        c.run(f'mkdir -p {env.APP_PATH}')
        with c.cd(env.APP_PATH):
            clone(c)
            backup(c)
            pull_images(c)
            run(c)


def clone(c):
    if c.run(f'test -d .git', warn=True).failed:
        print('\nCloning from GIT')
        c.run(f'git clone -b {env.BRANCH} {env.GIT_REPO_URL} .')
        print('\nCopying GCP credentials')
        c.run(f'cp ~/{env.GCP_CREDENTIALS_NAME} .')

    print('\nUpdate repository URL')
    c.run(f'git remote set-url origin {env.GIT_REPO_URL}')

    print('\nResetting branch')
    c.run(f'git reset --hard origin/{env.BRANCH}')

    print('\nFetching from GIT')
    c.run(f'git checkout {env.BRANCH}')
    c.run(f'git fetch origin {env.BRANCH}')
    c.run(f'git pull origin {env.BRANCH}')


def pull_images(c):
    print('\nPulling images from registry')
    c.run(f'echo {env.GCR_AUTH_TOKEN} | docker login -u oauth2accesstoken --password-stdin {env.get("CONTAINER_REGISTRY", "eu.gcr.io")}')
    if not c.run(f'test -f ./services.sh', warn=True).failed:
        c.run(f'./services.sh pull env={env.ENV}')
    else:
        c.run(f'make pull env={env.ENV}')


def backup(c):
    if env.get('MAKE_BACKUP'):
        try:
            c.run(f'make backup-to-storage env={env.ENV}')
        except Exception as e:
            print(e)
            if env.get('BACKUPS_REQUIRED'):
                sys.exit('Backup not created, aborting')


def run(c):
    if env.SHOULD_RUN:
        if c.run(f'test -f secrets.yml', warn=True).failed:
            print('It seems this is the first deployment for this project.\n'
                  'Please create the site\'s "secrets.yml" file and re-run the pipeline.')
            return
        run_cmd = f'make run-d env={env.ENV}'
        if not c.run(f'test -f ./services.sh', warn=True).failed:
            run_cmd = f'./services.sh run-d {env.ENV}'
        print('\nStarting containers')
        c.run(run_cmd)
        confirm_deployment_running(c)


def confirm_deployment_running(c):
    try:
        check_after_seconds = int(CHECK_AFTER_SECONDS)
    except Exception:
        check_after_seconds = None

    try:
        expected_services = int(env.EXPECTED_SERVICES)
    except Exception:
        expected_services = None

    if isinstance(check_after_seconds, int) and check_after_seconds > 0 and expected_services:
        sleep(check_after_seconds)
        result = c.run(f'docker ps -q \
            --filter label="com.voladi.project={env.PROJECT_NAME}" \
            --filter label="com.voladi.environment={env.ENV}" \
            --filter status=running')
        running_services = len(result.stdout.strip().splitlines())

        if running_services != expected_services:
            all_services = c.run(f'docker ps -a \
                --filter label="com.voladi.project={env.PROJECT_NAME}" \
                --filter label="com.voladi.environment={env.ENV}"')
            print(f'\nExpected "{expected_services}" services but only "{running_services}" running.')
            print(all_services.stdout.strip())
            sys.exit('One or more services did not start up correctly.')
