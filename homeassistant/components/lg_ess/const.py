"""Constants for the LG ESS integration."""
import voluptuous as vol

DOMAIN = "lg_ess"
DATA_SCHEMA = vol.Schema({"name": str, "password": str, "ip": str})
