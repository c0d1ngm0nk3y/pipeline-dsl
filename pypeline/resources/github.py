import os
from pypeline.concourse import concourse_context

class GithubReleaseResource:
    def __init__(self, name):
        self.name = name
        self.path = os.path.abspath(self.name)

    def __str__(self):
        return self.name

    def tag(self, default=None):
        if concourse_context():
            with open(os.path.join(self.path, "tag")) as f:
                return f.read().strip()
        return default


class GithubRelease:
    def __init__(self, owner, repo, access_token=None, pre_release=False, release=True, github_api_url=None, github_uploads_url=None):
        self.owner = owner
        self.repo = repo
        self.access_token = access_token
        self.pre_release = pre_release
        self.release = release
        self.github_api_url = github_api_url
        self.github_uploads_url = github_uploads_url

    def resource_type(self):
        return None

    def concourse(self, name):
        result = {
            "name": name,
            "type": "github-release",
            "icon": "github",
            "source": {
                "owner": self.owner,
                "repository": self.repo,
                "access_token": self.access_token,
                "pre_release": self.pre_release,
                "release": self.release,
            }
        }
        if self.github_api_url != None:
            result["source"]["github_api_url"] = self.github_api_url
        if self.github_uploads_url != None:
            result["source"]["github_uploads_url"] = self.github_uploads_url
        return result

    def get(self, name):
        return GithubReleaseResource(name)