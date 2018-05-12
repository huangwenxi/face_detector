
import cv2
import os
import json
import time
class DetectFace():
    def __init__(self, output_path, rate):
        self.output_path = output_path
        self.converted_pictures = []
        self.Unconverte_pictures = []
        self.converted_pictures_num = 0
        self.all_pictures_num = 0
        self.rate = rate

    def creat_cascadeclassifier(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def scan_input(self, input_path):
        if os.path.isdir(input_path) is False:
            return -1
        files = os.listdir(input_path)
        for _file in files:
            file = os.path.join(input_path, _file)
            if os.path.isdir(file) is True:
                self.scan_input(file)

            elif os.path.isfile(file) is True:
                if file not in self.converted_pictures:
                    self.detect_picture(file)
                    self.converted_pictures.append(file)
                    self.all_pictures_num += 1

    def detect_picture(self, picture):
        try:
            img = cv2.imread(picture)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except :
            # traceback.print_exc()
            print('can not parse picture:' + picture)
            return -1

        print('input... ' + picture)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) != 0:
            self.converted_pictures_num += 1
            img_height = len(img)
            img_width = len(img[0])
            for (x, y, w, h) in faces:

                # difference_height = img_height - h
                a_w = min(x, img_width - w -x)*self.rate
                a_h = min(y, img_height - h -y)*self.rate
                roi_color = img[int(y - 0.5*a_h):int(y + 0.5*a_h) + h, int(x - 0.5*a_w):int(x + 0.5*a_w) + w]
                output_picture = os.path.join(self.output_path,os.path.basename(picture))
                cv2.imwrite(output_picture, roi_color)
                print('output... ' + output_picture)
        else:
            print('can not convert picture...:' + picture)



def convert_video2_picture(video_path, output_path):#-vframes 30 -dframes 30
    ffmpeg_cmd = '/anaconda2/envs/py3.6/bin//ffmpeg -i video_file.mkv -r 0.01  -s 640x480 -f image2 '+ output_path +'/video_pictures/%03d.jpeg'
    os.system(ffmpeg_cmd)
    print('.......................................')

def load_setting():
    f = open('setting.json', encoding='utf-8')#use utf-8 encoding to parse file
    setting = json.load(f)
    if os.path.isdir(setting['input_path']) is False:
        print('please config correct input_path in setting.json')
    if os.path.isdir(setting['output_path']) is False:
        print('please config correct output_path in setting.json')
    return setting.get('input_path'),setting.get('output_path'),setting['rate']


if __name__ == '__main__':
    #load setting.json to get 'input_path' and 'output_path'
    # input_path,output_path,rate = load_setting()
    # detect = DetectFace(output_path,rate)
    # detect.creat_cascadeclassifier()
    # while True:
    #     detect.scan_input(input_path)
    #     time.sleep(1)
    input_path,output_path,rate = load_setting()
    convert_video2_picture(None, input_path)
