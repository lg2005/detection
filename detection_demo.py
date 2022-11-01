import cv2
from brainframe.api import BrainFrameAPI


def read_frame(stream_uri, frame_index):
    cap = cv2.VideoCapture(stream_uri)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    rst, frame = cap.read()
    if not rst:
        print(f"Failed to read frame: {frame_index}")
    cap.release()
    return frame


def detect_image(api, frame, capsule_names=None):
    if capsule_names is None:
        capsule_names = ["detector_person_openvino", "detector_face_openvino"]
    detections = api.process_image(frame, capsule_names, {})
    return detections

def face_detection(image):
	# 转成灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 创建一个级联分类器 加载一个.xml分类器文件 它既可以是Haar特征也可以是LBP特征的分类器
    face_detecter = cv2.CascadeClassifier(R'/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
    # 多个尺度空间进行人脸检测   返回检测到的人脸区域坐标信息
    faces = face_detecter.detectMultiScale(image=gray, scaleFactor=1.1, minNeighbors=5)
    print('检测人脸信息如下：\n', faces)
    for x, y, w, h in faces:
        # 在原图像上绘制圆形检测人脸
        cv2.circle(img=image, center=(x + w // 2, y + h // 2), radius=w // 2, color=[0, 255, 0], thickness=2)
    #cv2.imshow('result', image)
    return faces

def main():
    # The capsules for person and face detection

    #capsule_names = ["detector_person_openvino","detector_face_openvino"]
    '''???
    File "/home/gordon/.local/lib/python3.8/site-packages/brainframe/api/stubs/base_stub.py", line 359, in _perform_request  raise _make_api_error(resp=resp)
    brainframe.api.bf_errors.CapsuleNotFoundError: PluginNotFoundError: No capsule with name detector_face_openvino is loaded'''

    capsule_names = ["detector_person_openvino"]
    # The video file name, it can be replaced by the other video file or rtsp/http streams
    stream_path = "test.mp4"

    # The url to access the brainframe server with rest api
    bf_server_url = "http://localhost"

    api = BrainFrameAPI(bf_server_url)
    api.wait_for_server_initialization()

    cap = cv2.VideoCapture(stream_path)

    xy = [[0,0,0,0]]

    while True:
        #frame = read_frame(stream_path, 5)
        #cap.set(cv2.CAP_PROP_POS_FRAMES, 5)
        rst, frame = cap.read()
        if not rst:
            print(f"Failed to read frame")

        num_detections = 0
        if frame is not None:

            detections = detect_image(api, frame, capsule_names)
            print(detections)
            # Could extend the feature here to render and crop persons

            num_detections = len(detections)
            for index in range(num_detections):
                if detections[index].class_name == 'person':
                    coor = detections[index].coords
                    if index in range(len(xy)):
                        xy[index] = [coor[0][0],coor[0][1], coor[2][0], coor[2][1]]
                    else:
                        xy.append([coor[0][0],coor[0][1], coor[2][0], coor[2][1]])
                    cv2.rectangle(img=frame, pt1=(xy[index][0], xy[index][1]), pt2=(xy[index][2], xy[index][3]), color=[0, 0, 255], thickness=2)
                    cv2.imshow('output', frame)
            #end for

            face_detection(frame)
            cv2.imshow('output', frame)
        #end if

        keyv = cv2.waitKey(2)
        if ord('q') == keyv:
            break
        if ord('s') == keyv:
            for i in range(num_detections):
                str_crop = 'ocropped' + str(i)
                cropped = frame[xy[i][1]:xy[i][3], xy[i][0]:xy[i][2]]
                cv2.imshow(str_crop, cropped)
                str_crop += '.png'
                cv2.imwrite(str_crop, cropped)
            break

    cv2.waitKey()
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()
