"""Constants for the LG ESS integration."""
import voluptuous as vol
from homeassistant.const import (
    POWER_WATT,
    ENERGY_KILO_WATT_HOUR,
    ENERGY_WATT_HOUR,
    MASS_KILOGRAMS,
)

DOMAIN = "lg_ess"
DATA_SCHEMA = vol.Schema({"name": str, "password": str, "ip": str})


VOLTAGE = "V"
CURRENT_AMPS = "A"
PERCENTAGE = "%"
UTMP = {
    "COMMON": {
        "PV": {
            "brand": "LGE-SOLAR",
            "capacity": ENERGY_KILO_WATT_HOUR,
            "pv1_voltage": VOLTAGE,
            "pv2_voltage": VOLTAGE,
            "pv1_power": POWER_WATT,
            "pv2_power": POWER_WATT,
            "pv1_current": CURRENT_AMPS,
            "pv2_current": CURRENT_AMPS,
            "today_pv_generation_sum": ENERGY_WATT_HOUR,
            "today_month_pv_generation_sum": ENERGY_WATT_HOUR,
        },
        "BATT": {
            "status": "1",
            "soc": PERCENTAGE,
            "dc_power": POWER_WATT,
            "winter_setting": "",
            "winter_status": "",
            "safty_soc": PERCENTAGE,
            "today_batt_discharge_enery": ENERGY_WATT_HOUR,
            "today_batt_charge_energy": ENERGY_WATT_HOUR,
            "month_batt_charge_energy": ENERGY_WATT_HOUR,
            "month_batt_discharge_energy": ENERGY_WATT_HOUR,
        },
        "GRID": {
            "active_power": POWER_WATT,
            "a_phase": "232.800003",
            "freq": "49.990002",
            "today_grid_feed_in_energy": ENERGY_WATT_HOUR,
            "today_grid_power_purchase_energy": ENERGY_WATT_HOUR,
            "month_grid_feed_in_energy": ENERGY_WATT_HOUR,
            "month_grid_power_purchase_energy": ENERGY_WATT_HOUR,
        },
        "LOAD": {
            "load_power": POWER_WATT,
            "today_load_consumption_sum": ENERGY_WATT_HOUR,
            "today_pv_direct_consumption_enegy": ENERGY_WATT_HOUR,
            "today_batt_discharge_enery": ENERGY_WATT_HOUR,
            "today_grid_power_purchase_energy": ENERGY_WATT_HOUR,
            "month_load_consumption_sum": ENERGY_WATT_HOUR,
            "month_pv_direct_consumption_energy": ENERGY_WATT_HOUR,
            "month_batt_discharge_energy": ENERGY_WATT_HOUR,
            "month_grid_power_purchase_energy": ENERGY_WATT_HOUR,
        },
        "PCS": {
            "today_self_consumption": PERCENTAGE,
            "month_co2_reduction_accum": MASS_KILOGRAMS,
            "today_pv_generation_sum": ENERGY_WATT_HOUR,
            "month_pv_generation_sum": ENERGY_WATT_HOUR,
            "today_grid_feed_in_energy": ENERGY_WATT_HOUR,
            "month_grid_feed_in_energy": ENERGY_WATT_HOUR,
            "pcs_stauts": "",
            "feed_in_limitation": PERCENTAGE,
            "operation_mode": "",
        },
    },
    "HOME": {
        "statistics": {
            "pcs_pv_total_power": POWER_WATT,
            "batconv_power": POWER_WATT,
            "bat_use": "",
            "bat_status": "",
            "bat_user_soc": PERCENTAGE,
            "load_power": POWER_WATT,
            "load_today": "0.0",
            "grid_power": "9",
            "current_day_self_consumption": PERCENTAGE,
            "current_pv_generation_sum": ENERGY_WATT_HOUR,
            "current_grid_feed_in_energy": POWER_WATT,
        },
        "direction": {
            "is_direct_consuming_": "",
            "is_battery_charging_": "",
            "is_battery_discharging_": "",
            "is_grid_selling_": "",
            "is_grid_buying_": "",
            "is_charging_from_grid_": "",
        },
        "operation": {"status": "start", "mode": ""},
        "wintermode": {"winter_status": ""},
        "pcs_fault": {"pcs_status": ""},
    },
}
UNITS_BY_PATH = {
    "{}.{}.{}".format(a, b, c): UTMP[a][b][c]
    for a in UTMP.keys()
    for b in UTMP[a].keys()
    for c in UTMP[a][b].keys()
}

a = UNITS_BY_PATH.keys()
pass
