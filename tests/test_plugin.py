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
                    '\nhttp://report_link.com\n'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--telegram_id', telegram_chat_id,
                          '--telegram_token', telegram_token,
                          '--telegram_report_url', telegram_report_url)

        sticker_request = mock_post.mock_calls[0]
        sticker_called_url = sticker_request[1][0]
        sended_sticker = sticker_request[2]['json']['sticker']
        message_request = mock_post.mock_calls[4]
        message_called_url = message_request[1][0]
        message_text = message_request[2]['json']['text']
        message_chat_id = message_request[2]['json']['chat_id']

        assert sticker_called_url == f'https://api.telegram.org/bot{telegram_token}/sendSticker'
        assert message_called_url == f'https://api.telegram.org/bot{telegram_token}/sendMessage'
        assert message_text == expected_text
        assert message_chat_id == telegram_chat_id
        assert sended_sticker == fail_sticker_id
