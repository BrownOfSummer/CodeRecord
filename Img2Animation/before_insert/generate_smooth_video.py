# -*- coding utf-8 -*-
from __future__ import print_function
import os
import subprocess
def run_sys_command(command_str):
    print("command_str", command_str)
    fderr = subprocess.PIPE
     
    p = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE, stderr=fderr)  
    p.wait()
    stdout,stderr = p.communicate()
    print('stdout : ',stdout)
    print('stderr : ',stderr)

    return stdout

root_dir = '/Users/li_pengju/SomeDownload/Dataset/uray-4v/b'
subdirs = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
for subdir in subdirs:
    #input_video_path = os.path.join(root_dir, str(subdir), "datadir0", "a-"+str(subdir)+".mp4")
    input_video_path = os.path.join(root_dir, "b-"+str(subdir)+".mp4")
    #input_mask_path = os.path.join(root_dir, 'mask', "a-"+str(subdir)+"-mask.jpg");
    input_mask_path = os.path.join(root_dir, 'mask', "b-"+str(subdir)+"-mask.jpg");
    #output_video_path = os.path.join(root_dir, str(subdir), "datadir0", "a-"+str(subdir)+"-smoothed.mp4")
    output_video_path = os.path.join(root_dir, "b-"+str(subdir)+"-smoothed.mp4")
    if( os.path.exists(output_video_path) ):
        print("Exists ", output_video_path);
        continue;
    else:
        command_str = "./smooth_around_video "+input_mask_path+" "+input_video_path+" Y"
        run_sys_command(command_str)
        #print(command_str)

