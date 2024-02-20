import vk_api
import json

from config import token

vk_session = vk_api.VkApi(token=token)
KEY_WORDS = {"Собственник",
             "Сдам квартиру",
             "Аренда",
             # "собственник",
             # "cдам квартиру",
             # "aренда"
             }
vk = vk_session.get_api()

lst = {}
for q in KEY_WORDS:
    response = vk.newsfeed.search(q=q, count=10)
    for item in response['items']:
        lst.append(item['text'])

with open('data.json', 'w') as file:
    json.dump(lst, file, ensure_ascii=False)
