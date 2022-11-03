This is a git repository for Brainframe, the files description as below.

grafana_dashboard.jpg:  the screen capture of grafana dashboard
<<<<<<< HEAD
Panel_enter_query.txt:    the SQL query for total count of enter person at Screen zone
Panel_exit_query.txt:       the SQL query for total count of exit person at Screen zone

--------------------------------------
2022/11/1 
=======
Panel_enter_query.txt:  the SQL query for total count of enter person at Screen zone
Panel_exit_query.txt:   the SQL query for total count of exit person at Screen zone
test.mp4:               test video file for brainframe client

--------------------------------------
2022/11/1 
新增文件 
>>>>>>> dc57c9020582eeabdb4035c50a70536c3896347f
detecttion_demo.py   
       读取视频test.mp4, 检测视频画面中的人像和人脸，人像用红框框出，人脸圆形标识；
        按 s 键抠出当前画面中的人像并保存到图片中, 程序终止；

        人像检测使用 brainframe capsule- detector_person_openvino, 运行正常
       人脸检测使用 brainframe capsule- detector_face_openvino，提示error：PluginNotFoundError: No capsule with name detector_face_openvino is loaded
       本程序人脸检测改用 OpenCV 级联分类器 haarcascade_frontalface_default.xml 运行正常
  
ocropped*.png 
       输出抠出的人像图形
