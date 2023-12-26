"""Jira functions and main class"""
from jira.client import JIRA as _JIRA
from jira.resources import Issue
from jira import exceptions as jira_exceptions

from lib import (config, nothing)


class JiraHelper:
    """
    Main Jira helper and methods

    :param _type_ config: _description_
    """
    _jira = None  # hold Jira object

    def __init__(self):
        """
        POE + setup
        """
        self.project_slug = self.get_project_slug()

    def get_project_slug(self):
        """
        Gets the project slug.

        :return _type_: str
        """
        return self.jira.project(config.JIRA_PROJECT_ID)

    @property
    def jira(self):
        """
        Property to return handle, getting a new one as needed.

        :return _type_: <class 'jira.client.JIRA'>
        """
        if not self._jira:
            self.get_handle()
        return self._jira

    def get_handle(self):
        """
        Get a handle to Jira
        """
        self._jira = _JIRA(
            server=config.JIRA_SERVER,
            basic_auth=(
                config.JIRA_EMAIL,
                config.JIRA_API_TOKEN
            ),
        )

    def get_issue_by_slug(self, slug, **kwargs):
        """
        Get issue object using the slug, eg. XY-101
        :param slug: string ex. XX-1234
        :param kwargs: dict
            verbose: bool
        :return: resource object for issue, else None
        """
        ret = self.execute_jql(
            jql=f"project={self.project_slug} and issue = {slug}",
            **kwargs
        )

        if not ret or len(ret) != 1:
            config.logger.error(
                "When searching for slug %s using project %s an "
                "error was encountered",
                self.project_slug, slug
            )
            return None
        return ret[0]

    def execute_jql(self, jql=None, **kwargs):
        """
        Execute arbitrary JQL
        :param jql:
        :param kwargs: dict
            verbose: bool
        :return: list, empty or with query objects representing result set
        """
        if not jql:
            raise RuntimeError("no JQL provided. [5ygafs]")

        try:
            jql_result = self.jira.search_issues(jql)
        except jira_exceptions.JIRAError as e:
            if kwargs.get('verbose', True):

                _msg = ('\nDo not worry\nERROR was thrown, '
                        'Jira exception, here is the message:\n'
                        f'{e}\n')
                config.logger.error(_msg)
            jql_result = None
        return jql_result

    def get_transitions(self, issue=None):
        """
        Return a dict of transitions. Default operation (no issue provided) is
        to find the first active issue in the default project.

        :param str issue: Optional issue, will be used instead of
            default issue operation, defaults to None
        :return: dict {"transition_id": "name"}
        """
        # take the first issue, arbitrarily.
        # Also allows testing when one issue is being pushed.
        if issue is None:
            # no limit clause in JQL
            issues = self.execute_jql(
                f"project={self.project_slug} order BY created DESC"
            )
            if not issues:
                config.logger.error(
                    "No issues returned for project slug %s",
                    self.project_slug
                )
                return None
            issue = issues[0]

        if not isinstance(issue, Issue):
            config.logger.error(
                "Expected an issue, instead received: %s", issue
            )
            return None

        _transitions = self.jira.transitions(issue)
        transitions = {}
        for transition in _transitions:
            transitions[transition['id']] = transition['name']

        return transitions

    @staticmethod
    def r_get(_dict, _path):
        """
        "Recursive" get to use a path defined by a list for performing
        a deep get() on nested dictionary data.

        :param dict _dict: dictionary to parse
        :param dict _path: _description_
        :return str: data, if available, via the path provided

        Note: API's can return a valid "None" for unset values.  The `nothing`
        object is used when a path fails and will return "-MISSING-" string.
        """

        _temp = None
        if not isinstance(_dict, dict):
            config.logger.error(
                "r_get(): r_get() expects a dictionary, not %s", type(_dict)
            )
            return None
        for p in _path:
            if not _temp:
                _temp = _dict.get(p, nothing)
            else:
                _temp = _temp.get(p, nothing)
            if _temp is nothing:
                config.logger.error(
                    "The path %s using key: %s returned None.", _path, p
                )
                _temp = "-MISSING-"
                return _temp
        return _temp
