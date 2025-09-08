from __future__ import annotations

import os
import sys
from pathlib import Path
import subprocess

def _get_host() -> str:
    # 외부 접속 허용 기본값
    return os.getenv("HOST", "0.0.0.0")

def _get_port() -> int:
    return int(os.getenv("PORT", "8000"))

def _get_reload() -> bool:
    return os.getenv("RELOAD", "1") == "1"

def run_subprocess():
    host = _get_host()
    port = _get_port()
    reload_ = _get_reload()

    cmd = [
        sys.executable, "-m", "uvicorn", "app.main:app",
        "--host", host, "--port", str(port)
    ]
    if reload_:
        cmd.append("--reload")

    # 실행 기준 디렉터리: 이 파일 위치
    workdir = str(Path(__file__).resolve().parent)

    try:
        proc = subprocess.Popen(cmd, env=os.environ.copy(), cwd=workdir)
        proc.wait()
        code = proc.returncode
    except KeyboardInterrupt:
        code = 130
        try:
            proc.terminate()
        except Exception:
            pass
    sys.exit(code)

def run_inproc():
    import uvicorn
    host = _get_host()
    port = _get_port()
    reload_ = _get_reload()
    uvicorn.run("app.main:app", host=host, port=port, reload=reload_)

def parse_overrides():
    # 간단한 CLI 오버라이드: --host, --port, --reload/--no-reload
    # (환경변수보다 우선)
    args = sys.argv[1:]
    for i, a in enumerate(list(args)):
        if a == "--host" and i + 1 < len(args):
            os.environ["HOST"] = args[i + 1]
        if a == "--port" and i + 1 < len(args):
            os.environ["PORT"] = args[i + 1]
        if a == "--reload":
            os.environ["RELOAD"] = "1"
        if a == "--no-reload":
            os.environ["RELOAD"] = "0"

if __name__ == "__main__":
    parse_overrides()
    if "--inproc" in sys.argv:
        sys.argv.remove("--inproc")
        run_inproc()
    else:
        run_subprocess()
