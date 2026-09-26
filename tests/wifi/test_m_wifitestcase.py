"""Verify WAN and LAN connectivity after eRouter provisioning."""

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
def test_erouter_wan_lan_connectivity(setup_teardown, bf_logger, bf_context):
    board, wan, cmts = setup_teardown

    bf_logger.log_step("Step1: Verify the board is available")
    assert board is not None

    bf_logger.log_step("Step2: Verify the WAN device is available")
    assert wan is not None

    bf_logger.log_step("Step3: Verify the CMTS device is available")
    assert cmts is not None

    bf_logger.log_step("Step4: Verify WAN connectivity")
    # TODO: Verify connectivity from the board to the WAN.

    bf_logger.log_step("Step5: Verify LAN client connectivity")
    # TODO: Verify that LAN clients can reach the expected network destinations.

    bf_logger.log_step("Step6: Verify the expected result")
    # TODO: Add final connectivity assertions.
