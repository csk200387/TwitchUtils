import requests, json, time, threading

DISCORD_WEBHOOK_URL = ""

streamers = [] # streamers id


streamerInfo = { # ex
    "woowakgood" : {
        "name" : "우왁굳",
        "icon" : "https://static-cdn.jtvnw.net/jtv_user_pictures/ebc60c08-721b-4572-8f51-8be7136a0c96-profile_image-300x300.png"
    },
}

def inChat(name:str) :
    url = f"https://tmi.twitch.tv/group/user/{name}/chatters"
    response = requests.get(url).text
    data = json.loads(response)
    broadcaster = data["chatters"]["broadcaster"]
    if broadcaster == [] :
        return False
    else :
        return True

def sendHook(streamer:str, isIN:bool) :
    title = None
    headers = {"Content-Type" : "application/json"}
    title = "BroadCaster ON" if isIN else "BroadCaster OFF"
    name = streamerInfo[streamer]["name"]
    icon_url = streamerInfo[streamer]["icon"]
    data = {
        "embeds": [
            {
                "title": title,
                "author": {
                    "name": name,
                    "icon_url": icon_url
                }
            }
        ],
        "username": "BroadCast Alert",
        "avatar_url": "", # discord avatar img
    }
    data = json.dumps(data)
    requests.post(DISCORD_WEBHOOK_URL, headers=headers, data=data)

def run(streamer:str) :
    print("Start", streamer)
    status = False
    while True :
        try :
            nowStatus = inChat(streamer)
            if status != nowStatus :
                status = nowStatus
                sendHook(streamer, status)
        except :
            print("ERROR? Session :"+streamer)
            pass
        time.sleep(3)

threads = []
for i in streamers :
    t = threading.Thread(target=run, args=(i,))
    threads.append(t)
    t.start()

for t in threads :
    t.join()
