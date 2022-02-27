import requests
import time
import matplotlib.pyplot as plt


# key
# auth_key = '477777efd84f4620acef79e26843fc34'


def read_file(filename):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(5242880)
            if not data:
                break
            yield data


def transcribe_request(sentiment_analysis=True, iab_categories=False, auth_key="9035a07ce7cb48b9826ccf5ac942fa23",
                       file_name="Filian possesed on stream.mp3"):
    # what is fed into the api
    headers = {"authorization": auth_key, "content-type": "application/json"}
    # uploading to assembly ai
    upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(file_name))
    # result url
    audio_url = upload_response.json()["upload_url"]
    transcript_request = {'audio_url': audio_url, 'sentiment_analysis': sentiment_analysis,
                          "iab_categories": iab_categories}
    # transcript_request = {'audio_url': audio_url, "auto_highlights": True, 'sentiment_analysis': True,
    # "iab_categories": True, "auto_chapters": True, "entity_detection": True}
    # asking assembly ai to access out audio url
    transcript_response = requests.post("https://api.assemblyai.com/v2/transcript", json=transcript_request,
                                        headers=headers)
    # response from api, access the id,
    _id = transcript_response.json()["id"]
    # after url, we access file using the id
    # give us a text file, if response
    for _ in range(100):
        polling_response = requests.get("https://api.assemblyai.com/v2/transcript/" + _id, headers=headers)
        while polling_response.json()['status'] != 'completed':
            time.sleep(1)
            polling_response = requests.get("https://api.assemblyai.com/v2/transcript/" + _id, headers=headers)
        with open(_id + '.txt', 'w') as f:
            f.write(polling_response.json()['text'])
        print('Transcript saved to', _id, '.txt')
        return polling_response.json()


def sentiment_booliser(emotion):
    if emotion == 'NEGATIVE':
        return -1
    elif emotion == 'POSITIVE':
        return 1
    else:
        return 0


def sentiment_analysis(response_json):
    starts = []
    emotions = []
    emotion_bool = {"NEGATIVE": -1, "POSITIVE": 1, "NEUTRAL": 0}
    for phrase in response_json['sentiment_analysis_results']:
        print(phrase['text'], ',', phrase['sentiment'])
        starts.append(phrase['start'])
        emotions.append(emotion_bool[phrase['sentiment']])
    fig, ax = plt.subplots()
    ax.plot(starts, emotions)
    ax.set_xlabel("Time")
    ax.set_ylabel("Emotion")
    ax.set_ylim(-1, 1)
    ax.grid()
    plt.title("Emotion over soundbite")
    plt.show()
    return starts, emotions


if __name__ == "__main__":
    response_json = transcribe_request()
    starts, emotions = sentiment_analysis(response_json)
