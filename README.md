# deployment-api-toy
Toy repo to tinker with the Github Deployment API

## Setup

- Create a [Personal Access Token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/)
  - This token only needs the `repo_deployment` scope.
- Store the token in the `GITHUB_DEPLOYMENT_API_TOKEN` environment variable
- Get a python virtualenv going
- `pip install -r requirements.txt`

## What's going on here

The interesting tidbis are in `tasks.py`. Using [invoke](http://pyinvoke.org), this file provides a
deployment command run as so:

```
$ invoke deploy
```

This command creates a [deployment](https://developer.github.com/v3/repos/deployments/) through Github's
API with various extra bits of information and a [status](https://developer.github.com/v3/repos/deployments/#create-a-deployment-status) on top of it.

Viewing [old](http://github.com/sburns/deployment-api-toy/pull/1) [PRs](http://github.com/sburns/deployment-api-toy/pull/2), you can see that deployments are displayed in-line with commits.

## Why

This is a simple, easy way to add a deployment audit log to your application.

