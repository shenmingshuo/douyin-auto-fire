"""Filter a Playwright state from stdin; pipe stdout directly to a secret store.

Only Douyin cookies and security-SDK local storage are retained. Never log output.
This prepares a compatibility experiment, not a guarantee of cloud delivery.
"""
import json
import sys
from urllib.parse import urlsplit


def is_douyin(host):
    host = host.lower().lstrip('.')
    return host == 'douyin.com' or host.endswith('.douyin.com')


def scoped_state(state):
    cookies = [c for c in state['cookies'] if is_douyin(c.get('domain', ''))]
    origins = []
    for origin in state.get('origins', []):
        url = urlsplit(origin['origin'])
        if url.scheme != 'https' or not is_douyin(url.hostname or ''):
            continue
        items = [item for item in origin.get('localStorage', [])
                 if item['name'].startswith('security-sdk/')
                 or item['name'] == 'web_secsdk_runtime_cache']
        if items:
            origins.append({'origin': origin['origin'], 'localStorage': items})
    if not cookies:
        raise ValueError('No Douyin cookies in source state')
    return {'cookies': cookies, 'origins': origins}


if __name__ == '__main__':
    json.dump(scoped_state(json.load(sys.stdin)), sys.stdout, separators=(',', ':'))
