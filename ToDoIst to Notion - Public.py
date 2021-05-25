import todoist

##### ALL OF THE VALUES YOU PASTE HERE SHOULD BE IN STRINGS
TODOIST_API_KEY =  #copy and paste the api key 
NOTION_API_KEY =     #  "secret_somneklhjslkdgjsdljfg" or something like that 
database_id =  #get the mess of numbers before the "?" on your dashboard URL and then split it into 8-4-4-4-12 characters between each dash

api = todoist.TodoistAPI(TODOIST_API_KEY)
api.sync()

import requests
resultList=requests.get(
    "https://api.todoist.com/rest/v1/tasks",
    params={
        "label_id": 2157047813
    },
    headers={
        "Authorization": "Bearer %s" % TODOIST_API_KEY
    }).json()


taskData = []

import os
from notion_client import Client
from pprint import pprint
from datetime import datetime

os.environ['NOTION_TOKEN'] = NOTION_API_KEY
notion = Client(auth=os.environ["NOTION_TOKEN"])

for result in resultList:
    print(result)
    print("\n")

    taskName = result['content']
    dueDate = result['due']['date']

    #Enter the task into Notion
    my_page = notion.pages.create(
        **{
            "parent": {
                "database_id": database_id
            },
            "properties": {
                'Task': {
                    "type": 'title',
                    "title": [
                    {
                        "type": 'text',
                        "text": {
                        "content": taskName,
                        },
                    },
                    ],
                },
                'Date': {
                    "type": 'date',
                    'date': {
                        'start': dueDate, 
                        'end': None,
                    }
                },
                'Dashboard':  {
                    "type": 'multi_select', 
                    'multi_select': [{
                        "name": "ToDoIst"
                    }],
                },
            },
        },
    )

    #Delete the task from ToDoIst (the api stuff is defined in the first 3 lines of the program)

    item = api.items.get_by_id(result['id'])
    item.delete()
    api.commit()

    
