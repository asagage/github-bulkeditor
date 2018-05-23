from github import Github, GithubException
import requests, json
import os, sys
import config

class BulkEditor(object):
    _g = None
    _token = None
    _baseURL = 'https://api.github.com'
    _files = None
    _orgs = None
    _exclude = None

    def __init__(self, token=None, baseURL=None):
        if not token:
            try:
                token = os.environ["GITHUB_BULKEDITOR_AUTHTOKEN"]
            except KeyError:
                print(
                    "Please set the environment variable "
                    "GITHUB_BULKEDITOR_AUTHTOKEN")
                sys.exit(1)
        self._token = token

        if baseURL:
            self.baseURL = baseURL
        else:
            if config.baseURL:
                self._baseURL = config.baseURL

        self._orgs = config.orgs
        self._exclude = config.exclude
        self._files = config.files

        self._g = Github(base_url=self._baseURL, login_or_token=self._token)

    def orgs(self, orgs):
        self._orgs = orgs

    def exclude(self, exclude):
        self._exclude = exclude

    def files(self, files):
        self._files = files

    def enable_branch_protection(self, repository):
        # Create an issue on github.com using the given parameters
        # Url to create issues via POST
        # /repos/:owner/:repo/branches/:branch/protection
        method = 'PUT'
        url = self._baseURL + '/repos/%s/branches/master/protection' % (
            repository.full_name)

        # prepare object for branch protection
        data = {
            "required_status_checks": {
                "strict": True, "contexts": []
            },
            "enforce_admins": False,
            "required_pull_request_reviews": {
                "dismissal_restrictions": {
                },
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": True,
                "required_approving_review_count": 1
            },
            "restrictions": None
        }

        success_msg = 'Successfully enabled branch protection'
        fail_msg = 'Could not enable branch protection'

        self.request_raw(method, url, data, success_msg, fail_msg)

    def disable_branch_protection(self, repository):
        # Create an issue on github.com using the given parameters
        # Url to create issues via POST
        # /repos/:owner/:repo/branches/:branch/protection
        method = 'DELETE'
        url = self._baseURL + '/repos/%s/branches/master/protection' % (
            repository.full_name)

        # prepare object for branch protection
        data = dict()

        success_msg = 'Successfully disabled branch protection'
        fail_msg = 'Could not disable branch protection'

        self.request_raw(method, url, data, success_msg, fail_msg)


    def request_raw(self, method, url, data, success_msg, fail_msg, headers = None):
        # Create an issue on github.com using the given parameters
        # Url to create issues via POST
        # /repos/:owner/:repo/branches/:branch/protection
             # Headers
        if not headers:
            headers = {
                "Authorization": "token %s" % self._token,
                "Accept": 'application/vnd.github.luke-cage-preview+json'
            }

        payload = json.dumps(data)

        # Add the issue to our repository
        response = requests.request(method, url, data=payload, headers=headers)
        if response.status_code in (200, 204):
            print(success_msg)
        else:
            print(fail_msg)
            print('Response:', response.content)

    def commit_file(self, repository, path, file):
        try:
            repository.get_contents(path).sha
            print("File exists:", path)
            pass
            # disabled the ability to update for now

            # repository.update_file(
            #     path=path,
            #     message='Template update',
            #     content=file,
            #     sha=sha
            # )
        except GithubException:
            repository.create_file(
                path=path,
                message='Template initial commit',
                content=file
            )
            print("Initial commit of new file {}".format(path))

    def get_repos(self):
        repos = list()
        for repo in self._g.get_user().get_repos():
            if repo.owner.login in self._orgs:
                if (repo.full_name not in self._exclude):
                    repos.append(repo)
                else:
                    print('Excluding:', repo.full_name)
        return repos

    def upload_templates(self, repository):
        for filename in self._files:
            fileobject = open('templates/' + filename, "r")
            self.commit_file(repository, "/" + filename, fileobject.read())

