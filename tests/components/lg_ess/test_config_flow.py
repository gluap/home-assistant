"""Test the LG ESS config flow."""
from unittest.mock import patch

from homeassistant import config_entries, setup
from homeassistant.components.lg_ess.config_flow import CannotConnect, InvalidAuth
from homeassistant.components.lg_ess.const import DOMAIN
from tests.common import mock_coro


async def test_form(hass):
    """Test we get the form."""
    await setup.async_setup_component(hass, "persistent_notification", {})
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_ZEROCONF},
        data={
            "name": "the_name",
            "password": "the_password",
            "ip": "the_ip",
            "host": "le host",
        },
    )
    assert result["type"] == "form"
    assert result["errors"] is None

    with patch(
            "homeassistant.components.lg_ess.config_flow.validate_input",
            return_value=mock_coro({"title": "Test Title"}),
    ), patch(
        "homeassistant.components.lg_ess.async_setup", return_value=mock_coro(True)
    ) as mock_setup, patch(
        "homeassistant.components.lg_ess.async_setup_entry",
        return_value=mock_coro(True),
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"name": "the_name", "password": "the_password", "ip": "the_ip"},
        )

    assert result2["type"] == "create_entry"
    assert result2["title"] == "lg_ess"
    assert result2["data"] == {
        "name": "the_name",
        "ip": "the_ip",
        "password": "the_password",
    }
    await hass.async_block_till_done()
    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_auth(hass):
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_ZEROCONF},
        data={
            "name": "the_name",
            "password": "the_password",
            "ip": "the_ip",
            "host": "le host",
        },
    )

    with patch(
            "homeassistant.components.lg_ess.config_flow.validate_input",
            side_effect=InvalidAuth,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"ip": "1.1.1.1", "name": "test-username", "password": "test-password", },
        )

    assert result2["type"] == "form"
    assert result2["errors"] == {"base": "invalid_auth"}


async def test_form_cannot_connect(hass):
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_ZEROCONF},
        data={
            "name": "the_name",
            "password": "the_password",
            "ip": "the_ip",
            "host": "le host",
        },
    )

    with patch(
            "homeassistant.components.lg_ess.config_flow.validate_input",
            side_effect=CannotConnect,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"ip": "1.1.1.1", "name": "test-username", "password": "test-password", },
        )

    assert result2["type"] == "form"
    assert result2["errors"] == {"base": "cannot_connect"}
