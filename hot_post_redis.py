# -*- coding: UTF-8 -*-
__author__ = 'li'

import rank_algorithm, db, redis, quick_max_k, json, time
from read_config import config
# querysql = 'select * from post where post.postTime>now()-00000002000000  and post.status!=0 '

MAX_K = 10

# add som comment
def convert_to_json(mypost):
    post = {'postId': mypost[0],
            'accountId': mypost[1],
            'content': mypost[2],
            'downCount': mypost[3],
            'flowerName': mypost[4],
            'nickName': mypost[5],
            'position': mypost[6],
            'postTime': rank_algorithm.epoch_seconds(mypost[7]) * 1000 - 28800000,
            'postType': mypost[8],
            'reCount': mypost[9],
            'relation': mypost[10],
            'schoolNo': mypost[11],
            'status': mypost[12],
            'upCount': mypost[13],
            'url': mypost[14]
    }
    return post
    # return json.dumps(post)


def write_on_redis(querysql, type):
    try:
        redisConnection = redis.ConnectionPool(host=config.get('redis', 'redis_ip'),
                                               port=int(config.get('redis', 'redis_port')),
                                               db=int(config.get('redis', 'redis_db')))
        redisContext = redis.Redis(connection_pool=redisConnection)

        minHotMark = rank_algorithm.standard_mark()
        print ("最小的值为:"+str(minHotMark))

        dataset = db.get_data(querysql, type)

        for k, v in dataset.items():
            hotPost = []

            if len(v) > 10:
                score = {}

                for post in v:
                    # print(rank_algorithm.hot(post[13], post[3], post[9], post[7]))
                    scoreNum = rank_algorithm.hot(post[13], post[3], post[9], post[7])
                    if scoreNum >= minHotMark:
                        if scoreNum not in score:
                            score[scoreNum] = []
                            score[scoreNum].append(post)
                        else:
                            score[scoreNum].append(post)
                d = []
                for key in score.keys():
                    d.append(key)

                count = 0
                sortdata = quick_max_k.qselect(d, MAX_K)
                for sortk in sortdata[::-1]:
                    for p in score[sortk][::-1]:
                        if (count >= 10):
                            break

                        hotPost.append(convert_to_json(p))

                        count = count + 1
                print(k + '_hot_post'+json.dumps(hotPost, separators=(',', ':')))

                redisContext.set(k + '_hot_post', json.dumps(hotPost, separators=(',', ':')))


    except redis.ConnectionError as err:
        print("connect redis' failed.")
        print("Error: {}".format(err.msg))
















