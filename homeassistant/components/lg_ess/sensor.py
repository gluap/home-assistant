"""support for reading values from ESS."""
import datetime
import logging

from .const import DOMAIN, UNITS_BY_PATH
from homeassistant.helpers.entity import Entity


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Old configuration."""
    pass


PATHES = [
    "COMMON.PV.brand",
    "COMMON.PV.capacity",
    "COMMON.PV.pv1_voltage",
    "COMMON.PV.pv2_voltage",
    "COMMON.PV.pv1_power",
    "COMMON.PV.pv2_power",
    "COMMON.PV.pv1_current",
    "COMMON.PV.pv2_current",
    "COMMON.PV.today_pv_generation_sum",
    "COMMON.PV.today_month_pv_generation_sum",
    "COMMON.BATT.status",
    "COMMON.BATT.soc",
    "COMMON.BATT.dc_power",
    "COMMON.BATT.winter_setting",
    "COMMON.BATT.winter_status",
    "COMMON.BATT.safty_soc",
    "COMMON.BATT.today_batt_discharge_enery",
    "COMMON.BATT.today_batt_charge_energy",
    "COMMON.BATT.month_batt_charge_energy",
    "COMMON.BATT.month_batt_discharge_energy",
    "COMMON.GRID.active_power",
    "COMMON.GRID.a_phase",
    "COMMON.GRID.freq",
    "COMMON.GRID.today_grid_feed_in_energy",
    "COMMON.GRID.today_grid_power_purchase_energy",
    "COMMON.GRID.month_grid_feed_in_energy",
    "COMMON.GRID.month_grid_power_purchase_energy",
    "COMMON.LOAD.load_power",
    "COMMON.LOAD.today_load_consumption_sum",
    "COMMON.LOAD.today_pv_direct_consumption_enegy",
    "COMMON.LOAD.today_batt_discharge_enery",
    "COMMON.LOAD.today_grid_power_purchase_energy",
    "COMMON.LOAD.month_load_consumption_sum",
    "COMMON.LOAD.month_pv_direct_consumption_energy",
    "COMMON.LOAD.month_batt_discharge_energy",
    "COMMON.LOAD.month_grid_power_purchase_energy",
    "COMMON.PCS.today_self_consumption",
    "COMMON.PCS.month_co2_reduction_accum",
    "COMMON.PCS.today_pv_generation_sum",
    "COMMON.PCS.month_pv_generation_sum",
    "COMMON.PCS.today_grid_feed_in_energy",
    "COMMON.PCS.month_grid_feed_in_energy",
    "COMMON.PCS.pcs_stauts",
    "COMMON.PCS.feed_in_limitation",
    "COMMON.PCS.operation_mode",
    "HOME.statistics.pcs_pv_total_power",
    "HOME.statistics.batconv_power",
    "HOME.statistics.bat_use",
    "HOME.statistics.bat_status",
    "HOME.statistics.bat_user_soc",
    "HOME.statistics.load_power",
    "HOME.statistics.load_today",
    "HOME.statistics.grid_power",
    "HOME.statistics.current_day_self_consumption",
    "HOME.statistics.current_pv_generation_sum",
    "HOME.statistics.current_grid_feed_in_energy",
    "HOME.direction.is_direct_consuming_",
    "HOME.direction.is_battery_charging_",
    "HOME.direction.is_battery_discharging_",
    "HOME.direction.is_grid_selling_",
    "HOME.direction.is_grid_buying_",
    "HOME.direction.is_charging_from_grid_",
    "HOME.operation.status",
    "HOME.operation.mode",
    "HOME.wintermode.winter_status",
    "HOME.pcs_fault.pcs_status",
]


def iteratively_query_dict(path: list, d: dict):
    """
    Query a multidimensional dict with a list as the key.

    :param path:
    :param d:
    :return:
    """
    tmp = d
    for key in path:
        tmp = tmp[key]
    return tmp


async def async_setup_entry(hass, entry, async_add_entities):
    """Add an LG ESS entry."""
    ess = hass.data[DOMAIN][entry.data["ip"]]
    cache = ESS_Cache(ess)

    sensors = []
    for configured in PATHES:
        sensors.append(ESSSensor(cache, configured))
    async_add_entities(sensors)

    pass


class ESSSensor(Entity):
    """Representation of an CO2 sensor."""

    def __init__(self, ess, sensor_path):
        """Initialize a new PM sensor."""
        self._data = None
        self.ess = ess
        self.id = sensor_path
        self.sensor_path = sensor_path.split(".")
        self._name = "ESS_{}".format(self.sensor_path[-1])
        self._unit_of_measurement = UNITS_BY_PATH[sensor_path]

    @property
    def unique_id(self):
        """Return unique id generated from ess name and sensor id."""
        return "{}.{}".format(self.ess.ess.name, self.id)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._data is None:
            return None
        try:
            return float(iteratively_query_dict(self.sensor_path, self._data))
        except ValueError:
            # just return the string if it's not a number
            return iteratively_query_dict(self.sensor_path, self._data)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    async def async_update(self):
        """Read from sensor and update the state."""
        self._data = await self.ess.fetch()

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        result = {}
        return result


class ESS_Cache:
    """Data fetcher class."""

    def __init__(self, ess):
        """Init the data fetcher."""
        self.ess = ess
        self.data = None
        self.last = datetime.datetime.now()

    async def fetch(self):
        """Fetch data if cache is younger than 10 seconds."""
        if self.data is None or datetime.datetime.now() - self.last >= datetime.timedelta(
            seconds=10
        ):
            common = await self.ess.get_common()
            home = await self.ess.get_home()
            self.data = {"COMMON": common, "HOME": home}
        return self.data
