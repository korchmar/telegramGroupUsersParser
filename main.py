import telethon
from telethon.tl import functions, types
from telethon.sync import TelegramClient
import argparse
import re
import sys
import asyncio
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerUser
import csv

def readEnvVars():
    # read environment variables
    with open('.env', 'r') as f:
        for line in f:
            key, val = line.strip().split('=')
            globals()[key] = val

async def main():
    print("started")
    readEnvVars()
    # login and start
    try:
        client = telethon.TelegramClient(SESSION_NAME, APP_API_ID, APP_API_HASH)
        await client.start()
    except Exception as e:
        print('Error while authenticating the user:\n\t%s' % e)
        sys.exit()

    channel_username = CHANNEL_NAME  # your channel
    messages = client.iter_messages(channel_username, wait_time=1, limit=None)

    user_ids = []
    with open(channel_username + '_group.csv', 'w', newline='') as csvfile:
        fieldnames = ['user_id', 'user_nickname', 'user_firstname']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        async for message in messages:
           try:
             user = await client.get_entity(PeerUser(int(re.findall("\d+", str(message.from_id))[0])))
           except:
               print("user id not found")
           if not user.id in user_ids:
             user_ids.append(user.id)
             if not user.bot:
              writer.writerow({'user_id': str(user.id), 'user_nickname': user.username, 'user_firstname': user.first_name})
              try:
               print(str(user.id) + " " + user.username + " " + user.first_name + " " + str(user.bot))
              except:
                  print("string conversion error")
    print("-------------------------------------")

if __name__ == '__main__':
    asyncio.run(main())
