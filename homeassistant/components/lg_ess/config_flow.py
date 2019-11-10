"""Config flow for LG ESS integration."""
import logging

import voluptuous as vol

from homeassistant import core, config_entries, exceptions
from .const import DOMAIN  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)


# TODO adjust the data schema to the data that you need


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    # TODO validate the data can be used to set up a connection.
    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth
    from pyess.aio_ess import ESS, ESSException, ESSAuthException

    try:
        await ESS.create(data["name"], data["password"], data["ip"])
    except ESSAuthException:
        raise InvalidAuth
    except ESSException:
        raise CannotConnect

    # Return some info we want to store in the config entry.
    return {"password": data["password"], "ip": data["ip"], "name": data["name"]}


@config_entries.HANDLERS.register("lg_ess")
class DomainConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for LG ESS."""

    VERSION = 1
    # TODO pick one of the available connection classes in homeassistant/config_entries.py
    CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                await validate_input(self.hass, user_input)

                return self.async_create_entry(title=DOMAIN, data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        schema_with_defaults = vol.Schema(
            {
                vol.Optional("name", default=self.name): str,
                vol.Required("password"): str,
                vol.Required("ip", default=self.ip): str
                #                vol.Optional('sensors', default=['COMMON.PV.today_generatin_sum', 'COMMON.GRID.active_power',
                #                                                 'COMMON.LOAD.load_power']): list,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=schema_with_defaults, errors=errors
        )

    async def _async_step_init_show_form(self, name=None, ip=None):
        schema_with_defaults = vol.Schema(
            {
                vol.Optional("name", default=name): str,
                vol.Required("password"): str,
                vol.Required("ip", default=ip): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema_with_defaults)

    async def async_step_zeroconf(self, discovery_info):
        """Handle a discovered HomeKit accessory.

        This flow is triggered by the discovery component.
        """
        # Normalize properties from discovery
        # homekit_python has code to do this, but not in a form we can
        # easily use, so do the bare minimum ourselves here instead.
        from pyess.ess import extract_name_from_zeroconf

        self.name = name = extract_name_from_zeroconf(discovery_info["name"])
        self.ip = ip = discovery_info["host"]

        return await self._async_step_init_show_form(name=name, ip=ip)


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
