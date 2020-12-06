=================
pytest-telegram
=================

.. image:: https://img.shields.io/pypi/v/pytest-telegram.svg
        :target: https://pypi.python.org/pypi/pytest-telegram

.. image:: https://pyup.io/repos/github/rad96/pytest-telegram/shield.svg
        :target: https://pyup.io/repos/github/rad96/pytest-telegram/
        :alt: Updates
     


Pytest to Telegram reporting plugin


* Free software: MIT license


Requirements
------------

* Requests



Installation
------------

You can install "pytest-telegram" via `pip`_::

    $ pip install pytest-telegram


Usage
-----
* Use this plugin by running pytest normally and use the following options to customize report:


>>> telegram:
    --telegram_id=CHAT_ID
                        Id of telegram chat
    --telegram_token=BOT_TOKEN
                        Telegram Bot token
    --telegram_report_url=URL
                        Link for test report, optional
    --telegram_custom_test=TEXT
                        Custom text, will be added for message, optional
    --telegram_success_sticker_id=FILE_ID
                        File id of telegram sticker which will be attach to Success report
    --telegram_fail_sticker_id=FILE_ID
                        File id of telegram sticker which will be attach to Failed report

Example
-------
    $ pytest ./tests --telegram_id=100559633 --telegram_token=123:qwe --telegram_report_url=http://path.to.report --telegram_custom_text="This is custom text"

Success report:

.. image:: https://user-images.githubusercontent.com/2121715/101268709-7ba55200-3777-11eb-9552-cc24983419f2.png
        :target: https://user-images.githubusercontent.com/2121715/101268709-7ba55200-3777-11eb-9552-cc24983419f2.png

Failed report:

.. image:: https://user-images.githubusercontent.com/2121715/101268724-a8596980-3777-11eb-8d0e-38e0621b3006.png
        :target: https://user-images.githubusercontent.com/2121715/101268724-a8596980-3777-11eb-8d0e-38e0621b3006.png

Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`file an issue`: https://github.com/rad96/pytest-telegram/issues
.. _`pip`: https://pypi.python.org/pypi/pip/
