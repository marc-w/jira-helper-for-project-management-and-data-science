"""Configuration dataclass"""
from dataclasses import dataclass
import logging
from os import environ
import sys

# Allows turning on debug from env
_DEBUG = environ.get('DEBUG')

# set up logging
logging.basicConfig()
_log = logging.getLogger("jira-help")

if _DEBUG:
    _log.setLevel(logging.DEBUG)
else:
    _log.setLevel(logging.ERROR)


@dataclass
class Konfig:
    """
    Handles all of the config, hydration, and validation
    of credentials and set up
    """
    # Jira
    JIRA_SERVER = environ.get('JIRA_SERVER')
    JIRA_EMAIL = environ.get('JIRA_EMAIL')
    JIRA_API_TOKEN = environ.get('JIRA_API_TOKEN')
    JIRA_PROJECT_ID = environ.get('JIRA_PROJECT_ID')

    # Optional Slack webhook
    SLACK_WEBHOOK_URL = environ.get('SLACK_WEBHOOK_URL')

    logger = _log

    def __init__(self) -> None:
        """
        Initialization also performs basic checks
        """
        self.check()

    def check(self) -> None:
        """
        Required check for set up with reporting

        """
        # dropping log level for set up for visibility
        _critical_errors = []  # collect errors (will exit set up)
        _warnings = []  # Collect warning (will not exit set up)
        _break = False  # when set to True will exit setup with logs

        # Checks
        if not self.JIRA_SERVER:
            _critical_errors.append('JIRA_SERVER not set')
        if not self.JIRA_EMAIL:
            _critical_errors.append('JIRA_EMAIL not set')
        if not self.JIRA_SERVER:
            _critical_errors.append('JIRA_SERVER not set')

        if not self.SLACK_WEBHOOK_URL:
            _warnings.append('SLACK_WEBHOOK_URL not set')

        # Final reporting
        if _critical_errors:
            _break = True
            self.logger.error('\nCRITICAL errors, please fix')
            for e in _critical_errors:
                self.logger.error(e)
        if _warnings:
            self.logger.error('\n Warnings found:')
            for e in _warnings:
                self.logger.error(e)

        self.logger.error('Configuration check complete.')

        if _break:
            sys.exit("Graceful exit, see logs for errors found.")

        return True


lazy_config = Konfig()
