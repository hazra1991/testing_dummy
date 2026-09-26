"""Verify voice service registration and call functionality."""

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
                },
            ],
        },
        "voice": {
            "required": True,
            "lines": 2,
            "protocol": ["SIP"],
        },
        "wan": {
            "internet_access": True,
        },
    }
})
def test_voice_service_registration_and_call(
    setup_teardown, bf_logger, bf_context
):
    board, wan, cmts = setup_teardown

    bf_logger.log_step("Step1: Verify the board is available")
    assert board is not None

    bf_logger.log_step("Step2: Verify voice service provisioning")
    # TODO: Verify voice service configuration on the device.

    bf_logger.log_step("Step3: Verify voice line registration")
    # TODO: Verify the required voice lines are registered.

    bf_logger.log_step("Step4: Verify outbound voice call")
    # TODO: Place a call and verify successful call establishment.

    bf_logger.log_step("Step5: Verify bidirectional audio")
    # TODO: Verify audio transmission and reception.

    bf_logger.log_step("Step6: Verify call termination")
    # TODO: Terminate the call and verify both endpoints return to idle.

    bf_logger.log_step("Step7: Verify voice service remains operational")
    # TODO: Confirm voice registration remains intact after the call.
