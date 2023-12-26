"""Setup and discovery for Jira"""
import sys
from jira.client import JIRA

from lib import config
from lib.jira import JiraHelper

jh = JiraHelper()


class Setup:
    """
    Setup and discovery of Jira credentials and assets
    """

    def __init__(self):
        # get handle automatically
        self.jira = JIRA(
            server=config.JIRA_SERVER,
            basic_auth=(config.JIRA_EMAIL, config.JIRA_API_TOKEN),
        )

    def setup(self) -> None:
        """
        Set up and discovery script for the command line.
        :return: None
        """
        if config.JIRA_PROJECT_ID:
            config.logger.info(
                "JIRA_PROJECT_ID set to %s", config.JIRA_PROJECT_ID
            )
            config.logger.info("Setup will not run.")
            return

        config.logger.error("SWITCHING TO STD OUT FROM LOGGER FOR SET UP")

        # set up
        input("Press [enter] to continue...")

        # Check for projects
        projects = self.get_all_projects()

        keys = self.map_projects(projects)

        # Cast selection
        project_key = self.get_selected_project(keys)

        print(f'\nProject slug selected: {project_key}')

        # With the project key selected search for issues
        q = f'project={project_key}'

        issues = self.jira.search_issues(q)
        if not issues:
            print(f'No issues found for {q}. Set up exiting.')
            sys.exit()

        self.get_transitions_for_project(issues)

        # EOL
        print('\nSet up discovery complete.')

    def get_all_projects(self):
        """
        Get all of the projects visible to the user
        associated with the API token

        :return _type_: list

        ex. [<JIRA Project: key='MP', name='Main Project', id='10001'>, ...]
        """
        # Check for projects
        print('\nLooking for projects associated with the API key')
        projects = self.jira.projects()
        if not projects:
            _msg = 'No projects found. Exiting.'
            print(_msg)
            sys.exit(_msg)

        print("* " * 20)
        print(f'{len(projects)} projects(s) found.\n')

        return projects

    def map_projects(self, projects):
        """
        _summary_

        :param _type_ projects: _description_
        :return dict: keys and other data, see example:
        {'MP': {'name': 'Main Project', 'id': '10001'}, ...]
        """
        keys = {}
        for i in projects:
            keys[i.key] = {
                "name": i.name,
                "id": i.id,
            }
        return keys

    def get_transitions_for_project(self, issues):
        """
        _summary_

        :param list issues: jira.client.ResultList
        """
        # take the first issue, arbitrarily.
        # Also allows testing when one issue is being pushed.
        issue = issues[0]

        transitions = jh.get_transitions(issue)

        # Print out the transitions and IDs for the config mapping necessary
        print(
            '\nThe transitions were found using issue {issues[0].key}\n')
        print('The following list is the transition ID and string name '
              'for transitions discovered.\n')
        print('Map either the string value (can change in Jira) or use the '
              'ID (number, that should not change) to map Jira labels '
              'to a triggered transition.')
        print("* " * 20)
        print(" ")

        for k, v in transitions.items():
            print(f"ID: {k} -- string name: {v}")

    def get_selected_project(self, keys):
        """
        Provide user with options and selection for the project to use
        :param dict keys: return via self.map_projects()

        :return str: selected project slug
        """
        while True:
            _recall = {}  # holds valid options for selection
            _selections = []

            cnt = 1
            for k, v in keys.items():
                _recall[cnt] = k
                _selections.append(cnt)  # note offset for human readability
                print(
                    f'{cnt}:  slug: {k} | name: {v.get("name", "missing")} | '
                    f'id: {v.get("id", "missing")} '
                )
                cnt += 1

            selected_project = str(input(
                f'\nTo continue select a project key'
                f' (choices {",".join(str(i) for i in _selections)}): '))

            try:  # cast/validate
                selected_project = int(selected_project)
            except ValueError:
                selected_project = -1  # Note: too low because enumerate
            if selected_project in _recall:  # valid selection
                break
            else:
                print('Invalid selection.')

        return _recall.get(selected_project)
