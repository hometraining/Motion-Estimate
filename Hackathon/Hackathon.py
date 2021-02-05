import cv2
import mediapipe as mp
import math
import numpy as np

times=10
def is_pushup(shoulder_l, shoulder_r, elbow_l, elbow_r, wrist_l, wrist_r):
    l_elbow_angle = get_angle_v3(wrist_l, elbow_l, shoulder_l)
    r_elbow_angle = get_angle_v3(wrist_r, elbow_r, shoulder_r)

    elbow_angle = (l_elbow_angle + r_elbow_angle) / 2

    print("팔꿈치 각도 {0}".format(round(elbow_angle, 2)))


def is_squat(shoulder_l, shoulder_r, hip_l, hip_r, knee_l, knee_r, ankle_l, ankle_r):
    l_knee_angle = get_angle_v3(hip_l, knee_l, ankle_l)
    l_hip_angle = get_angle_v3(knee_l, hip_l, shoulder_l)
    r_knee_angle = get_angle_v3(hip_r, knee_r, ankle_r)
    r_hip_angle = get_angle_v3(knee_r, hip_r, shoulder_r)

    knee_angle = (l_knee_angle + r_knee_angle) / 2
    hip_angle = (l_hip_angle + r_knee_angle) / 2

    print("무릎 각도 {0} | 엉덩이 각도 {1}".format(round(knee_angle, 2), round(hip_angle, 2)))

    '''
    if 60 < knee_angle < 80 and  60 < hip_angle < 80:
        print("굳")
    else:
        if knee_angle < 60 or  80 < knee_angle :
            print("스쿼트 제대로해 발목나간다!!")
        elif hip_angle < 60 or  80 < hip_angle:
            print("스쿼트 제대로해 허리나간다!!")
    '''


'''
# 엉덩이 무릎 발목
def get_angle_squat_knee(type, hip, knee, ankle):
    if type == 'front':
        data1 = [(hip.y - knee.y), (hip.z - knee.z), (hip.x - knee.x)]
        data2 = [(ankle.y - knee.y), (ankle.z - knee.z), (ankle.x - knee.x)]
        array1 = np.array(data1)
        array2 = np.array(data2)
        angle = np.dot(array1, array2.T)
    elif type == 'side':
        data1 = [(hip.x - knee.x), (hip.y - knee.y), (hip.z - knee.z)]
        data2 = [(ankle.x - knee.x), (ankle.y - knee.y), (ankle.z - knee.z)]
        array1 = np.array(data1)
        array2 = np.array(data2)
        angle = np.dot(array1, array2.T)
    return angle
# 어깨 엉덩이 무릎
def get_angle_squat_hip(type, shoulder, hip, knee):
    if type == 'front':
        data1 = [(shoulder.y - hip.y), (shoulder.z - hip.z), (shoulder.x - hip.x)]
        data2 = [(knee.y - hip.y), (knee.z - hip.z), (knee.x - hip.x)]
        array1 = np.array(data1)
        array2 = np.array(data2)
        angle = np.dot(array1, array2.T)
    elif type == 'side':
        data1 = [(shoulder.x - hip.x), (shoulder.y - hip.y), (shoulder.z - hip.z)]
        data2 = [(knee.x - hip.x), (knee.y - hip.y), (knee.z - hip.z)]
        array1 = np.array(data1)
        array2 = np.array(data2)
        angle = np.dot(array1, array2.T)
    return angle
'''


# 엉덩이 무릎 발목
def get_angle_v3(p1, p2, p3):
    angle = math.degrees(math.atan2(p3.y - p2.y, p3.x - p2.x) - math.atan2(p1.y - p2.y, p1.x - p2.x))

    return angle + 360 if angle < 0 else angle

    '''
    o1 = math.atan((p1.y - p2.y)/(p1.x - p2.x))
    o2 = math.atan((p3.y - p2.y)/(p3.x - p2.x))
    angle = (abs((o1-o2) * 180/math.pi))
    return angle
    '''


def get_angle_v2(left, right):
    x = right.x - left.x
    y = right.y - left.y

    radian = math.atan2(y, x)
    degree = radian * 180 / math.pi

    if -180 < degree < -170 or 170 < degree < 180:
        print("이사람 정면다!!!!!!!!")
    else:
        print("이사람 사이드다!!!!!!!!!!")


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
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # 웹캠으로 사용
    cap = cv2.VideoCapture(0)
    count = 0
    while cap.isOpened():
        global times
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        times -= sec
        if times < 0:
            print("alert!!!!!!!!!!!!!!!!!!!!!!")
        
        if count % 24 == 0:
            success, image = cap.read()
            if not success:
                print("카메라가 인식되지않습니다.")
                continue
            # 이미지를 좌우 반전을 시키고 BGR형태의 이미지를 RGB로 변환하여 활용합니다.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # 해당 영역에서 입력된 이미지를 분석하여 결과값을 도출해줍니다.
            results = pose.process(image)

            try:

                l_shoulder = results.pose_landmarks.landmark[11]
                l_elbow = results.pose_landmarks.landmark[13]
                l_wrist = results.pose_landmarks.landmark[15]
                l_hip = results.pose_landmarks.landmark[23]
                l_knee = results.pose_landmarks.landmark[25]
                l_ankle = results.pose_landmarks.landmark[27]

                r_shoulder = results.pose_landmarks.landmark[12]
                r_elbow = results.pose_landmarks.landmark[14]
                r_wrist = results.pose_landmarks.landmark[16]
                r_hip = results.pose_landmarks.landmark[24]
                r_knee = results.pose_landmarks.landmark[26]
                r_ankle = results.pose_landmarks.landmark[28]

                # is_squat(l_shoulder, r_shoulder, l_hip, r_hip, l_knee, r_knee, l_ankle, r_ankle)
                is_pushup(l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist)
                '''
                #================거북목?======================
                l_ear = results.pose_landmarks.landmark[7].z
                l_sh = results.pose_landmarks.landmark[11].z
                is_turtleneck(l_ear, l_sh)
                #================정자세인지?==================
                l_sh = results.pose_landmarks.landmark[11]
                r_sh = results.pose_landmarks.landmark[12]
                get_angle_v2(l_sh, r_sh)
                #================앉아있는지?==================
                if results.pose_landmarks.landmark[23].y > 1:
                    print("이사람 앉아있다!!!!")
                else:
                    print("이사람 서있다!!!!!!!!!!")   
                '''

            except Exception as e:
                print(e)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 이미지에 result에 저장된 좌표에 맞게 landmark를 표시합니다.
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.imshow('MediaPipe Pose', image)
        count += 1

        # esc누르면 끝나요
        if cv2.waitKey(5) & 0xFF == 27:
            break

    pose.close()
    cap.release()


if __name__ == "__main__":
    main()
