"""Board eRouter provisioning and connectivity test suite.

This module validates eRouter provisioning behaviour across different
provisioning modes and verifies WAN/LAN connectivity after provisioning.
"""

from __future__ import annotations

import time

import pytest

from boardfarm3.lib.device_manager import DeviceManager


DEFAULT_TIMEOUT = 30
DEFAULT_RETRY_INTERVAL = 2


@pytest.fixture
def provisioning_config():
    """Return the default provisioning configuration used by the tests."""
    return {
        "mode": "dual",
        "lan_clients": [],
        "verify_connectivity": True,
    }


def wait_for_device_ready(device, timeout=DEFAULT_TIMEOUT):
    """Wait until the device reports that it is ready for testing."""

    start_time = time.time()

    while time.time() - start_time < timeout:
        if device.is_ready():
            return True

        time.sleep(DEFAULT_RETRY_INTERVAL)

    return False


def configure_provisioning_mode(board, mode):
    """Configure the requested eRouter provisioning mode on the board."""

    current_mode = board.get_provisioning_mode()

    if current_mode != mode:
        board.set_provisioning_mode(mode)

    return board.get_provisioning_mode()


def verify_wan_connectivity(wan):
    """Verify that the WAN interface has working connectivity."""

    status = wan.check_connectivity()

    if not status:
        return False

    return wan.get_ip_address() is not None


def verify_lan_clients(board, expected_count):
    """Verify that the board reports the expected number of LAN clients."""

    clients = board.get_lan_clients()

    return len(clients) == expected_count


def collect_device_state(board, wan, cmts):
    """Collect the relevant device state for diagnostic purposes."""

    return {
        "provisioning_mode": board.get_provisioning_mode(),
        "lan_clients": len(board.get_lan_clients()),
        "wan_connected": wan.check_connectivity(),
        "cmts_connected": cmts.is_connected(),
    }


@pytest.mark.env_req({
    "environment_def": {
        "board": {
            "eRouter_Provisioning_mode": ["dual"],
            "lan_clients": [],
        }
    }
})
def test_erouter_dual_mode_provisioning(
    setup_teardown,
    bf_logger,
    bf_context,
    provisioning_config,
):
    """Verify successful provisioning of the board in dual mode.

    The test configures the board for dual eRouter provisioning mode,
    verifies the CMTS connection, checks WAN connectivity, and finally
    validates that the expected LAN client configuration is active.
    """

    board, wan, cmts = setup_teardown

    bf_logger.log_step("Step1: Verify that the board is ready")
    assert wait_for_device_ready(board), "Board did not become ready"

    bf_logger.log_step("Step2: Verify CMTS connectivity")
    assert cmts.is_connected(), "CMTS connection is not available"

    bf_logger.log_step("Step3: Configure the board for dual provisioning")
    mode = configure_provisioning_mode(
        board,
        provisioning_config["mode"],
    )
    assert mode == "dual"

    bf_logger.log_step("Step4: Verify WAN connectivity")
    if provisioning_config["verify_connectivity"]:
        assert verify_wan_connectivity(wan), (
            "WAN connectivity verification failed"
        )

    bf_logger.log_step("Step5: Verify LAN client configuration")
    assert verify_lan_clients(
        board,
        len(provisioning_config["lan_clients"]),
    )

    bf_logger.log_step("Step6: Collect final device state")
    state = collect_device_state(board, wan, cmts)

    assert state["provisioning_mode"] == "dual"
    assert state["lan_clients"] == 0
    assert state["wan_connected"] is True
    assert state["cmts_connected"] is True


@pytest.mark.env_req({
    "environment_def": {
        "board": {
            "eRouter_Provisioning_mode": ["dual"],
            "lan_clients": [],
        }
    }
})
@pytest.mark.parametrize(
    "requested_mode",
    ["dual", "bridge"],
    ids=["dual-mode", "bridge-mode"],
)
def test_erouter_provisioning_modes(
    setup_teardown,
    bf_logger,
    bf_context,
    requested_mode,
):
    """Verify that the board accepts the supported provisioning modes."""

    board, wan, cmts = setup_teardown

    bf_logger.log_step(
        f"Step1: Verify device readiness before configuring {requested_mode}"
    )
    assert wait_for_device_ready(board)

    bf_logger.log_step("Step2: Verify CMTS connectivity")
    assert cmts.is_connected()

    bf_logger.log_step(
        f"Step3: Configure provisioning mode to {requested_mode}"
    )
    actual_mode = configure_provisioning_mode(
        board,
        requested_mode,
    )

    bf_logger.log_step("Step4: Verify configured provisioning mode")
    assert actual_mode == requested_mode

    bf_logger.log_step("Step5: Verify WAN state after provisioning")
    wan_status = wan.check_connectivity()

    if requested_mode == "dual":
        assert wan_status is True
    else:
        assert wan_status in (True, False)


def get_expected_device_state(mode, lan_client_count):
    """Build the expected device state used by validation tests."""

    return {
        "mode": mode,
        "lan_clients": lan_client_count,
        "requires_wan": mode == "dual",
        "requires_cmts": True,
    }


def validate_device_state(actual_state, expected_state):
    """Compare actual device state against the expected state."""

    errors = []

    if actual_state["mode"] != expected_state["mode"]:
        errors.append(
            f"Expected mode {expected_state['mode']}, "
            f"got {actual_state['mode']}"
        )

    if actual_state["lan_clients"] != expected_state["lan_clients"]:
        errors.append(
            f"Expected {expected_state['lan_clients']} LAN clients, "
            f"got {actual_state['lan_clients']}"
        )

    if expected_state["requires_cmts"] and not actual_state["cmts_connected"]:
        errors.append("CMTS connection is unavailable")

    if expected_state["requires_wan"] and not actual_state["wan_connected"]:
        errors.append("WAN connectivity is unavailable")

    return errors


class TestProvisioningValidation:
    """Additional validation scenarios for eRouter provisioning."""

    @pytest.mark.env_req({
        "environment_def": {
            "board": {
                "eRouter_Provisioning_mode": ["dual"],
                "lan_clients": [],
            }
        }
    })
    def test_initial_device_state(
        self,
        setup_teardown,
        bf_logger,
        bf_context,
    ):
        """Verify the initial device state before provisioning."""

        board, wan, cmts = setup_teardown

        bf_logger.log_step("Step1: Check board readiness")
        assert wait_for_device_ready(board)

        bf_logger.log_step("Step2: Collect initial device state")
        state = collect_device_state(board, wan, cmts)

        assert state["cmts_connected"] is True
        assert state["provisioning_mode"] is not None

    @pytest.mark.env_req({
        "environment_def": {
            "board": {
                "eRouter_Provisioning_mode": ["dual"],
                "lan_clients": [],
            }
        }
    })
    def test_final_device_state(
        self,
        setup_teardown,
        bf_logger,
        bf_context,
    ):
        """Verify the complete device state after provisioning."""

        board, wan, cmts = setup_teardown

        bf_logger.log_step("Step1: Configure dual provisioning")
        configure_provisioning_mode(board, "dual")

        bf_logger.log_step("Step2: Collect device state")
        actual_state = collect_device_state(board, wan, cmts)

        bf_logger.log_step("Step3: Build expected device state")
        expected_state = get_expected_device_state(
            mode="dual",
            lan_client_count=0,
        )

        bf_logger.log_step("Step4: Validate device state")
        errors = validate_device_state(
            actual_state,
            expected_state,
        )

        assert not errors, "\n".join(errors)
