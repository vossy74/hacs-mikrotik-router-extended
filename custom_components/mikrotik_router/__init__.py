"""Mikrotik Router integration."""

from __future__ import annotations

import voluptuous as vol
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import device_registry
from homeassistant.config_entries import ConfigEntry

from homeassistant.const import CONF_VERIFY_SSL

from .const import PLATFORMS, DOMAIN, DEFAULT_VERIFY_SSL
from .coordinator import MikrotikData, MikrotikCoordinator, MikrotikTrackerCoordinator

SCRIPT_SCHEMA = vol.Schema(
    {vol.Required("router"): cv.string, vol.Required("script"): cv.string}
)

_LOGGER = logging.getLogger(__name__)


# ---------------------------
#   _get_coordinator
# ---------------------------
def _get_coordinator(hass, router_name):
    """Find coordinator by router name (config entry title)."""
    for entry_id, data in hass.data.get(DOMAIN, {}).items():
        entry = hass.config_entries.async_get_entry(entry_id)
        if entry and entry.title == router_name:
            return data.data_coordinator
    return None


# ---------------------------
#   async_setup_services
# ---------------------------
async def async_setup_services(hass: HomeAssistant) -> None:
    """Register MikroTik Router services."""
    if hass.services.has_service(DOMAIN, "dns_entry_add"):
        return

    async def handle_dns_entry_add(call):
        coordinator = _get_coordinator(hass, call.data["router"])
        if not coordinator:
            _LOGGER.error("MikroTik: Router '%s' not found", call.data["router"])
            return
        attrs = {"name": call.data["name"], "address": call.data["address"]}
        if "ttl" in call.data:
            attrs["ttl"] = call.data["ttl"]
        if "comment" in call.data:
            attrs["comment"] = call.data["comment"]
        await hass.async_add_executor_job(
            coordinator.api.add_entry, "/ip/dns/static", attrs
        )
        await coordinator.async_refresh()

    async def handle_dns_entry_delete(call):
        coordinator = _get_coordinator(hass, call.data["router"])
        if not coordinator:
            _LOGGER.error("MikroTik: Router '%s' not found", call.data["router"])
            return
        await hass.async_add_executor_job(
            coordinator.api.remove_entry, "/ip/dns/static", "name", call.data["name"]
        )
        await coordinator.async_refresh()

    async def handle_dhcp_lease_make_static(call):
        coordinator = _get_coordinator(hass, call.data["router"])
        if not coordinator:
            _LOGGER.error("MikroTik: Router '%s' not found", call.data["router"])
            return
        await hass.async_add_executor_job(
            coordinator.api.execute,
            "/ip/dhcp-server/lease",
            "make-static",
            "mac-address",
            call.data["mac_address"],
        )
        await coordinator.async_refresh()

    async def handle_dhcp_lease_delete(call):
        coordinator = _get_coordinator(hass, call.data["router"])
        if not coordinator:
            _LOGGER.error("MikroTik: Router '%s' not found", call.data["router"])
            return
        await hass.async_add_executor_job(
            coordinator.api.remove_entry,
            "/ip/dhcp-server/lease",
            "mac-address",
            call.data["mac_address"],
        )
        await coordinator.async_refresh()

    async def handle_script_run(call):
        coordinator = _get_coordinator(hass, call.data["router"])
        if not coordinator:
            _LOGGER.error("MikroTik: Router '%s' not found", call.data["router"])
            return
        await hass.async_add_executor_job(
            coordinator.api.run_script, call.data["script_name"]
        )

    hass.services.async_register(DOMAIN, "dns_entry_add", handle_dns_entry_add)
    hass.services.async_register(DOMAIN, "dns_entry_delete", handle_dns_entry_delete)
    hass.services.async_register(DOMAIN, "dhcp_lease_make_static", handle_dhcp_lease_make_static)
    hass.services.async_register(DOMAIN, "dhcp_lease_delete", handle_dhcp_lease_delete)
    hass.services.async_register(DOMAIN, "script_run", handle_script_run)


# ---------------------------
#   async_setup_entry
# ---------------------------
async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    coordinator = MikrotikCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()
    coordinatorTracker = MikrotikTrackerCoordinator(hass, config_entry, coordinator)
    await coordinatorTracker.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = MikrotikData(
        data_coordinator=coordinator,
        tracker_coordinator=coordinatorTracker,
    )

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    config_entry.async_on_unload(config_entry.add_update_listener(async_reload_entry))

    await async_setup_services(hass)

    return True


# ---------------------------
#   async_reload_entry
# ---------------------------
async def async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Reload the config entry when it changed."""
    await hass.config_entries.async_reload(config_entry.entry_id)


# ---------------------------
#   async_unload_entry
# ---------------------------
async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    if unload_ok := await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    ):
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


# ---------------------------
#   async_remove_config_entry_device
# ---------------------------
async def async_remove_config_entry_device(
    hass, config_entry: ConfigEntry, device_entry: device_registry.DeviceEntry
) -> bool:
    """Remove a config entry from a device."""
    return True


# ---------------------------
#   async_migrate_entry
# ---------------------------
async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    _LOGGER.debug(
        "Migrating configuration from version %s.%s",
        config_entry.version,
        config_entry.minor_version,
    )

    if config_entry.version < 2:
        new_data = {**config_entry.data}
        new_data[CONF_VERIFY_SSL] = DEFAULT_VERIFY_SSL
        hass.config_entries.async_update_entry(config_entry, data=new_data, version=2)

    _LOGGER.debug(
        "Migration to configuration version %s.%s successful",
        config_entry.version,
        config_entry.minor_version,
    )
    return True
