"""M15: call a real local FastAPI server, then always stop the process started here."""

import json
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

card_dir = Path(__file__).resolve().parent
server = subprocess.Popen([sys.executable, "-m", "uvicorn", "bounded_api:app", "--app-dir", str(card_dir), "--port", "8015"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(30):
        try:
            with urlopen("http://127.0.0.1:8015/health", timeout=0.3) as response:
                health = json.load(response)
            break
        except OSError:
            time.sleep(0.1)
    else:
        raise RuntimeError("Local FastAPI server did not become healthy.")
    bad_request = Request("http://127.0.0.1:8015/v1/advisor/explain", data=b'{"question":""}', headers={"Content-Type": "application/json"}, method="POST")
    try:
        urlopen(bad_request, timeout=2)
    except HTTPError as error:
        invalid_status = error.code
    print({"health": health, "blank_question_status": invalid_status, "proof": "FastAPI validated input before model inference."})
finally:
    server.terminate()
    server.wait(timeout=5)
