import pytest
from tools.scoped_login_state import scoped_state


def test_scoped_state_excludes_other_sites_and_user_history():
    state = {'cookies': [{'domain': d} for d in
                         ['.douyin.com', 'www.douyin.com', 'notdouyin.com', 'douyin.com.evil.test']],
             'origins': [{'origin': origin, 'localStorage': [
                 {'name': 'security-sdk/s_sdk_cert_key', 'value': 'fixture'},
                 {'name': 'SEARCH_AI_HISTORY_user', 'value': 'private'},
                 {'name': 'user_info', 'value': 'private'}]}
                 for origin in ['https://www.douyin.com', 'https://evil.test', 'http://www.douyin.com']]}
    result = scoped_state(state)
    assert len(result['cookies']) == 2
    assert len(result['origins']) == 1
    assert result['origins'][0]['localStorage'] == [
        {'name': 'security-sdk/s_sdk_cert_key', 'value': 'fixture'}]


def test_no_cookies_fails_closed():
    with pytest.raises(ValueError):
        scoped_state({'cookies': []})
