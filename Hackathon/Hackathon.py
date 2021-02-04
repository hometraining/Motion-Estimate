import cv2
import mediapipe as mp
import math
import time

times = 10


def get_angle(left, right):
    x = right.x - left.x
    y = right.y - left.y;
    radian = math.atan2(y, x);
    degree = radian * 180 / math.pi

    if -180 < degree < -170 or 170 < degree < 180:
        print("이사람 정자세다!!!!!!!!")
    else:
        print("이사람 정자세 아니다!!!!!!!!!!")


def is_turtleneck(ear, shoulder):
    # print(round(ear,2), round(shoulder,2))
    turtleneck = shoulder * 0.1

    if shoulder - turtleneck < ear < shoulder + turtleneck:
        print("거북목 아님")
    else:
        print("거북목 의심해보시길...")


def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # 웹캠으로 사용
    pose = mp_pose.Pose(min_detection_confidence=0.5)

    cap = cv2.VideoCapture(0)
    prevTime = time.time()
    print("TIMER START")

    while cap.isOpened():
        global times
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        times -= sec
        if times < 0:
            print("alert!!!!!!!!!!!!!")

        # print("sec", sec)

        success, image = cap.read()
        if not success:
            print("카메라가 인식되지않습니다.")
            continue
        # 이미지를 좌우 반전을 시키고 BGR형태의 이미지를 RGB로 변환하여 활용합니다.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # 해당 영역에서 입력된 이미지를 분석하여 결과값을 도출해줍니다.
        results = pose.process(image)

        '''
        try:
            if results.pose_landmarks.landmark[23].y > 1:
                print("이사람 앉아있다!!!!")

            else:
                print("이사람 서있다!!!!!!!!!!")
        '''

        '''
            #================거북목?======================
            l_ear = results.pose_landmarks.landmark[7].z
            l_sh = results.pose_landmarks.landmark[11].z

            is_turtleneck(l_ear, l_sh)
            #================정자세인지?==================
            l_sh = results.pose_landmarks.landmark[11]
            r_sh = results.pose_landmarks.landmark[12]
            get_angle(l_sh, r_sh)
            #================앉아있는지?==================
            print(results.pose_landmarks.landmark[23].y)

        '''

        # except Exception as e:
        #    print(e)

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
    main()