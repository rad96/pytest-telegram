import pytest
import requests


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
    custom_text = f'\n{config.option.telegram_custom_text}' if config.option.telegram_custom_text else ''

    final_results = 'Passed=%s Failed=%s Skipped=%s Error=%s XFailed=%s XPassed=%s' % (
        passed, failed, skipped, error, xfailed, xpassed)

    if failed == 0 and error == 0:
        payload = {'chat_id': chat_id, 'sticker': success_sticker_id}
    else:
        payload = {'chat_id': chat_id, 'sticker': fail_sticker_id}

    message_id = requests.post(f'{telegram_uri}/sendSticker', json=payload).json()['result']['message_id']
    payload = {'chat_id': chat_id, 'text': f'{final_results}{custom_text}{report_url}', 'reply_to_message_id': message_id}
    requests.post(f'{telegram_uri}/sendMessage', json=payload).json()
