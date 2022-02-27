import youtube_dl

# we might want to take the url as an input
# passed back from the html frontend
def run(video_url=""):
    # asking user in command line to input url
    video_url = input("please enter youtube video url:")
    
    # get the url of the video
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = video_url,download=False
    )
    # save as a wave file
    filename = f"{video_info['title']}.wav"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }

    youtube_dl.YoutubeDL(options).download([video_info['webpage_url']])
    print("Download complete... {}".format(filename))

if __name__=='__main__':
    run()
