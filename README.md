# MikroTik Router Extended

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Extended Home Assistant integration for MikroTik routers running RouterOS 7.x.

Based on the original [homeassistant-mikrotik_router](https://github.com/tomaae/homeassistant-mikrotik_router) by tomaae.

## Features

### System
- **Reboot** button
- **Backup** button

### Firewall
- Filter, NAT and Mangle rule switches
- Bytes and packets statistics as attributes

### Network Interfaces
- RX/TX error counters

### DHCP
- Active, static and total lease sensors
- Device tracker for DHCP clients (home/away based on lease status)

### DNS
- Cache usage sensor (KiB)
- Static entry count sensor
- Switch per static DNS entry (enable/disable)

### Client Monitoring
- Total active client count sensor

### Services
| Service | Description |
|---|---|
| `mikrotik_router.dns_entry_add` | Add a static DNS entry |
| `mikrotik_router.dns_entry_delete` | Delete a static DNS entry |
| `mikrotik_router.dhcp_lease_make_static` | Convert a DHCP lease to static |
| `mikrotik_router.dhcp_lease_delete` | Delete a DHCP lease |
| `mikrotik_router.script_run` | Run a RouterOS script |

## Requirements

- Home Assistant 2023.x or newer
- MikroTik router running RouterOS 7.x
- MikroTik API enabled (port 8728)

## Installation via HACS

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click the three-dot menu → **Custom repositories**
4. Add `https://github.com/vossy74/hacs-mikrotik-router-extended` as **Integration**
5. Install **MikroTik Router Extended**
6. Restart Home Assistant

## Configuration

Add the integration via **Settings → Devices & Services → Add Integration → MikroTik Router**.

| Option | Description |
|---|---|
| Host | IP address of your MikroTik router |
| Port | API port (default: 8728) |
| Username | RouterOS username |
| Password | RouterOS password |
| DHCP Leases | Enable DHCP lease sensors and device tracker |
| DNS | Enable DNS sensors and switches |

## Credits

Original integration by [tomaae](https://github.com/tomaae).
