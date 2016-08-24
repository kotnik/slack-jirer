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

    issue = settings.jira_class.get_ticket(issue_id)
    if not issue:
        print("Issue %s not found" % issue_id)
        return

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
