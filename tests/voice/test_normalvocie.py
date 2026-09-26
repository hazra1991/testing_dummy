```python
"""Verify basic voice service functionality."""

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
def test_voice_call(setup_teardown, bf_logger, bf_context):
    board, wan, cmts = setup_teardown

    bf_logger.log_step("Step1: Verify the board is available")
    assert board is not None

    bf_logger.log_step("Step2: Verify voice service is provisioned")
    # TODO: Verify voice service is provisioned on the board.

    bf_logger.log_step("Step3: Verify voice line registration")
    # TODO: Verify the voice line is registered.

    bf_logger.log_step("Step4: Place a voice call")
    # TODO: Place a call and verify it is successfully established.

    bf_logger.log_step("Step5: Verify voice communication")
    # TODO: Verify audio is working in both directions.

    bf_logger.log_step("Step6: End the call")
    # TODO: Terminate the call and verify the call ends successfully.
```
