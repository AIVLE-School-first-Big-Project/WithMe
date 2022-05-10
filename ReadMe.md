# 🏫 언택트 시대 스터디 서비스, WithMe
<img src="https://github.com/inchangson/contents/blob/main/withme.JPG">

# 목차

- [실행 방법](#⚙-실행-방법)

- [서비스 개요](#📜-서비스-개요)

- [서비스 FLOW](#📳-서비스-flow)

- [기술 스택](#🧩-기술-스택)

- [Architecture](#📐-Architecture)

- [ERD](#🛢-ERD)

- [소개 영상](#📽-소개-영상)

- [조원](#🙇‍♂️-조원)


## ⚙ 실행방법

### 1. 환경 설정
- 제공된 env.zip을 압축 해제합니다.
- 비밀번호: 에이블수료날짜(YYYYMMDD)
- .env 파일을 프로젝트 디렉토리에 위치시킵니다.

### 2. 서비스 구동 (파이썬 환경)
```
> pip install -r requirements.txt
> python manage.py makemigrations
> python manage.py migrate
> python manage.py runserver
```

### 3. 웹페이지 이동
- 웹브라우저 실행 후 http://127.0.0.1:8000/ 로 이동

## 📜 서비스 개요


### 배경
- 메가스터디, 인프런, 유데미 등과 같은 인터넷 강의 플랫폼 및 유튜브 보급으로 인한 온라인 교육 확대
- 코로나 19로 인한 언택트 사회 가속화
- 온라인 강의 서비스에 비해 부족한 학습 관리 서비스
- 온라인 교육으로 인한 목 디스크 환자 급증 현상
> **언택트 시대에 맞는 자기주도 학습 서비스 제공**

### 주요 기능
- AI 모델을 통한 졸음, 이석 시간을 제외한 "실질 공부시간 측정 및 통계 서비스"
- AI 모델을 통한 "거북목 감지 및 통계 서비스"
- 서비스 이용자 간 질의응답, 소통할 수 있는 "게시판 서비스"

### 기대 효과
- 새로운 교육 온라인 플랫폼으로의 확대
- 기존 교육 플랫폼(kt Genius, Zoom 등)과의 연동 서비스 구축 가능

## 📳 서비스 FLOW
<img src="https://github.com/inchangson/contents/blob/main/serviceFlow.PNG">

## 🧩 기술 스택
<img src="https://github.com/inchangson/contents/blob/main/techstack.PNG">

## 📐 Architecture
<img src="https://github.com/inchangson/contents/blob/main/archi.png">

## 🛢 ERD
<img src="https://github.com/inchangson/contents/blob/main/erd.png">

## 📽 소개 영상
- 추후 업데이트 예정

## 🙇‍♂️ 조원
> 손인창 정태환 장병훈 정형섭 백지영