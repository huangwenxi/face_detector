
import cv2
import os
import json
import time
import threading
import dlib
from skimage import io
class DetectFace():
    def __init__(self):
        self.converted_videos= []
        self.Unconverte_videos = {}
        self.converted_pictures = []
        self.Unconverte_pictures = []
        self.converted_pictures_num = 0
        self.all_pictures_num = 0

    def creat_cascadeclassifier(self):
        self.face_cascade = cv2.CascadeClassifier(self.classifier)

    def scan_video(self):
        while True:
            time.sleep(10)
            if os.path.isdir(self.video_input_path) is False:
                print(self.video_input_path +' not dir ')
                return -1
            files = os.listdir(self.video_input_path)
            print(files)
            print(self.converted_videos)
            for _file in files:
                file = os.path.join(self.video_input_path, _file)
                if file not in self.converted_videos:
                    file_ctime = os.stat(file).st_ctime
                    file_mtime = os.stat(file).st_mtime
                    print(int(file_ctime))
                    if time.time() - file_mtime > 30:
                        print('time.times() - os.stat(file).st_mtime > 30')
                        video_2_pictures_path = os.path.join(self.video_2_pictures_path, str(int(file_ctime)))
                        try:
                            os.mkdir(video_2_pictures_path)
                            pass
                        except:
                            pass
                        self.convert_video2_picture(file, video_2_pictures_path)
                        self.converted_videos.append(file)


    def scan_picture(self, input_path):
        files = os.listdir(input_path)
        for _file in files:
            file = os.path.join(input_path, _file)
            if os.path.isdir(file) is True:
                self.scan_picture(file)

            elif os.path.isfile(file) is True:
                if file not in self.converted_pictures:
                    self.detect_picture_opencv(file, self.output_path)
                    self.converted_pictures.append(file)
                    self.all_pictures_num += 1
                    print('Conversion rate:' + str(detect.converted_pictures_num / detect.all_pictures_num))

    def detect_picture_opencv(self, picture, output_path):
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
                parname_picture = os.path.basename(os.path.dirname(picture))
                filepath, tempfilename = os.path.split(picture);
                (shotname, extension) = os.path.splitext(tempfilename);
                c_time = time.localtime(int(shotname) + int(parname_picture))
                output_picture = os.path.join(output_path,  str(c_time.tm_year) + '_' +
                                              str(c_time.tm_mon) + '-' + str(c_time.tm_mday) + '_' + str(c_time.tm_hour) + '_' +
                                              str(c_time.tm_min) + '_' + str(c_time.tm_sec) + '.jpeg')
                print('output:' + output_picture)
                cv2.imwrite(output_picture, roi_color)
             
        else:
            print('can not convert picture:' + picture)

    def detect(self, picture, output_path):
        # 初始化dlib人脸检测器
        detector = dlib.get_frontal_face_detector()

        # opencv加载视频文件
        # cap = cv2.VideoCapture('2018-1-1/192.168.1.64_01_20180511172841401_1.mp4')

        index = 1
        img2 = None
        # while True:
            # ret, cv_img = cap.read()
            # if cv_img is None:
            #     break
        try:
            img = io.imread(picture)

            dets = detector(img, 1)
            print("Number of faces detected: {}".format(len(dets)))
            for i, d in enumerate(dets):
                print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                    i, d.left(), d.top(), d.right(), d.bottom()))
                img2 = img[d.top():d.bottom(), d.left():d.right()]
                parname_picture = os.path.basename(os.path.dirname(picture))
                filepath, tempfilename = os.path.split(picture);
                (shotname, extension) = os.path.splitext(tempfilename);
                c_time = time.localtime(int(shotname) + int(parname_picture))
                output_picture = os.path.join(output_path, str(c_time.tm_year) + '_' +
                                              str(c_time.tm_mon) + '-' + str(c_time.tm_mday) + '_' + str(
                    c_time.tm_hour) + '_' +
                                              str(c_time.tm_min) + '_' + str(c_time.tm_sec) + '.jpeg')

                io.imsave(output_picture, img2)
        except:
            pass
                # img2 = img[163:271, 28:91]
                # print(img2)
                # io.imsave('output/%d.jpeg'%index, img2)
                # dlib.hit_enter_to_continue()



    def load_setting(self):
        f = open('setting.json', encoding='utf-8')  # use utf-8 encoding to parse file
        setting = json.load(f)

        self.video_input_path = setting.get('video_input_path')
        self.video_2_pictures_path = setting['video_2_pictures_path']
        self.output_path = setting.get('output_path')
        self.rate = setting.get('rate')
        self.time = setting.get('time')
        self.bit = setting.get('bit')
        self.resolution = setting.get('resolution')
        self.ffmpeg = setting.get('ffmpeg')
        self.classifier = setting.get('classifier')
        print('resolution' + self.resolution)

    def convert_video2_picture(self, video_input_path, output_path):#-vframes 30 -dframes 30
        ffmpeg_cmd = self.ffmpeg +' -i ' + video_input_path + ' -r ' + str(self.time) + ' -s ' + self.resolution + ' -f image2 '+ output_path + os.path.sep + '%'+ str(self.bit) +'d.jpeg'
        os.system(ffmpeg_cmd)
        print('.......................................')

if __name__ == '__main__':
    detect = DetectFace()
    detect.load_setting()
    detect.creat_cascadeclassifier()

    t = threading.Thread(target=detect.scan_video)
    t.start()
    print('.....................')
    while True:
        time.sleep(1)
        detect.scan_picture(detect.video_2_pictures_path)


