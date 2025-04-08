# 📌 FastAPI 기반 급식 평가 및 사용자 관리 시스템

✅ **FastAPI, SQLAlchemy, Pydantic을 활용해 구축된 급식 평가 및 사용자 관리 API 백엔드**  
✅ **음식, 메뉴, 댓글, 점수, 인증, 로그 기능을 포함한 통합형 RESTful API**  
✅ **SQLite 로컬 개발 환경 및 `.env` 환경 변수 기반 설정 지원**  
✅ **CRUD, 통계, 로그인, 요청/응답 로깅까지 포함한 완성형 백엔드 구조**  

---

## 📌 프로젝트 개요

이 프로젝트는 **급식 메뉴에 대한 사용자 평가 및 의견 수집**을 목적으로 한 **FastAPI 기반 RESTful 백엔드 서비스**입니다.  
음식/메뉴 관리부터 댓글, 점수 통계, 사용자 인증 및 프론트 로그 수집까지 **급식 서비스 운영에 필요한 모든 기능**을 제공합니다.

### 🔧 주요 특징
- **음식/메뉴 CRUD 및 통계 API 제공**
- **메뉴별 점수/댓글 집계 기능**
- **Pydantic을 활용한 데이터 유효성 검증**
- **SQLAlchemy ORM 기반 DB 모델링**
- **JWT 기반 사용자 로그인 및 인증**
- **요청/응답 자동 로깅 미들웨어 도입**
- **프론트엔드 사용자 이벤트 로그 수신 기능**
- **Swagger / ReDoc 문서 자동 생성**

---

## 📌 핵심 기능

### ✅ 인증/회원 기능
- 사용자 회원가입 (`POST /register`)
- 사용자 로그인 및 액세스 토큰 발급 (`POST /token`)
- 로그인된 사용자 정보 확인 (`GET /me`)

### ✅ 메뉴 기능
- 메뉴 등록 (`POST /menus`)
- 날짜별 메뉴 조회 (`GET /menus/{date}`)
- 메뉴에 포함된 음식 통계 조회 (`GET /menus/{menu_id}/statistics`)
- 메뉴별 총 점수/댓글 수 조회 (`GET /menus/{menu_id}/counters`)

### ✅ 음식 기능
- 음식 등록 (`POST /foods`)
- 음식 이름 수정 (`PATCH /foods/{food_id}`)
- 음식별 점수 통계 조회 (`GET /foods/{food_id}/statistic`)

### ✅ 점수 기능
- 음식 점수 등록 (`POST /foods/score`)
  - 여러 음식에 대한 점수를 한 번에 저장 가능

### ✅ 댓글 기능
- 메뉴에 댓글 등록 (`POST /menus/comments`)

### ✅ 프론트엔드 로그 수집
- 사용자 이벤트 로그 수신 및 저장 (`POST /logs/front`)

---

## 📌 프로젝트 구조
```bash
📦 app/
├── 📂 cores/               # 핵심 유틸, 인증 보안, 로거 등
│   ├── logger/            # 요청/응답 로깅 관련
│   │   └── logger.py
│   └── security.py        # 비밀번호 해시, JWT 등 보안 기능
│
├── 📂 crud/                # DB 조작 함수 (도메인별 CRUD)
│   ├── comments.py
│   ├── foods.py
│   ├── logs.py
│   ├── menus.py
│   └── users.py
│
├── 📂 dependencies/        # FastAPI Depends 의존성 모듈
│   ├── auth.py
│   └── user.py
│
├── 📂 middlewares/        # 커스텀 미들웨어
│   └── logging.py         # 요청/응답 로깅 미들웨어
│
├── 📂 models/              # SQLAlchemy ORM 모델 정의
│   ├── comments.py
│   ├── food_menu.py
│   ├── foods.py
│   ├── logs.py
│   ├── menus.py
│   ├── roles.py
│   ├── scores.py
│   └── users.py
│
├── 📂 routers/             # API 라우터 정의
│   ├── auth.py
│   ├── comments.py
│   ├── foods.py
│   ├── logs.py
│   ├── menus.py
│   └── users.py
│
├── 📂 schemas/             # Pydantic 요청/응답 모델 정의
│   ├── comments.py
│   ├── foods.py
│   ├── logs.py
│   ├── menus.py
│   ├── scores.py
│   ├── tokens.py
│   └── users.py
│
├── config.py               # 환경 설정
├── database.py             # DB 연결 및 초기화
├── main.py                 # FastAPI 앱 실행 진입점

📄 .env                      # 환경 변수 설정 파일
📄 .babp.db                  # SQLite 로컬 개발용 데이터베이스 파일
📄 requirements.txt          # 프로젝트 의존성 목록
📄 README.md                 # 프로젝트 설명 문서
📄 .gitignore                # Git 추적 제외 설정
```

---

## 📌 설치 및 실행 방법

### 🔹 1️⃣ 프로젝트 클론
```bash
git clone https://github.com/your-repo/fastapi-menus.git
cd fastapi-menus
```

### 🔹 2️⃣ 가상 환경 설정 (선택)
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 🔹 3️⃣ 패키지 설치
```bash
pip install -r requirements.txt
```

### 🔹 4️⃣ 환경 변수 설정 (.env)
```ini
SQLITE_URL=sqlite:///./database.db
CORS_ORIGINS=*
```

### 🔹 5️⃣ DB 초기화
```bash
python -c "from app.database import init_db; init_db()"
```

### 🔹 6️⃣ 서버 실행
```bash
uvicorn app.main:app --reload
```

---

## 📌 API 문서 (자동 생성)

| 문서 유형 | 주소 |
|----------|----------------------------|
| Swagger UI | `http://127.0.0.1:8000/docs` |
| ReDoc      | `http://127.0.0.1:8000/redoc` |

---

## 📌 주요 API 엔드포인트

### 🗂 메뉴(Menu)
| 메서드 | 경로 | 설명 |
|--------|------|------|
| `POST` | `/api/v1/menus/` | 메뉴 생성 |
| `GET`  | `/api/v1/menus/{date}` | 날짜별 메뉴 조회 |
| `GET`  | `/api/v1/menus/{menu_id}/statistics` | 메뉴에 속한 음식 점수 통계 |
| `GET`  | `/api/v1/menus/{menu_id}/counters` | 메뉴에 달린 댓글 수 및 점수 수 |
| `POST` | `/api/v1/menus/comments` | 메뉴에 댓글 작성 |

---

### 🍱 음식(Food)
| 메서드 | 경로 | 설명 |
|--------|------|------|
| `POST` | `/api/v1/foods/` | 음식 등록 |
| `PATCH`| `/api/v1/foods/{food_id}` | 음식 이름 수정 |
| `GET`  | `/api/v1/foods/{food_id}/statistic` | 음식별 점수 통계 |

---

### ⭐ 점수(Score)
| 메서드 | 경로 | 설명 |
|--------|------|------|
| `POST` | `/api/v1/foods/score` | 점수 일괄 등록 (여러 음식 대상) |

---

### 💬 댓글(Comment)
| 메서드 | 경로 | 설명 |
|--------|------|------|
| `POST` | `/api/v1/menus/comments` | 메뉴에 댓글 작성 |

---

### 🔐 인증(Auth)
| 메서드 | 경로 | 설명 |
|--------|------|------|
| `POST` | `/api/v1/auth/register` | 사용자 회원가입 |
| `POST` | `/api/v1/auth/token` | 사용자 로그인 (JWT 발급) |
| `GET`  | `/api/v1/auth/me` | 로그인된 사용자 정보 조회 |

---

### 📦 프론트 로그(Front Logs)
| 메서드 | 경로 | 설명 |
|--------|------|------|
| `POST` | `/api/v1/logs/front` | 프론트엔드 사용자 로그 수신 및 저장 |
