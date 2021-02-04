# Motion-Estimate

```mediapipe```라이브러리 사용한 모션 인식


### requirements
```python
pip install python==3.7.4
pip install mediapipe==0.8.2
pip install opencv-python==4.5.0
```
## 앉아 있을 때
### 추가 기능
- 앉은 자세 판별
- 앉은 상태에서 정자세 판별 및 각도 추출
- 거북목 진단
- Timer 추가 (앉은 시간 판별 후 📢 ALERT)

## 운동할 때

### 추가 기능
#### SQUAT
- 무릎 각도와 엉덩이 각도를 내적을 통하여 연산
- 무릎 사이와 어깨사이의 길이 연산
