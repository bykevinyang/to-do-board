from ticktick.oauth2 import OAuth2        # OAuth2 Manager
from ticktick.api import TickTickClient   # Main Interface
import pprint                             # Pretty Print
from datetime import date
from datetime import datetime

from support import readSecrets

time = datetime.today()

pp = pprint.PrettyPrinter(indent=4)

client_id, client_secret, username, password = readSecrets()
uri = 'https://ticktick.com/oauth/token'

auth_client = OAuth2(client_id=client_id,
                     client_secret=client_secret,
                     redirect_uri=uri)

client = TickTickClient(username, password, auth_client)
state = client.state
# State contains:
    # 'projects': list of projects
    # 'project_folders': list of project folders
    # 'tags': list of tags
    # 'tasks': list of tasks
    # 'user_settings': list of user settings
    # 'profile': list of profile

raw_tasks = state['tasks']

def stripTime(time):
    return datetime.strptime(time[:-8], '%Y-%m-%dT%H:%M:%S.')

def grabTasks(raw_tasks):    
    tasks = {}
    dueToday = []
    
    for task in raw_tasks:
        title = task.get('title')
        dueDate = task.get('dueDate')
        priority = task.get('priority')
        sortOrder = task.get('sortOrder') 
        desc = task.get('desc')

        if dueDate != None:
            dueDate = stripTime(dueDate)
            if dueDate < time:
                dueToday.append(task)

        tasks[task['title']] = task

    sortedToday = sorted(dueToday, key=lambda k: (k['priority'], k['sortOrder']))

    sortedByPri = sorted(sortedToday, key=lambda k: (k['priority'], k['sortOrder']), reverse=True)
    
    return sortedByPri, sortedToday, dueToday, tasks

sortedByPri, sortedTasks, _, _ = grabTasks(raw_tasks)

for task in sortedByPri:
    print(task['title'])
    
# Things to care about: sortOrder, dueDate, priority, title, desc, content

# Tasks is stored in state['tasks'] 
    # Before usersettings