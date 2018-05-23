# github-bulkeditor

This project is used to apply bulk updates to github and github enterprise repositories. It
can turn off unused github features such as issues, projects, etc. in case your org is using 
other tools for issue tracking. It enables branch protection for the master branch and configures
minimum approvals required for merges.  It limits allowed pull request merge types to
squash merges. It also commits template files to each repository.

## Getting Started

### Prerequisites

This project requires python 3.6 or higher. It may work with lower
versions of python 3 but that has not been tested.

Before installing, please create a virtual env so as to not introduce
package dependency problems with your OS env.

```
$ pip3 install virtualenv
$ cd github-templates    # or whatever you named your project folder
$ virtualenv venv
$ source venv/bin/activate
```


### Installing

Pip install the dependencies.

This project needs pyGitHub. At the time of writing this, the public
pyGithub did not include support for merge types so I created a fork
support for the merge attributes while we wait for the upstream project
to approve the pull requests.

When the following PR's are merged, the requirements.txt can be updated
point to the upstream pyGithub project.
https://github.com/PyGithub/PyGithub/pull/785
https://github.com/PyGithub/PyGithub/pull/784

```
$ pip3 install -r requirements.txt
```

You will need a github personal access token with 'Repo' access to use
this utility. After creating your personal access token, export it to
make it available for the script to use.

```
$ export GITHUB_BULKEDITOR_AUTHTOKEN=<your key goes here>
```

Open the config.py file and configure the variables as needed.

* _baseURL_ - The api url of your github installation. If set to _None_
it will default to public github.
```
baseURL = 'https://github.yourorg.com/api/v3'
```

* _orgs_ - a list of github orgs that will receive changes
```
orgs = ['org1', 'org2', 'org3']
```

* _exclude_ - a list of repositories to exclude
```
exclude = [
    'org2/repo-name'
]
```

* _files_ - the list of files in the _templates_ project directory to
publish to the remote repos. Files will only be committed if there is
no existing file with the same name.  The script will not overwrite
files.
```
files = [
    'CODEOWNERS',
    'CONTRIBUTING.md',
    '.github/PULL_REQUEST_TEMPLATE.md'
]
```

* _testMode_ - execute against a single repo only
```
testMode = True
```

* _testRepoName_ - the name of the single repo to use in testMode
```
testRepoName = 'org1/test-repo'
```

## Running the script (main.py)
Be sure to setup the appropriate variables in config.py before running.

```
$ python3 main.py
```

## Viewing Non-Private Repos
Be sure to setup the appropriate variables in config.py before running.

```
$ python3 nonprivate.py
```

## Authors

* **Asa Gage** - *Initial work*
