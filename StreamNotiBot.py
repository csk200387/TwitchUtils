import asyncio
import aiohttp
import datetime
import json


DISCORD_WEBHOOK_URL = ""
TWITCH_BEARER_TOKEN = ""
TWITCH_CLIENT_ID = ""


names = {
    "ID": "NICKNAME",
}

streamer = names.keys()


async def is_live(name:str, session) :
    url = f"https://api.twitch.tv/helix/streams?user_login={name}"
    async with session.get(url, headers = {
        "Authorization": f"Bearer {TWITCH_BEARER_TOKEN}",
        "Client-ID": TWITCH_CLIENT_ID
        }, raise_for_status=True) as response :
            data = await response.json()
            if data["data"] == [] :
                return False
            else :
                return True


async def send_hook(content:str, session) :
    today = datetime.date.today()
    date = today.strftime("%m월 %d일")

    headers = {"Content-Type" : "application/json"}
    data = {
        "content": f"{date} 뱅온 - {content}",
        "username": "StreamLog",
        "avatar_url": "https://i.pinimg.com/474x/40/e4/86/40e486f34c81555ff1b9012aa8a24866.jpg"
        }
    data = json.dumps(data)
    async with session.post(DISCORD_WEBHOOK_URL, headers=headers, data=data) as response:
        response.raise_for_status()


async def main(streamer:str, session) :
    print("Start", streamer)
    status = False
    while True :
        try :
            now_status = await is_live(streamer, session)
            if status != now_status and now_status :
                status = now_status
                await send_hook(names[streamer], session)
        except Exception as e :
            print(f"ERROR : {e}, Session : {streamer}")
        await asyncio.sleep(2)


async def run():
    async with aiohttp.ClientSession() as session :
        tasks = []
        for i in streamer :
            tasks.append(asyncio.create_task(main(i, session)))
        await asyncio.gather(*tasks)


if __name__ == "__main__" :
    asyncio.run(run())
