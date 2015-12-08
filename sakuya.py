
import argparse
import yaml
import json
import time
import datetime
import re
import multiprocessing
import threading
from requests.exceptions import ConnectionError, ReadTimeout, SSLError


import oauth2 as oauth
import urllib
from requests_oauthlib import OAuth1Session
from http.client import IncompleteRead

import six.moves.cPickle as pickle
from six.moves import queue

import subprocess


with open('keys_sakuya.yml', 'r') as f:
    keys_sakuya = yaml.load(f)

with open('config.yml', 'r') as f:
    config = yaml.load(f)

# 自分のアカウントのID
allowed_screen_name = config['allowed_screen_name']
my_id = config['my_id']


twitter_api = OAuth1Session(
    keys_sakuya['CONSUMER_KEY'],
    client_secret=keys_sakuya['CONSUMER_SECRET'],
    resource_owner_key=keys_sakuya['ACCESS_TOKEN'],
    resource_owner_secret=keys_sakuya['ACCESS_SECRET']
)


# エアコンの電源をON
def aircon_on():
    cmd = "irsend SEND_ONCE aircon power_on"
    subprocess.call(cmd, shell=True)



schedule = []

tasks_q = queue.Queue()

def tweet(text, reply_data=None):
    global twitter_api

    params = {}

    if reply_data:
        params['in_reply_to_status_id'] = reply_data['id']
        text = '@{} '.format(reply_data['user']['screen_name']) + text

    params['status'] = text

    url = "https://api.twitter.com/1.1/statuses/update.json"
    res = twitter_api.post(url, params=params)

    return res.status_code

def manage_schedule():
    global schedule, tasks_q

    while(True):
        if len(schedule) != 0:
            if datetime.datetime.now() > schedule[0]['datetime']:
                tasks_q.put(schedule[0]['task'])

        time.sleep(1)


def do_tasks():
    global tasks_q

    task = tasks_q.get()

    if task == 'aircon_on':
        aircon_on()
        print("エアコンが付く")
        tweet('エアコンを付けました')

r_backhome = re.compile(r'([0-9０-９]{1,2})(時|じ).*(かえ|帰)')
r_call = re.compile(r'(咲|さく|サク)(夜|や|ヤ)')

# 咲夜さんを呼んだか判定
def is_call(data):

    # 咲夜さんの名前を含むか？
    f1 = r_call.search(data['text'])

    # 自分のアカウントのツイートか？
    f2 = data['user']['screen_name'] in allowed_screen_name

    return f1 and f2


# sakuyaへのメッセージか判定
def is_massage(data):

    # 自分へのリプライか？
    f1 = data['in_reply_to_user_id'] == my_id

    # 自分のアカウントからのリプライか？
    f2 = data['user']['screen_name'] in allowed_screen_name

    return f1 and f2




# メッセージを解釈して実行(queueに入れる)
def do_massage(data):
    global schedule

    filtered_text = re.sub(r'@[a-zA-Z0-9_]{1,15}\s', '', data['text'])

    match = r_backhome.search(filtered_text)

    if not match:
        return

    backhome_hour = int(match.group(1))
    backhome_time = datetime.datetime.today().replace(hour=backhome_hour, minute=0, second=0, microsecond=0)

    if backhome_time < datetime.datetime.now():
        backhome_time += datetime.timedelta(days=1)

    aircon_on_time = backhome_time - datetime.timedelta(minutes=30)

    schedule.append({'datetime': aircon_on_time, 'task':'aircon_on'})
    schedule = sorted(schedule, key=lambda x:x['datetime'])

    print("{}時{}分にエアコン付けます".format(aircon_on_time.hour, aircon_on_time.minute))
    reply_status = {'tweet_id': data['id'], 'screen_name': data['user']['screen_name']}
    text = 'わかりました．{}時{}分にエアコンを付けますので，気をつけてお帰りください．'.format(aircon_on_time.hour, aircon_on_time.minute)
    res = tweet(text=text, reply_data=data)



def feed_tweet():
    global tasks_q, twitter_api

    url = 'https://userstream.twitter.com/1.1/user.json'

    params = {}

    res = twitter_api.get(url, params=params, stream=True)


    try:
        for r in res.iter_lines():
            if not r:
                continue
            data = json.loads(r.decode())
            print(data)
            if 'delete' in data.keys() or 'lang' not in data:
                pass
            elif 'in_reply_to_user_id' in data.keys() and 'text' in data.keys():

                if is_massage(data):
                    do_massage(data)

                elif is_call(data):
                    tweet('どうしましたか', reply_data=data)



    except Exception as e:
        print( '=== エラー内容 ===')
        print( 'type:' + str(type(e)))
        print( 'args:' + str(e.args))
        print( 'message:' + str(e.message))
        print( 'e self:' + str(e))

    except:
        print( "error.")



if __name__ == '__main__':
    tasker = threading.Thread(target=do_tasks)
    scheduler = threading.Thread(target=manage_schedule)
    tasker.daemon = True
    scheduler.daemon = True
    tasker.start()
    scheduler.start()

    feed_tweet()

    tasker.join()
    scheduler.join()

    print('finish!')
