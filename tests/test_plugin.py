import mock
import pytest


def test_pytest_telegram(testdir):
    """Make sure plugin works."""

    testdir.makepyfile(
        """
        import pytest
        def test_pass():
            assert 1 == 1


        def test_fail():
            assert 1 == 2


        @pytest.mark.skip()
        def test_skip():
            assert 1 == 1


        def test_error(test):
            assert 1 == ""


        @pytest.mark.xfail()
        def test_xfail():
            assert 1 == 2

        @pytest.mark.xfail()
        def test_xpass():
            assert 1 == 1
        """
    )

    telegram_token = 'Token'
    telegram_chat_id = '130559633'
    telegram_report_url = 'http://report_link.com'
    fail_sticker_id = 'CAACAgIAAxkBAAMIX8rohSxoNbodB1D38VZx9HI2CDwAAmIBAAIQGm0izcITZBkXtbceBA'
    expected_text = 'Passed=1 Failed=1 Skipped=1 Error=1 XFailed=1 XPassed=1' \
                    '\nTime taken: 00:00:00' \
                    '\nhttp://report_link.com\n'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--telegram_id', telegram_chat_id,
                          '--telegram_token', telegram_token,
                          '--telegram_report_url', telegram_report_url)

        sticker_request = mock_post.mock_calls[0]
        sticker_called_url = sticker_request[1][0]
        send_sticker = sticker_request[2]['json']['sticker']
        message_request = mock_post.mock_calls[4]
        message_called_url = message_request[1][0]
        message_text = message_request[2]['json']['text']
        message_chat_id = message_request[2]['json']['chat_id']

        assert sticker_called_url == f'https://api.telegram.org/bot{telegram_token}/sendSticker'
        assert message_called_url == f'https://api.telegram.org/bot{telegram_token}/sendMessage'
        assert message_text == expected_text
        assert message_chat_id == telegram_chat_id
        assert send_sticker == fail_sticker_id


def test_success_sticker_telegram(testdir):
    """Make sure plugin sends success sticker."""

    testdir.makepyfile(
        """
        import pytest
        def test_pass():
            assert 1 == 1
        """
    )

    telegram_token = 'Token'
    telegram_chat_id = '130559633'
    telegram_report_url = 'http://report_link.com'
    success_sticker_id = 'CAACAgIAAxkBAAMHX8roD4u8f7DCsRobma1dZNuCeBwAAlkBAAIQGm0iHZVsOV_OQB8eBA'
    expected_text = 'Passed=1 Failed=0 Skipped=0 Error=0 XFailed=0 XPassed=0' \
                    '\nTime taken: 00:00:00' \
                    '\nhttp://report_link.com\n'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--telegram_id', telegram_chat_id,
                          '--telegram_token', telegram_token,
                          '--telegram_report_url', telegram_report_url)

        sticker_request = mock_post.mock_calls[0]
        sticker_called_url = sticker_request[1][0]
        send_sticker = sticker_request[2]['json']['sticker']
        message_request = mock_post.mock_calls[4]
        message_called_url = message_request[1][0]
        message_text = message_request[2]['json']['text']
        message_chat_id = message_request[2]['json']['chat_id']

        assert sticker_called_url == f'https://api.telegram.org/bot{telegram_token}/sendSticker'
        assert message_called_url == f'https://api.telegram.org/bot{telegram_token}/sendMessage'
        assert message_text == expected_text
        assert message_chat_id == telegram_chat_id
        assert send_sticker == success_sticker_id


def test_list_failed_telegram(testdir):
    """Make sure plugin sends failed tests."""

    testdir.makepyfile(
        """
        import pytest
        def test_fail():
            assert 1 != 1
        """
    )

    telegram_token = 'Token'
    telegram_chat_id = '130559633'
    telegram_report_url = 'http://report_link.com'
    fail_sticker_id = 'CAACAgIAAxkBAAMIX8rohSxoNbodB1D38VZx9HI2CDwAAmIBAAIQGm0izcITZBkXtbceBA'
    expected_text = 'Passed=0 Failed=1 Skipped=0 Error=0 XFailed=0 XPassed=0' \
                    '\nTime taken: 00:00:00' \
                    '\nhttp://report_link.com\n' \
                    '\nFailed tests:' \
                    '\ntest_list_failed_telegram.py::test_fail\n'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--telegram_id', telegram_chat_id,
                          '--telegram_token', telegram_token,
                          '--telegram_report_url', telegram_report_url,
                          '--telegram_list_failed')

        sticker_request = mock_post.mock_calls[0]
        sticker_called_url = sticker_request[1][0]
        send_sticker = sticker_request[2]['json']['sticker']
        message_request = mock_post.mock_calls[4]
        message_called_url = message_request[1][0]
        message_text = message_request[2]['json']['text']
        message_chat_id = message_request[2]['json']['chat_id']

        assert sticker_called_url == f'https://api.telegram.org/bot{telegram_token}/sendSticker'
        assert message_called_url == f'https://api.telegram.org/bot{telegram_token}/sendMessage'
        assert message_text == expected_text
        assert message_chat_id == telegram_chat_id
        assert send_sticker == fail_sticker_id


def test_list_failed_with_dots_telegram(testdir):
    """Make sure plugin sends limited amount of failed tests."""

    testdir.makepyfile(
        """
        import pytest
        
        @pytest.mark.parametrize('id', range(10))
        def test_fail(id):
            assert 1 != 1
        """
    )

    telegram_token = 'Token'
    telegram_chat_id = '130559633'
    telegram_report_url = 'http://report_link.com'
    fail_sticker_id = 'CAACAgIAAxkBAAMIX8rohSxoNbodB1D38VZx9HI2CDwAAmIBAAIQGm0izcITZBkXtbceBA'
    expected_text = 'Passed=0 Failed=10 Skipped=0 Error=0 XFailed=0 XPassed=0' \
                    '\nTime taken: 00:00:00' \
                    '\nhttp://report_link.com\n' \
                    '\nFailed tests:' \
                    '\ntest_list_failed_with_dots_telegram.py::test_fail[0]' \
                    '\ntest_list_failed_with_dots_telegram.py::test_fail[1]' \
                    '\ntest_list_failed_with_dots_telegram.py::test_fail[2]' \
                    '\n...'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--telegram_id', telegram_chat_id,
                          '--telegram_token', telegram_token,
                          '--telegram_report_url', telegram_report_url,
                          '--telegram_list_failed')

        sticker_request = mock_post.mock_calls[0]
        sticker_called_url = sticker_request[1][0]
        send_sticker = sticker_request[2]['json']['sticker']
        message_request = mock_post.mock_calls[4]
        message_called_url = message_request[1][0]
        message_text = message_request[2]['json']['text']
        message_chat_id = message_request[2]['json']['chat_id']

        assert sticker_called_url == f'https://api.telegram.org/bot{telegram_token}/sendSticker'
        assert message_called_url == f'https://api.telegram.org/bot{telegram_token}/sendMessage'
        assert message_text == expected_text
        assert message_chat_id == telegram_chat_id
        assert send_sticker == fail_sticker_id


def test_time_taken(testdir):
    """Make sure plugin sends limited amount of failed tests."""

    testdir.makepyfile(
        """
        import pytest
        import time

        def test_fail():
            time.sleep(1)
            assert 1 != 1
        """
    )

    telegram_token = 'Token'
    telegram_chat_id = '130559633'
    telegram_report_url = 'http://report_link.com'
    fail_sticker_id = 'CAACAgIAAxkBAAMIX8rohSxoNbodB1D38VZx9HI2CDwAAmIBAAIQGm0izcITZBkXtbceBA'
    expected_text = 'Passed=0 Failed=1 Skipped=0 Error=0 XFailed=0 XPassed=0' \
                    '\nTime taken: 00:00:01' \
                    '\nhttp://report_link.com\n'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--telegram_id', telegram_chat_id,
                          '--telegram_token', telegram_token,
                          '--telegram_report_url', telegram_report_url)

        sticker_request = mock_post.mock_calls[0]
        sticker_called_url = sticker_request[1][0]
        send_sticker = sticker_request[2]['json']['sticker']
        message_request = mock_post.mock_calls[4]
        message_called_url = message_request[1][0]
        message_text = message_request[2]['json']['text']
        message_chat_id = message_request[2]['json']['chat_id']

        assert sticker_called_url == f'https://api.telegram.org/bot{telegram_token}/sendSticker'
        assert message_called_url == f'https://api.telegram.org/bot{telegram_token}/sendMessage'
        assert message_text == expected_text
        assert message_chat_id == telegram_chat_id
        assert send_sticker == fail_sticker_id