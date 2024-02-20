import vk_api
import json

from config import token

import functools
import time

KEY_WORDS = {
        "Сдам квартиру",
        # "Аренда"
    }
def cache_with_timeout(func):
    cache = {}
    last_called = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        userid = "0"
        current_time = time.time()

        if userid in last_called and current_time - last_called[userid] < 7200 and cache.get(userid) is not None:
            return cache[userid]
        else:
            result = func(*args, **kwargs)
            cache[userid] = result
            last_called[userid] = current_time
            return result

    return wrapper


@cache_with_timeout
# def get_rent_news1():
#     vk_session = vk_api.VkApi(token=token)
#     KEY_WORDS = {
#         # "Собственник",
#         "Сдам квартиру",
#         "Аренда",
#     }
#     vk = vk_session.get_api()
#
#     lst = []
#     for q in KEY_WORDS:
#         response = vk.newsfeed.search(q=q, count=10)
#         print(response)
#         with open('data/data1.json', 'w') as file:
#             json.dump(list(response["next_from"]), file, ensure_ascii=False)
#         # with open('data/data2.json', 'w') as file:
#         #     json.dump(list(response["total_count"]), file, ensure_ascii=False)
#         with open('data/data3.json', 'w') as file:
#             json.dump(list(response["count"]), file, ensure_ascii=False)
#         with open('data/data4.json', 'w') as file:
#             json.dump(list(response["items"]), file, ensure_ascii=False)
#         for item in response['items']:
#             lst.append(item['text'])
#
#     with open('data/data.json', 'w') as file:
#         json.dump(lst, file, ensure_ascii=False)
#     return 1

# @cache_with_timeout
def get_rent_news():
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    lst = []
    for q in KEY_WORDS:
        response = vk.newsfeed.search(q=q, count=10, extended=1, latitude=55.3, longitude=37.5, radius=5000,
                                      filters='post',
                                      author_only=1
                                      )
        for item in response['items']:
            # if item['from_id'] > 0:
            lst.append([item.get('text'), "https://vk.com/id" + str(item['from_id'])[1:]])
            print(item['from_id'])
        print(q)
    with open('data/data.json', 'w') as file:
        json.dump(lst, file, ensure_ascii=False)
    print(1234)
    return 1


if __name__ == "__main__":
    get_rent_news()
    pass
