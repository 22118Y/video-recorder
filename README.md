<img src="https://capsule-render.vercel.app/api?type=waving&color=BDBDC8&height=150&section=header" />

## OpenCV video Recorder
OpenCV를 이용하여 웹캠 영상을 프리뷰하고, 원하는 시점에 녹화할 수 있는 간단한 비디오 레코더입니다.  
추가 기능으로 밝기 조절, 블러, 색 반전, 픽셀화 필터를 제공합니다.  

---

## 주요 기능
- **실시간 프리뷰**: 카메라 영상 거울 모드로 표시
- **녹화**: `Space` 키로 시작/종료 (녹화 시 화면에 REC 표시)
- **종료**: `ESC` 키로 프로그램 종료
- **필터 기능** :밝기, 블러, 색상 반전, 픽셀화

---

## 폴더 구성

다음 파일들은 모두 같은 위치에서 작동합니다.
- **cam_check.ipynb** : 가용 카메라의 유무 확인과 카메라 INDEX를 출력합니다.  
- **filters.py** : 추가 기능인 필터들의 코드 파일입니다.  
- **video-recorder.py** : 메인 코드 파일로, `def main()` 내부의 `cap = cv2.VideoCapture(INDEX)`에 cam_check.ipynb에서 출력된 INDEX와 동일하게 입력하여 실행합니다.

---

## 사용법
- **space** : 녹화 시작 / 종료 토글
- **ESC** : 프로그램 종료 토글
- **a** : 밝기 조절 필터 토글
- **↑ / ↓** : 밝기 조절 토글
- **s** : 블러 필터 토글
- **d** : 색상 반전 필터 토글
- **f** :픽셀화 필터 토글

---

## 저장
녹화된 파일은 recordings/ 폴더에 .mp4 형식으로 저장됩니다.

---

## 실행 예시(demo)
- **video-recoder_demo.mp4** : 전체 데모 영상
- **record_20250915_211448.mp4** : 화면 녹화 영상
  
<img src="https://capsule-render.vercel.app/api?type=waving&color=BDBDC8&height=150&section=footer" />
