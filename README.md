# FastAPI Project Template
- FashAPI를 쉽고 빠르게 생성하기 위한 템플릿
1. 알고 있는 FashAPI 기술을 모두 접목
2. 존재하는 모든 코드에 주석으로 설명 작성

# Settings
## Step 1. Download Python3

## Step 2. Launch PostgreSQL
1. 본 프로젝트는 PostgreSQL를 활용합니다. `.env`에 본인의 계정 정보를 추가해주세요.
```markdown
POSTGRES_HOST={your_postgres_host}
POSTGRES_DATABASE={your_postgres_database}
POSTGRES_USER={your_postgres_user}
POSTGRES_PASSWORD={your_postgres_password}
POSTGRES_PORT={your_postgres_port}

MILVUS_URI={your_milvus_uri}

MODEL_VERSION={your_llm_ollama_model}
```
2. develop_database 데이터베이스 생성
- PostgreSQL에 develop_database를 생성하세요.
> 자동으로 생성되기를 원하면 테이블 생성 권한이 있는 DB_USER를 이용하세요. 

## Step 3. Launch Milvus
1. 본 프로젝트는 MilvusLite를 활용합니다. `.env`에 본인의 계정 정보를 추가해주세요.
```markdown
# TODO
```

## Step 3. 실행여부 확인
- 직접 접속해보세요! [Swagger UI 바로가기](http://localhost:8000/docs)

# How to Install
## from PyCharm
- PyCharm IDEA Ultimate
1. CommonSpringbootApplication.java로 이동한다.
![how-to-install-from-idea](docs/image/how-to-install-from-idea.png)

## 2. from JAR
- TODO

## 3. from Docker
- TODO

# API Documentation
- [Swagger UI](http://localhost:8000/docs)

# Directory Structure
- [Directory Strategy](docs/strategy/directory.md)

# Git Strategy
### Branch Strategy
- [Branch Strategy](docs/strategy/branch.md)

### PR Strategy
- [Pull Request Strategy](docs/strategy/pull-request.md)

### Issue Strategy
- [Issue Strategy](docs/strategy/issue.md)

# Dependency & Library
| Name               | Description                                                                                               | Version |
|--------------------|-----------------------------------------------------------------------------------------------------------|---------|
| backports.tarfile  | Backport of Python’s `tarfile` module (security/bug-fixes) for older runtimes; work with `.tar` archives. | 1.2.0   |
| dataclasses        | Backport of `dataclasses` (built-in on Python ≥3.7). Usually unnecessary on modern Python.                | 0.6     |
| dotenv             | Legacy dotenv loader package. **Most projects use `python-dotenv`** (`load_dotenv`) instead.              | 0.9.9   |
| fastapi            | High-performance web framework for building APIs with Pydantic and ASGI.                                  | 0.116.1 |
| importlib-metadata | Access package metadata (backport of `importlib.metadata` for older Python).                              | 8.0.0   |
| jaraco.collections | Small utility helpers around Python collections (dict/list/set tools) from the Jaraco suite.              | 5.1.0   |
| langchain          | Framework for building LLM apps (chains, agents, tools, memory, prompts, integrations).                   | 0.3.27  |
| langchain-ollama   | LangChain integration for **Ollama** (run local LLMs via Ollama within LangChain).                        | 0.3.6   |
| pip-chill          | Generates top-level (direct) dependencies with pinned versions.                                           | 1.0.3   |
| pipreqs            | Scans your source imports to generate a minimal `requirements.txt`.                                       | 0.5.0   |
| psycopg2-binary    | Precompiled PostgreSQL driver for Python (`psycopg2`)—easy install for dev.                               | 2.9.10  |
| pymilvus           | Official Python SDK for **Milvus** vector database (collections, indexes, vector CRUD/search).            | 2.6.0   |
| tinycss2           | Low-level CSS parser/tokenizer used by tools like `nbconvert`/`bleach`.                                   | 1.4.0   |
| tomli              | TOML parser (backport for older Python; stdlib `tomllib` on ≥3.11).                                       | 2.0.1   |
| torch              | PyTorch—tensor library and deep learning framework (CPU/GPU).                                             | 2.8.0   |
| transformers       | Hugging Face Transformers—pretrained model hub & pipelines for NLP/Vision/Audio.                          | 4.55.2  |
| uvicorn            | Lightning-fast ASGI server (often used to serve FastAPI apps).                                            | 0.35.0  |


# Support
### E-Mail
- aduwnssp@gmail.com

### Contributer
| Name | Role   | Description | Link                                                             |
|------|--------|-------------|------------------------------------------------------------------|
| 김명준  | Writer | 김명준입니다.     | [gomj Repository](https://github.com/gomj-repo?tab=repositories) |

# License
|Name|License|CopyRight|
|---|---|---|
|name|license|copy_right|