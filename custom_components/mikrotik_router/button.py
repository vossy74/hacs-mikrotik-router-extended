"""Support for the Mikrotik Router buttons."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import MikrotikEntity, async_add_entities
from .coordinator import MikrotikConfigEntry
from .button_types import (
    SENSOR_TYPES,
    SENSOR_SERVICES,
)


# ---------------------------
#   async_setup_entry
# ---------------------------
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: MikrotikConfigEntry,
    add_entities_callback: AddEntitiesCallback,
) -> None:
    """Set up entry for component"""
    dispatcher = {
        "MikrotikButton": MikrotikButton,
        "MikrotikScriptButton": MikrotikScriptButton,
        "MikrotikActionButton": MikrotikActionButton,
    }
    await async_add_entities(
        hass,
        config_entry,
        add_entities_callback,
        dispatcher,
        SENSOR_TYPES,
        SENSOR_SERVICES,
    )


# ---------------------------
#   MikrotikButton
# ---------------------------
class MikrotikButton(MikrotikEntity, ButtonEntity):
    """Representation of a button."""

    async def async_update(self):
        """Synchronize state with controller."""

    async def async_press(self) -> None:
        pass


# ---------------------------
#   MikrotikScriptButton
# ---------------------------
class MikrotikScriptButton(MikrotikButton):
    """Representation of a script button."""

    async def async_press(self) -> None:
        """Run script using Mikrotik API"""
        await self.async_run_routeros(
            self.coordinator.api.run_script, self._data["name"]
        )


# ---------------------------
#   MikrotikActionButton
# ---------------------------
class MikrotikActionButton(MikrotikButton):
    """Representation of a system action button."""

    async def async_press(self) -> None:
        """Execute system action via Mikrotik API"""
        key = self.entity_description.key
        if key == "system-reboot":
            await self.async_run_routeros(
                self.coordinator.api.execute, "/system", "reboot", None, None
            )
        elif key == "system-backup":
            await self.async_run_routeros(
                self.coordinator.api.execute, "/system/backup", "save", None, None
            )
