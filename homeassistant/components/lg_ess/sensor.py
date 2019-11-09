"""support for reading values from ESS."""
import logging

# SENSORS

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Old configuration."""
    pass


async def async_setup_entry(hass, entry, async_add_entities):
    """Add an solarEdge entry."""
    pass


class ESSDataFetcher:
    """Data fetcher class."""

    def __init__(self, ess):
        """Init the data fetcher."""
        self.ess = ess
