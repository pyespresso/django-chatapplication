#!/usr/bin/env bash
coverage erase
echo "Initiating test run"
## Add all projects to be tested for coverage here if there are more than one
coverage run --source='chats' manage.py test chats
coverage html
echo "\n\nCoverage report is:-\n"
coverage report
