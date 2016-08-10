# Slack Jirer

This is a simple Slack bot that listens for issues being mentioned in the channel and provides link to them along with additional information.

## Quick start

Set up virtual environment and install it:

```
virtualenv -p python2 slack-jirer
source slack-jirer/bin/activate
pip install slack_jirer
```

Provide configuration with environment variables and run the bot:

```
export SLACKBOT_API_TOKEN=FROM_BOT_CONFIG_IN_SLACK
export SLACKBOT_JIRA_SERVER='https://XXX.atlassian.net'
export SLACKBOT_JIRA_USERNAME='user'
export SLACKBOT_JIRA_PASSWORD='pass'
export SLACKBOT_JIRA_PROJECTS='OP,CODE'

slack_jirer
```
