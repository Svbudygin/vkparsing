import vk_api
import json

from config import token

import functools
import time

KEY_WORDS = {
    "Сдам квартиру",
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


# @cache_with_timeout
def get_rent_news():
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    lst = []
    for q in KEY_WORDS:
        response = vk.newsfeed.search(q=q, count=200,
                                      # extended=1,
                                      # latitude=55.3, longitude=37.5,
                                      # radius=50,
                                      # filters='post',
                                      # author_only=1
                                      )
        with open('data/response.json', 'w') as file:
            json.dump(response, file, ensure_ascii=False)
        for item in response['items']:
            if item['from_id'] > 0:
                user_info = vk.users.get(user_ids=item['from_id'])
                print(user_info, item['from_id'], item['owner_id'])
                lst.append([item.get('text'), "https://vk.com/id" + str(item['owner_id'])])
            else:
                print("опять группа")
    with open('data/data.json', 'w') as file:
        json.dump(lst, file, ensure_ascii=False)
    return 1


if __name__ == "__main__":
    get_rent_news()
    pass
