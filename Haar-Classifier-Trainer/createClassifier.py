import cv2
import numpy as np
import os
import subprocess

totalCount =1000

def func_convert_togray():
    
    for file_type in os.listdir('./negative_images'):
        print(file_type + " Done")
        f_str = "negative_images/" +file_type 
        img= cv2.imread(f_str)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (100, 100))
        cv2.imwrite(f_str,img)
    print("=======================================")
    for file_type in os.listdir('./positive_images'):
        print(file_type +" Done")
        f_str = "positive_images/" +file_type
        img= cv2.imread(f_str)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (100, 100))
        cv2.imwrite(f_str,img)
    print("=======================================")
    
def func_create_pos_n_neg():
    for file_type in os.listdir('./negative_images'):
        line = "negative_images/"+ file_type +'\n'
        with open('bg.txt','a') as f:
            f.write(line)
            
    for file_type in os.listdir('./positive_images'):
        line = "positive_images/"+ file_type +' 1 0 0 100 100\n'
        with open('info.dat','a') as f:
            f.write(line)      

def create_samdples():
    
    for file_type in os.listdir('./positive_images'):
        file_path = "opencv_createsamples -img positive_images/"+file_type+" -bg bg.txt -info info/info.lst -pngoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num "+str(totalCount)
        print(run_win_cmd(file_path))

    print(run_win_cmd("opencv_createsamples -info info/info.lst -num "+str(totalCount)+" -w 20 -h 20 -vec positives.vec"))

    print(run_win_cmd("opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos 40 -numNeg 100 -numStages 10 -w 20 -h 20"))

def run_win_cmd(cmd):
    result = []
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    for line in process.stdout:
        result.append(line)
    errcode = process.returncode
    for line in result:
        print(line)
    if errcode is not None:
        raise Exception('cmd %s failed, see above for details', cmd)
    
func_convert_togray()
func_create_pos_n_neg()
create_samdples()
