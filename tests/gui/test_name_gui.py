"""Verify the device web GUI login page is accessible and rendered correctly."""

import pytest

from boardfarm3.lib.device_manager import DeviceManager


@pytest.mark.env_req({
    "environment_def": {
        "board": {
            "eRouter_Provisioning_mode": ["dual"],
            "lan_clients": [
                {
                    "type": "linux",
                    "count": 1,
                    "connection": "ethernet",
                },
                {
                    "type": "wifi",
                    "count": 1,
                    "connection": "wireless",
                },
            ],
        },
        "wan": {
            "connection": "ethernet",
            "internet_access": True,
        },
        "cmts": {
            "required": True,
        },
    }
})
def test_gui_login_page(setup_teardown, bf_logger, bf_context):
    board, wan, cmts = setup_teardown

    bf_logger.log_step("Step1: Verify the board is available")
    assert board is not None

    bf_logger.log_step("Step2: Open the device web GUI")
    # TODO: Navigate to the device GUI.

    bf_logger.log_step("Step3: Verify the login page is displayed")
    # TODO: Assert that the login page is visible.

    bf_logger.log_step("Step4: Verify the login form elements")
    # TODO: Check username, password, and login button.

    bf_logger.log_step("Step5: Verify login form validation")
    # TODO: Submit empty credentials and verify validation.

    bf_logger.log_step("Step6: Verify the GUI is accessible after page refresh")
    # TODO: Refresh the page and verify it loads correctly.
