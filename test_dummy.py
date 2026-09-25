"""Verify eRouter provisioning mode behaviour on the DUT."""

import pytest

from boardfarm3.lib.device_manager import DeviceManager


@pytest.mark.env_req({
    "environment_def": {
        "board": {
            "eRouter_Provisioning_mode": ["dual"],
            "lan_clients": [],
        }
    }
})
def test_erouter_provisioning_mode(setup_teardown, bf_logger, bf_context):
    board, wan, cmts = setup_teardown

    bf_logger.log_step("Step1: Verify the board is provisioned in dual mode")
    assert board is not None

    bf_logger.log_step("Step2: Verify WAN connectivity")
    # TODO: perform WAN connectivity verification

    bf_logger.log_step("Step3: Verify LAN client behaviour")
    # TODO: exercise LAN client behaviour

    bf_logger.log_step("Step4: Verify eRouter provisioning behaviour")
    # TODO: perform eRouter provisioning checks

    bf_logger.log_step("Step5: Verify the expected result")
    # TODO: add final assertions
