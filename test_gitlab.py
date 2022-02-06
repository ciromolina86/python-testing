import requests
import json

global item_counter, total_seconds
item_counter = total_seconds = 0

def get_total_hours(project, issue):
    global item_counter, total_seconds

    print(f'\nProject name: {project["name"]}')
    # print(f'\tId: {project["id"]}')
    print(f'\tNamespace: {project["namespace"]["name"]}')

    print(f'\t\tIssue milestone: {issue["milestone"]["title"]}')
    print(f'\t\tIssue title: {issue["title"]}')
    print(f'\t\tTime spent: {issue["time_stats"]["human_total_time_spent"]}')
    print()

    total_seconds += int(issue['time_stats']['total_time_spent'])
    item_counter += 1

def main():
    API_KEY = "FZBCZezRsgKoPkAg4HjA"
    BASE_URL = "https://gitlab.desa.sorbapp.com/api/v4/projects/"
    HEADER = {'PRIVATE-TOKEN': API_KEY}
    milestone = 'june-sprint1-dev-team1'
    username = 'emolina'

    # for i in range(116, 200):  # manually set range of issues here. All issues doesn't work well.
    projects = requests.get(BASE_URL, headers=HEADER).json()
    # print(projects)
    # print(f'Number of projects: {len(projects)}')

    for project in projects:

        issues = requests.get(f'{BASE_URL}{project["id"]}/issues/', headers=HEADER).json()
        # print(f'\tNumber of issues: {len(issues)}')

        for issue in issues:
            if (
                    issue['milestone'] is not None
                    and issue['milestone']['title'] == milestone
                    and issue['assignee'] is not None
                    and issue['assignees'] is not None
            ):
                if issue['assignee']['username'] == username:
                    get_total_hours(project, issue)
                    for assignee in issue['assignees']:
                        if assignee['username'] == username:
                            get_total_hours(project, issue)

    print("Hours on all issues: %.2f" % float((total_seconds / 60) / 60))
    print("Total issues: " + str(item_counter))


if __name__ == '__main__':
    main()
