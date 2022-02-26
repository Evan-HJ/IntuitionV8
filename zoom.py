from zoomus import ZoomClient
import secrets,json
client = ZoomClient(secrets.zoom_apikey, secrets.zoom_apisecret)

def create_meeting(topic):
    #Returns join url
    res = client.meeting.create(user_id = 'cepfinal2@gmail.com', topic = topic, settings = {
        'join_before_host': True,
        'waiting_room': False
        })
    #print(res.content)
    return json.loads(res.content)['join_url']
