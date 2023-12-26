# Jira Helper

Python application for exploring, extending, and automating Jira programmatically.

Three main use case:

1. Explore Jira data and the API programmatically to gain insight and details often missing or difficult to know using the Jira UI
1. Query, graph, and manipulate data in a data-science (jupyter) environment
1. Run this application as needed or persistently to CRUD data or notify user(s) of events, conditions, and changes in an exact manner.

## Local Environment

`PIPENV` is used with a `requirements.txt` file included.

Setting up the `local.sh` file by removing `.example` from `local.sh.example`. Populate `JIRA_API_TOKEN`, `JIRA_EMAIL`, and `JIRA_SERVER`.

Environment variables are required and made available in the shell.  Use the `local.sh` file to hydrate your session such as:

```
. ./local.sh
```

With success a message is displayed in the shell session.

## Requirements

* Minimum Python:  3.10.x or greater 
* PIPENV: v2023.4.29 or greater

### Slack Integration

Included is a siple Slack function for delivering information via a webhook to your Slack workspace.  Configure the webhook in the `local.sh` file.

## Technical Notes

### Using `config`

To use the configuration object, import from the `lib' module as such:

```
from lib import config
```

The class `Konfig` located in `lib/configuration` can be extended as needed to for non-environment variable use.  Note the use of `lazy-config`.


## Using Jupyter

To start Jupyter, use the following command:

```
jupyter notebook
```


## Dependencies

* Flake8: Final linting.

```
flake8 lib main.py
```
