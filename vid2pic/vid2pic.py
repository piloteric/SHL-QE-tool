import cv2
import os

# 定位script，指定i/o影像位置
script_directory = os.path.dirname(os.path.realpath(__file__))
input_folder = script_directory
output_folder = script_directory

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

listing = [f for f in os.listdir(input_folder) if f.endswith(('.mp4', '.avi', '.MOV'))]

count = 1
for vid in listing:
    vid_path = os.path.join(input_folder, vid)
    print(f"Processing video: {vid_path}")
    vidcap = cv2.VideoCapture(vid_path)
    if not vidcap.isOpened():
        print(f"Cannot open video: {vid_path}")
        continue

    def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        hasFrames, image = vidcap.read()
        if hasFrames:
            # 原始影像放大兩倍
            timestamp = round(sec, 2)
            original_path = os.path.join(output_folder, f"{timestamp}s.jpg")
            original_doublesize = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            success_original = cv2.imwrite(original_path, original_doublesize)
            if not success_original:
                print(f"Failed to save original frame {timestamp}")

            # 旋轉影像放大兩倍 (逆時針旋轉90度)
            rotated_path = os.path.join(output_folder, f"{timestamp}s_rotated.jpg")
            rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            rotated_doublesize = cv2.resize(rotated_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            success_rotated = cv2.imwrite(rotated_path, rotated_doublesize)
            if not success_rotated:
                print(f"Failed to save rotated frame {timestamp}")

        return hasFrames

    # sec 影像起始點
    sec = 0
    # 每 n 秒截取
    frameRate = 5
    success = getFrame(sec)
    while success:
        print(f"Frame {count} extracted at {sec} seconds")
        count += 1
        sec += frameRate
        sec = round(sec, 2)
        success = getFrame(sec)