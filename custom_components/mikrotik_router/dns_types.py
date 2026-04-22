"""Definitions for Mikrotik Router DNS switch entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from homeassistant.components.switch import SwitchEntityDescription

from .const import DOMAIN

DEVICE_ATTRIBUTES_DNS = [
    "address",
    "type",
    "ttl",
    "comment",
]


@dataclass
class MikrotikDNSSwitchEntityDescription(SwitchEntityDescription):
    """Class describing mikrotik DNS switch entities."""

    icon_enabled: str | None = None
    icon_disabled: str | None = None
    ha_group: str | None = None
    ha_connection: str | None = None
    ha_connection_value: str | None = None
    data_path: str | None = None
    data_attribute: str = "enabled"
    data_name: str | None = None
    data_name_comment: bool = False
    data_uid: str | None = None
    data_reference: str | None = None
    data_attributes_list: List = field(default_factory=lambda: [])
    data_switch_path: str | None = None
    data_switch_parameter: str | None = None
    func: str = "MikrotikDNSSwitch"


SENSOR_TYPES: tuple[MikrotikDNSSwitchEntityDescription, ...] = (
    MikrotikDNSSwitchEntityDescription(
        key="dns",
        name="",
        icon_enabled="mdi:dns",
        icon_disabled="mdi:dns-outline",
        ha_group="DNS",
        ha_connection=DOMAIN,
        ha_connection_value="DNS",
        data_path="dns",
        data_attribute="enabled",
        data_name="name",
        data_uid="name",
        data_reference="name",
        data_attributes_list=DEVICE_ATTRIBUTES_DNS,
        data_switch_path="/ip/dns/static",
        data_switch_parameter="disabled",
        func="MikrotikDNSSwitch",
    ),
)

SENSOR_SERVICES = {}
