import srt, unidecode, webvtt, os
from datetime import datetime
from unidecode import unidecode
from google_images_download import google_images_download  
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize



def transliterate(string):
    """Transliterates string into his closest representation.
    Ex: 1. àé => ae,
        2. สวัสดีครับ => swasdiikhrab.
    :param string: string
    :return: closest string.
    """
    if not isinstance(string, bytes):
        string = u''.join(string)

    return unidecode(string)


def format_text(string):
    for txt in transliterate(string).split("\n")[::-1]:
        if txt.strip() != "":
            return txt
    return "" 


def make_video(subs, outimg=None, fps=30, size=None,
               is_color=True, format="XVID"):
    fourcc = VideoWriter_fourcc(*format)
    vid = None
    total_frames=0
    subslist = [{"content":s.text, "start":to_deltatime(s.start), "end": to_deltatime(s.end)} for s in subs if len(s.text.strip()) >0]
    for (i, sub) in enumerate(subslist):
        image = paths[0][format_text(sub["content"])][0]
        if not os.path.exists(image):
            raise FileNotFoundError(image)
        img = imread(image)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter('video.mp4', fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)

        print(sub)
        if len(subslist) == i + 1:
            frames = int(sub["end"].total_seconds()*fps - total_frames)
        else:
            frames = int(subslist[i+1]["start"].total_seconds()*fps - total_frames)

        total_frames = frames + total_frames
        for i in range(frames):    
            vid.write(img)
    vid.release()
    return vid

def to_deltatime(timestp):
    return datetime.strptime(timestp, "%H:%M:%S.%f") - datetime.strptime("00:00:00.000", "%H:%M:%S.%f") 


def get_keywords_from_subs(subs):
    return ",".join([format_text(s.text) for s in subs if len(s.text.strip()) >0])

# with open("captions.srt") as f:
#     subs = srt.parse(f.read())

subs = webvtt.read('captions.vtt')

response = google_images_download.googleimagesdownload()

arguments = {"keywords":get_keywords_from_subs(subs), "limit":1,"print_urls":True}   #creating list of arguments
paths = response.download(arguments)   #passing the arguments to the function

print(paths)   #printing absolute paths of the downloaded images

subs = webvtt.read('captions.vtt')
make_video(subs, outimg=None, fps=2, size=None,is_color=True, format="XVID")

