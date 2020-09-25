import srt, unidecode
from google_images_download import google_images_download  
import os
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize



def transliterate(string):
    """Transliterates string into his closest representation.
    Ex: 1. àé => ae,
        2. สวัสดีครับ => swasdiikhrab.
    :param string: string
    :return: closest string.
    """
    from unidecode import unidecode

    if not isinstance(string, bytes):
        string = u''.join(string)

    return unidecode(string)


def make_video(subs, outimg=None, fps=30, size=None,
               is_color=True, format="XVID"):
    fourcc = VideoWriter_fourcc(*format)
    vid = None
    total_frames=0
    subslist = [{"content":s.content, "start":s.start, "end": s.end} for s in subs]
    for (i, sub) in enumerate(subslist):
        image = paths[0][transliterate(sub["content"])][0]
        if not os.path.exists(image):
            raise FileNotFoundError(image)
        img = imread(image)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter('video.mp4', fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)

        if len(subslist) == i + 1:
            frames = int(sub["end"].total_seconds()*fps - total_frames)
        else:
            frames = int(subslist[i+1]["start"].total_seconds()*fps - total_frames)

        total_frames = frames + total_frames
        for i in range(frames):    
            vid.write(img)
    vid.release()
    return vid

def get_keywords_from_subs(subs):
    return transliterate(",".join([s.content for s in subs]))

with open("captions.srt") as f:
    subs = srt.parse(f.read())

response = google_images_download.googleimagesdownload()

arguments = {"keywords":get_keywords_from_subs(subs), "limit":1,"print_urls":True}   #creating list of arguments
paths = response.download(arguments)   #passing the arguments to the function

print(paths)   #printing absolute paths of the downloaded images

with open("captions.srt") as f:
    subs = srt.parse(f.read())
    make_video(subs, outimg=None, fps=2, size=None,is_color=True, format="XVID")

