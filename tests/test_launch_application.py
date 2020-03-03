#!/usr/bin/python
import curses
import npyscreen
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import deployer
import pytest


@pytest.mark.skip(reason="Pytest doesn't utilze proper terminal supported by ncurses testing. This file should be ran manually")
def test_successful_launch_and_exit():
    npyscreen.TEST_SETTINGS['TEST_INPUT'] = ['^X', curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN, ord('\n')]
    npyscreen.TEST_SETTINGS['CONTINUE_AFTER_TEST_INPUT'] = False

    try:
        TA = deployer.App()
        TA.run(fork=False)
    except npyscreen.ExhaustedTestInput:
        pytest.fail("The application did not quit, and is still running")

if __name__ == '__main__':
    test_successful_launch_and_exit()
    sys.exit(0)

