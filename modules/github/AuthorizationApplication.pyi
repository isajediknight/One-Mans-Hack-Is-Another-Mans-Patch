from typing import Dict

from github.GithubObject import CompletableGithubObject

class AuthorizationApplication(CompletableGithubObject):
    def _initAttributes(self) -> None: ...
    def _useAttributes(self, attributes: Dict[str, str]) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def url(self) -> str: ...
