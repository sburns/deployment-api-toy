import os
from warnings import warn
import json

from invoke import task, run
import requests

ENDPOINT = 'https://api.github.com/repos/sburns/deployment-api-toy/deployments'


@task
def deploy(task='deploy', env='production', desc='my deploy'):
    r = create_deployment(rev_parse(), task=task, environment=env, description=desc)
    response = r.json()
    status_url = response['statuses_url']

    deploy_state = actually_deploy()

    create_status(status_url, 'success')

def actually_deploy():
    return 'success'


def create_deployment(ref, task='deploy', auto_merge=True, payload=None,
        environment='production', description=''):
    data = {
        'ref': ref,
        'task': task,
        'auto_merge': auto_merge,
        'payload': json.dumps(payload) if payload else "",
        'environment': environment,
        'description': description,
    }
    session = prepare_session()
    return session.post(ENDPOINT, json=data)


def create_status(url, state):
    session = prepare_session()
    return session.post(url, json={'state': state})

def get_token():
    oauth_token = os.environ.get('GITHUB_DEPLOYMENT_API_TOKEN', None)
    if not oauth_token:
        warn('''Unauthenticated API calls are rate-limited.

Store a Personal Access Token in GITHUB_DEPLOYMENT_API_TOKEN''')
    return oauth_token


def prepare_session():
    token = get_token()
    session = requests.Session()
    if token:
        session.headers['Authorization'] = 'token {}'.format(token)
    return session


def rev_parse(ref='HEAD'):
    return run('git rev-parse {}'.format(ref), hide='out').stdout.strip()

