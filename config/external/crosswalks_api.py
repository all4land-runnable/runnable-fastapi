# config/external/crosswalks_api.py
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOCAL_PATH = PROJECT_ROOT / "dataset" / "dataset" / "crosswalks.json"

def get_crosswalks(source: str | Path | None = None) -> Any:
    """
    - source 지정 없으면: 환경변수 CROSSWALKS_SOURCE → 기본 로컬 파일 순.
    - http(s):// 이면 원격에서 받아서 JSON 파싱해 객체(dict/list)로 반환.
    - 파일이면 로컬에서 읽어 JSON 파싱해 객체(dict/list)로 반환.
    """
    src = str(source) if source else os.getenv("CROSSWALKS_SOURCE", str(DEFAULT_LOCAL_PATH))

    if src.startswith(("http://", "https://")):
        import requests
        resp = requests.get(src, timeout=10)
        resp.raise_for_status()
        return resp.json()

    p = Path(src)
    if not p.is_absolute():
        p = (PROJECT_ROOT / p).resolve()
    return json.loads(p.read_text(encoding="utf-8"))
