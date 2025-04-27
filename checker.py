#!/usr/bin/env python3
import requests

def check_code(code):
    req = requests.get("https://thinker.phoenix-ray.ts.net/check-code",
        params = {
        "code": code,
        "cubby_id": 1,
        }
    )
    return req.content, req.status_code
