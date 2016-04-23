# -*- coding: UTF-8 -*-
__author__ = 'li'

import time, os, sched, hot_post_redis
from datetime import datetime
from read_config import config
# 任务执行周期k + '_hot_post'
taskCycle = int(config.get('timertask', 'task_cycle'))

schedule = sched.scheduler(time.time, time.sleep)
# 查询帖子S
queryPostSql = "SELECT * FROM post where post.postTime > DATE_SUB(now(),INTERVAL 7 DAY) and post.status!=0"
# 查询城市帖子
queryCitySql = "SELECT * FROM citypost where citypost.postTime > DATE_SUB(now(),INTERVAL 7 DAY)  and citypost.status!=0"


def perform_command(inc):
    # 安排inc秒后再次运行自己，即周期运行
    startTime=datetime.now()
    hot_post_redis.write_on_redis(queryPostSql, 1)
    hot_post_redis.write_on_redis(queryCitySql, 2)
    endTime=datetime.now()
    print(endTime-startTime)
    schedule.enter(inc, 0, perform_command, (inc,))


def timming_exe(inc=60):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动
    schedule.enter(inc, 0, perform_command, (inc,))
    schedule.run()


print("start:")
timming_exe(taskCycle)