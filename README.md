# 📌 FastAPI 기반 음식 및 메뉴 관리 시스템

✅ **FastAPI, SQLAlchemy, Pydantic을 사용하여 구축된 음식 및 메뉴 관리 API**  
✅ **SQLite를 기본 데이터베이스로 활용하며, CORS 설정 및 환경 변수 관리 지원**  
✅ **CRUD 기능 구현 (메뉴 및 음식 관리, 음식 점수 저장 기능 포함)**  

---

## 📌 프로젝트 개요
이 프로젝트는 **FastAPI** 기반의 RESTful API로, 음식 및 메뉴 데이터를 관리하는 기능을 제공합니다.  
FastAPI의 **비동기(Async)** 기능을 활용하여 빠르고 효율적인 API 성능을 제공합니다.  
또한, **Pydantic을 사용한 데이터 검증**, **SQLAlchemy ORM을 통한 DB 관리**, **CORS 설정** 등의 기능을 포함하고 있습니다.  

🚀 **주요 기능**
- `메뉴 CRUD (생성, 조회, 삭제)`
- `음식 CRUD (생성, 조회, 삭제)`
- `음식 점수 저장 및 조회`
- `SQLite 데이터베이스 연동`
- `환경 변수 관리 (.env 지원)`
- `FastAPI의 Pydantic을 활용한 데이터 검증`
- `Swagger UI & ReDoc을 통한 API 문서 자동화`

---

## 📌 프로젝트 구조
```plaintext
📂 back-end/
│── 📂 app/
│   ├── 📂 models/             # SQLAlchemy ORM 모델 정의
│   │   ├── menus.py           # 메뉴 관련 데이터 모델
│   │   ├── foods.py           # 음식 관련 데이터 모델
│   │   ├── scores.py          # 음식 점수 모델
│   │
│   ├── 📂 schemas/            # Pydantic 데이터 검증 모델
│   │   ├── menus.py           # 메뉴 요청 및 응답 스키마
│   │   ├── foods.py           # 음식 요청 및 응답 스키마
│   │   ├── scores.py          # 점수 요청 및 응답 스키마
│   │
│   ├── 📂 crud/               # 데이터베이스 CRUD 로직
│   │   ├── menus.py           # 메뉴 관련 CRUD 함수
│   │   ├── foods.py           # 음식 관련 CRUD 함수
│   │   ├── scores.py          # 점수 관련 CRUD 함수
│   │
│   ├── 📂 routers/            # FastAPI 라우터 설정
│   │   ├── menus.py           # 메뉴 API 엔드포인트
│   │   ├── foods.py           # 음식 API 엔드포인트
│   │   ├── scores.py          # 점수 API 엔드포인트
│   │
│   ├── database.py            # SQLAlchemy DB 설정 및 초기화
│   ├── main.py                # FastAPI 애플리케이션 엔트리포인트
│   ├── config.py              # 환경 변수 및 설정 로직
│
│── 📄 .env                    # 환경 변수 설정 파일 (DB 연결 등)
│── 📄 requirements.txt         # 프로젝트 종속 패키지 목록
│── 📄 README.md                # 프로젝트 문서
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

### 🔹 3️⃣ 필요 패키지 설치
```bash
pip install -r requirements.txt
```

### 🔹 4️⃣ 환경 변수 설정 (.env 파일)
`.env` 파일을 생성하고 다음과 같이 설정합니다.
```ini
# SQLite DB 경로 설정
SQLITE_URL=sqlite:///./database.db

# FastAPI 설정
CORS_ORIGINS=*
```

### 🔹 5️⃣ 데이터베이스 초기화
```bash
python -c "from app.database import init_db; init_db()"
```

### 🔹 6️⃣ FastAPI 서버 실행
```bash
uvicorn app.main:app --reload
```

---

## 📌 API 문서 (Swagger UI)
FastAPI는 자동으로 API 문서를 생성하며, 브라우저에서 접근할 수 있습니다.

| API 문서 유형 | URL |
|--------------|------------------------|
| Swagger UI  | `http://127.0.0.1:8000/docs` |
| ReDoc       | `http://127.0.0.1:8000/redoc` |

---

## 📌 주요 API 엔드포인트
### 🔹 1️⃣ 메뉴 관리
| 메서드 | 경로 | 설명 |
|--------|------|------|
| `POST` | `/api/v1/menus/` | 새로운 메뉴 생성 |
| `GET`  | `/api/v1/menus/{date}` | 특정 날짜의 메뉴 조회 |

### 🔹 2️⃣ 음식 관리
| 메서드 | 경로 | 설명 |
|--------|------|------|
| `POST` | `/api/v1/foods/` | 새로운 음식 생성 |
| `GET`  | `/api/v1/foods/{food_id}` | 특정 음식 조회 |

### 🔹 3️⃣ 음식 점수 관리
| 메서드 | 경로 | 설명 |
|--------|------|------|
| `POST` | `/api/v1/foods/score` | 음식 점수 저장 |

---

## 📌 기술 스택
- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Database:** SQLite
- **Documentation:** Swagger UI, ReDoc

---
