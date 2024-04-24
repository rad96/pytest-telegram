import datetime
import time
import logging
import pytest
import requests

from requests import exceptions


LOG = logging.getLogger(__name__)


def pytest_addoption(parser):
    group = parser.getgroup('telegram')
    group.addoption(
        '--telegram_id',
        action='store',
        dest='telegram_id',
        default=None,
        help='Id of telegram chat'
    )
    group.addoption(
        '--telegram_token',
        action='store',
        dest='telegram_token',
        default=None,
        help='telegram token'
    )
    group.addoption(
        '--telegram_success_sticker_id',
        action='store',
        dest='success_sticker_id',
        default='CAACAgIAAxkBAAMHX8roD4u8f7DCsRobma1dZNuCeBwAAlkBAAIQGm0iHZVsOV_OQB8eBA',
        help='file id of success sticker'
    )
    group.addoption(
        '--telegram_fail_sticker_id',
        action='store',
        dest='fail_sticker_id',
        default='CAACAgIAAxkBAAMIX8rohSxoNbodB1D38VZx9HI2CDwAAmIBAAIQGm0izcITZBkXtbceBA',
        help='file id of fail sticker'
    )
    group.addoption(
        '--telegram_report_url',
        action='store',
        dest='telegram_report_url',
        default=None,
        help='Report url'
    )
    group.addoption(
        '--telegram_custom_text',
        action='store',
        dest='telegram_custom_text',
        default=None,
        help='Custom text which will added to telegram message'
    )
    group.addoption(
        '--telegram_disable_stickers',
        action='store_true',
        dest='telegram_disable_stickers',
        help='Option for disable stickers'
    )
    group.addoption(
        '--telegram_list_failed',
        action='store_true',
        dest='telegram_list_failed',
        help='Option for list failed tests'
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    yield

    if not config.option.telegram_token:
        return
    # special check for pytest-xdist plugin, cause we do not want to send report for each worker.
    if hasattr(terminalreporter.config, 'workerinput'):
        return
    failed = len(terminalreporter.stats.get('failed', []))
    passed = len(terminalreporter.stats.get('passed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    error = len(terminalreporter.stats.get('error', []))
    xfailed = len(terminalreporter.stats.get("xfailed", []))
    xpassed = len(terminalreporter.stats.get("xpassed", []))

    token = config.option.telegram_token
    telegram_uri = f'https://api.telegram.org/bot{token}'
    chat_id = config.option.telegram_id

    success_sticker_id = config.option.success_sticker_id
    fail_sticker_id = config.option.fail_sticker_id
    report_url = f'\n{config.option.telegram_report_url}' if config.option.telegram_report_url else ''
    custom_text = f'\n{config.option.telegram_custom_text}'.replace('\\n',
                                                                    '\n') if config.option.telegram_custom_text else ''
    disable_stickers = config.option.telegram_disable_stickers
    list_failed = config.option.telegram_list_failed
    list_failed_amount = 3

    failed_tests = ''
    error_tests = ''
    if list_failed and failed != 0:
        failed_tests = '\nFailed tests:\n'

        for failed_test in terminalreporter.stats.get('failed', [])[:list_failed_amount]:
            failed_tests += f'{failed_test.nodeid}\n'

        if failed > list_failed_amount:
            failed_tests += '...'
    if list_failed and error != 0:
        error_tests = '\nError tests:\n'

        for error_test in terminalreporter.stats.get('error', [])[:list_failed_amount]:
            error_tests += f'{error_test.nodeid}\n'

        if error > list_failed_amount:
            error_tests += '...'
    final_results = 'Passed=%s Failed=%s Skipped=%s Error=%s XFailed=%s XPassed=%s' % (
        passed, failed, skipped, error, xfailed, xpassed)

    session_time = time.time() - terminalreporter._sessionstarttime
    time_taken = f'\nTime taken: {str(time.strftime("%H:%M:%S", time.gmtime(session_time)))}'

    if failed == 0 and error == 0:
        sticker_payload = {'chat_id': chat_id, 'sticker': success_sticker_id}
    else:
        sticker_payload = {'chat_id': chat_id, 'sticker': fail_sticker_id}
    try:
        message_id = None
        if not disable_stickers:
            message_id = requests.post(f'{telegram_uri}/sendSticker', json=sticker_payload).json()['result']['message_id']
        message_payload = {
            'chat_id': chat_id,
            'text': f'{final_results}{time_taken}{custom_text}{report_url}\n{failed_tests}{error_tests}',
            'reply_to_message_id': message_id
        }
        requests.post(f'{telegram_uri}/sendMessage', json=message_payload).json()
    except exceptions.RequestException as e:
        LOG.error("TELEGRAM Sending Message Error!!!")
        LOG.exception(e)
