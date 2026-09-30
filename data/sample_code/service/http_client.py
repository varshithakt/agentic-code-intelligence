"""Outbound HTTP helper with timeouts and bounded retries."""
import time
from urllib.request import Request, urlopen
from urllib.error import URLError

def fetch_json(url, attempts=3, timeout=4):
    last_error=None
    for attempt in range(max(1,attempts)):
        try:
            request=Request(url,headers={"Accept":"application/json","User-Agent":"sample-service/1"})
            with urlopen(request,timeout=timeout) as response:
                import json
                return json.loads(response.read().decode("utf-8"))
        except (URLError,TimeoutError,ValueError) as exc:
            last_error=exc
            if attempt+1<attempts: time.sleep(0.1*(attempt+1))
    raise RuntimeError("Remote service request failed") from last_error
