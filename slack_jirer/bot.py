from __future__ import print_function

import re

from slackbot.bot import listen_to
from slackbot import settings


@listen_to('(\S+\-\d+)')
def response_issue(message, issue_string=None):
    print("Handling %s" % issue_string)

    project = issue_string.split('-')[0]
    issue_id = issue_string.split('-')[1]
    if "/" in project:
        project = project.split("/")[-1]
    try:
        issue_id = project + "-" + re.search(r'\d+', issue_id).group()
    except AttributeError:
        print("Unknown issue in %s" % issue_id)
        return
    print("Detected project: %s" % project)
    if project.upper() not in settings.ALLOWED_PROJECTS:
        print("Unknown project %s" % project)
        return
    print("Searching for: %s" % issue_id)
    try:
        issue = settings.CACHE[issue_id]
        print("Used cached version of %s" % issue_id)
    except KeyError:
        issue = settings.jira_class.get_ticket(issue_id)
        if not issue:
            print("Issue %s not found, Jira says" % issue_id)
            return
        settings.CACHE[issue_id] = issue
        print("Fetched %s from Jira" % issue_id)

    msg = "<%s/browse/%s|%s: %s>\n" % (
        settings.JIRA_SERVER,
        issue_id.upper(),
        issue_id.upper(),
        issue.fields.summary
        )
    msg += "*Assignee*: %s\n" % issue.fields.assignee
    msg += "*Created*: %s\n" % issue.fields.created.split('T')[0]
    msg += "*Priority*: %s\n" % issue.fields.priority
    msg += "*Status*: %s" % issue.fields.status

    message.send_webapi(msg)
