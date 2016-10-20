from __future__ import print_function

from slackbot.bot import listen_to
from slackbot import settings


@listen_to('(\S+\-\d+)')
def response_issue(message, issue_id=None):
    print("Handling %s" % issue_id)

    project = issue_id.split('-')[0]
    print("Detected project: %s" % project)
    if "/" in project:
        project = project.split("/")[-1]
        issue_id = project + "-" + issue_id.split('-')[-1]
    if project.upper() not in settings.ALLOWED_PROJECTS:
        print("Unknown project %s" % project)
        return

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
