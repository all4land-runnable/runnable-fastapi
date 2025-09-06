# Introduce
GitHub에서 재사용하기 위해 제작한 Directory 기본 양식이다.

### Sample Template
```markdown
.
├── app
│   ├── __init__.py			    # 패키지 초기화
│   ├── main.py			        # FastAPI 앱 진입점 (uvicorn main:app 실행)
│   ├── dependencies.py		    # 공통 의존성 (DB, 인증, 공통 모듈 DI)
│   ├── routers			        # 비즈니스 도메인 별 API 엔드포인트
│   │   ├── __init__.py
│   │   └── items			    # Items 도메인
│   │	    ├── items.py		            # APIRouter 등록
│   │	    ├── items_controller.py	        # HTTP 요청 처리 (입출력)
│   │	    ├── items_repository.py	        # DB 처리 계층 (ORM)
│   │       ├── items_service.py	        # 비즈니스 로직
│   │	    └── dto			    # 요청/응답 모델
│   │		    ├── items_request.py
│   │		    └── items_response.py
│   └── internal				# 내부용 전용 API/모듈
│		├── __init__.py
│		├── exception			# 예외 처리 시스템
│		│	├── exception_handler.py	# FastAPI 글로벌 예외 처리 등록
│		│	└── error_code.py	# 에러코드 정의 및 매핑
│		├── logger.py			# 로깅 설정 (Logger 커스터마이징)
│		└── admin			    # Admin 도메인
│			├── admin_controller.py
│			├── admin_repository.py
│	   		├── admin_service.py
│			└── dto
│				├── admin_request.py
│				└── admin_response.py
├── config                      # 시스템 환경 설정 및 외부 라이브러리 초기화
│	├── database
│	│	├── database1.py		# 첫 번째 DB 클라이언트 (예: PostgreSQL, MySQL 등)
│	│	└── database2.py		# 추가 DB 클라이언트 (예: Redis, MongoDB 등)
│	└── llm
│		└── llm1.py			    # LLM 모델 초기화 및 클라이언트 관리
├── Dockerfile					# 도커 이미지 생성을 위한 DockerFile
└── test					    # 테스트 코드 (pytest 기반 유닛테스트/통합테스트)
```