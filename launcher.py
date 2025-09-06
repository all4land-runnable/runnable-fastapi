from __future__ import annotations

import os
import sys
from pathlib import Path
import subprocess

def run_subprocess():
    host = os.getenv("HOST", "localhost")
    port = os.getenv("PORT", "8000")
    reload = os.getenv("RELOAD", "1") == "1"

    cmd = [
        sys.executable, "-m", "uvicorn", "app.main:app",
        "--host", host, "--port", str(port)
    ]
    if reload:
        cmd.append("--reload")

    try:
        proc = subprocess.Popen(cmd, env=os.environ.copy(), cwd=str(Path(__file__).resolve().parent))
        proc.wait()
        sys.exit(proc.returncode)
    except KeyboardInterrupt:
        try:
            proc.terminate()
        except Exception:
            pass
        proc.wait()
        sys.exit(proc.returncode)

def run_inproc():
    import uvicorn
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "1") == "1"
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)

if __name__ == "__main__":
    if "--inproc" in sys.argv:
        sys.argv.remove("--inproc")
        run_inproc()
    else:
        run_subprocess()
