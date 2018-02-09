#!/usr/bin/env python

import os, sys, multiprocessing, traceback
from os.path import join, dirname, basename, realpath, splitext, isdir, isfile
from collections import namedtuple
from PIL import Image

BASE_DIR = dirname(realpath(__file__))
q = multiprocessing.Queue()

point = namedtuple('coordinate', ('x', 'y'))
csp = {   # camera start point
    'c10': point(33,34),
    'c11': point(63,34),    
    'c12': point(66,17),
    'c13': point(91,51),
    'c14': point(105,38),
    'c15': point(104,51),  
    'c16': point(75,54),  
    'c17': point(159,42),
    'c18': point(154,51),  
    'c19': point(145,32),
}


def crop(img, start_point, save_path, width=1116, height=632):
    img_dir = dirname(img)
    img_base_name = basename(img)
    img_name, img_ext = splitext(img_base_name)

    crop_box = [
        start_point.x,
        start_point.y,
        start_point.x + width,
        start_point.y + height
    ]

    im = Image.open(img)
    im.crop(crop_box).resize((1280,720)).save(save_path)


def frame_crop(plock):
    process_name = multiprocessing.current_process().name
    plock.acquire()
    print ">>> Process [ %s ] started!" % process_name
    plock.release()
    while True:
        try:
            frame_dir = q.get(timeout=5)
            plock.acquire()
            print ">>> Process [ %s ] handler [ %s ]!" % (process_name, basename(frame_dir))
            plock.release()

            new_frame_dir = join(BASE_DIR, "new", basename(frame_dir))
            if not isdir(new_frame_dir):
                os.makedirs(new_frame_dir)

            frames = [join(frame_dir, f) for f in os.listdir(frame_dir) if splitext(f)[1] == '.jpg']
            frames.sort()

            start_point = csp.get(basename(frame_dir))
            
            for f in frames:
                save_path = join(new_frame_dir, basename(f))
                crop(f, start_point, save_path)

        except:
            traceback.print_exc()
            break


plock = multiprocessing.Lock()

def main():
    camera_list = [d for d in os.listdir(BASE_DIR) if isdir(d) and d.startswith('c1')]
    camera_list.sort()
    for c in camera_list:
        c = join(BASE_DIR, c)
        q.put(c)

    process_list = []
    for i in range(4):
        p = multiprocessing.Process(target=frame_crop, args=(plock,))
        p.start()

        process_list.append(p)

    for p in process_list:
        p.join()


if __name__ == '__main__':
    main()
