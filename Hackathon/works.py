import cv2
import mediapipe as mp
import math
import time
#import keyboard

'''pip install keyboard'''
#==================================
pose_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
times=10
Alert = -1
status = -1
#==================================

def is_turtleneck(ear, shoulder):
    print(">>거북목 검사하기<<")
    print(round(ear, 2), round(shoulder, 2))
    turtleneck = shoulder * 0.19
    if shoulder - turtleneck < ear:
        print("거북목 아님")
    else:
        print("거북목 의심해보시길...")

def get_angle_v2(p1, p2):
    print(">>정자세 검사하기<<")
    x = p2.x - p1.x
    y = p2.y - p1.y
    radian = math.atan2(y, x)
    degree = radian * 180 / math.pi
    if -180 < degree < -170 or 170 < degree < 180:
        print("이사람 정면이다!!!!!!!!")
    else:
        print("이사람 사이드다!!!!!!!!!!")

def is_sit(hip):
    print(">>앉아있는지 검사하기<<")
    if hip > 1:
        print("이사람 앉아있다!!!!")
    else:
        print("이사람 서있다!!!!!!!!!!")

def working():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # use webcam
    cap = cv2.VideoCapture(0)
    count = 0
    prevTime = time.time()
    while cap.isOpened():
        global times
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        times -= sec
        if times < 0:
            print("Alert!!!!!!!!!!운동하세요!!!!!!!")
            # if keyboard.is_pressed('q'):
            #     times = 10
            #     continue
        else:
            pass

        if count % 10 == 0:
            success, image = cap.read()
            if not success:
                print("카메라가 인식되지않습니다.")
                continue
            # 이미지를 좌우 반전을 시키고 BGR형태의 이미지를 RGB로 변환하여 활용합니다.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # 해당 영역에서 입력된 이미지를 분석하여 결과값을 도출해줍니다.
            results = pose.process(image)
            try:
                for index in pose_list:
                    if results.pose_landmarks.landmark[index].visibility < 0.000000000000000001:
                        results.pose_landmarks.landmark[index].x = None
                        results.pose_landmarks.landmark[index].y = None
                        results.pose_landmarks.landmark[index].z = None

                l_ear = results.pose_landmarks.landmark[7]
                l_sh = results.pose_landmarks.landmark[11]
                r_sh = results.pose_landmarks.landmark[12]
                l_hip = results.pose_landmarks.landmark[23]
                while True:
                    status = input("앉음 확인하기 1, 정자세 확인하기 2, 거북목 확인하기 3, 종료 q: ")
                    if status == '1':
                        # ================앉아있는지?==================
                        is_sit(l_hip.y)
                    elif status == '2':
                        # ================정자세인지?==================
                        get_angle_v2(l_sh, r_sh)

                    elif status == '3':
                        break

                    elif status == 'q':
                        return -1

                    else:
                        print("다른 값을 넣으세요.")

                #================거북목?======================
                # (시계 반대방향으로 도세요)
                is_turtleneck(l_ear.x, l_sh.x)

            # except TypeError as te:
            #     print(te)
            # except AttributeError as ae:
            #     print(ae)
            except Exception as e:
                #print(e)
                pass

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 이미지에 result에 저장된 좌표에 맞게 landmark를 표시합니다.
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.imshow('MediaPipe Pose', image)

        # esc누르면 끝나요
        if cv2.waitKey(5) & 0xFF == 27:
            break

    pose.close()
    cap.release()

if __name__ == "__main__":
    working()