import os

import requests
from dotenv import load_dotenv

import nuctpy

load_dotenv(verbose=True)

# secret
api_key = os.environ.get("NOTION_API_KEY")

headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    "Authorization": f"Bearer {api_key}",
}


def create_note_db(page_id):
    url = "https://api.notion.com/v1/databases"
    note_db_template = {
        "parent": {"page_id": page_id},
        "title": [
            {
                "text": {
                    "content": "講義ノート",
                },
            }
        ],
        "properties": {
            "タイトル": {"title": {}},
            "講義名": {
                "select": {},
            },
            "期間": {
                "select": {},
            },
        },
    }
    response = requests.post(url, json=note_db_template, headers=headers)
    return response.json()


def create_course_db(page_id):
    url = "https://api.notion.com/v1/databases"
    course_db_template = {
        "parent": {"page_id": page_id},
        "title": [
            {
                "text": {
                    "content": "講義DB",
                },
            }
        ],
        "properties": {
            "講義名": {"title": {}},
            "時限": {
                "select": {},
            },
            "曜日": {
                "multi_select": {},
            },
            "期間": {
                "select": {},
            },
        },
    }
    response = requests.post(url, json=course_db_template, headers=headers)
    return response.json()


def insert_course_data(database_id):
    ct = nuctpy.NUCT(use_old_cookie=False)
    lectures = nuctpy.get_lectures(ct)
    url = "https://api.notion.com/v1/pages"
    responses = list()

    for lec in lectures:
        hour = "".join([str(a) for a in lec.hour])
        hour = "その他" if len(hour) == 0 else hour
        days = {v: k for k, v in nuctpy.lecture.day_ja2en.items()}
        term = str(lec.year if lec.year != 0 else "") + str(lec.term).replace(
            "SPR", "春"
        ).replace("FALL", "秋").replace("OTHER", "その他")
        payload = {
            "parent": {"database_id": database_id},
            "properties": {
                "講義名": {"title": [{"text": {"content": lec.title}}]},
                "時限": {
                    "select": {"name": hour},
                },
                "曜日": {
                    "multi_select": [{"name": days[d]} for d in lec.day],
                },
                "期間": {
                    "select": {"name": term},
                },
            },
        }
        response = requests.post(url, json=payload, headers=headers)
        responses.append(response.json())
        print(response.json())
    return responses


if __name__ == "__main__":
    root_page_id = "your_root_page_id"  # secret
    create_note_db(root_page_id)
    res = create_course_db(root_page_id)
    database_id = res["id"]
    insert_course_data(database_id)
