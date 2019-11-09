"""The LG ESS integration."""
import voluptuous as vol

from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from .const import DOMAIN

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required("name"): str,
                vol.Required("password"): str,
                vol.Required("ip"): str,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Legacy setup way."""
    return True


async def async_setup_entry(hass, entry):
    """Set up the LG ESS integration."""

    from pyess.aio_ess import ESS

    # TODO forward the entry for each platform that you want to set up.
    # hass.async_create_task(
    #     hass.config_entries.async_forward_entry_setup(entry, "media_player")
    # )

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    params = entry.data
    lg_ess = await ESS.create(**params)

    hass.data[DOMAIN][params["ip"]] = lg_ess

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, lg_ess.destruct)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    #    hass.async_create_task(
    #        hass.config_entries.async_forward_entry_setup(entry, "switch")
    #    )

    return True
