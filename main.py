import functools
import time

import vk_api
import json

from config import token

import functools
import time


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
def get_rent_news():
    vk_session = vk_api.VkApi(token=token)
    KEY_WORDS = {"Собственник",
                 "Сдам квартиру",
                 "Аренда",
                 # "собственник",
                 # "cдам квартиру",
                 # "aренда"
                 }
    vk = vk_session.get_api()

    lst = []
    for q in KEY_WORDS:
        response = vk.newsfeed.search(q=q, count=10)
        for item in response['items']:
            lst.append(item['text'])

    with open('data/data.json', 'w') as file:
        json.dump(lst, file, ensure_ascii=False)
    return 1


if __name__ == "__main__":
    get_rent_news()
    get_rent_news()
