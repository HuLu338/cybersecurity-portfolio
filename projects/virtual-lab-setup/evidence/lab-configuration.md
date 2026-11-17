# Selected lab configuration record

This is a text record of the owned lab configuration, not a screenshot or a newly measured scan.

| Setting | Kali | Metasploitable 2 |
|---|---|---|
| Experimental network | Private LAN Segment `WQE7001-AppSec` | Same private segment |
| VMware adapter type | `pvn` | `pvn` |
| Experimental adapter present | true | true |
| Shared segment identifier | Matched in private configuration review | Matched to Kali |
| Unused second target adapter | Not applicable | present=false; startConnected=false |
| Recorded IPv4 address | `192.168.77.10/24` | `192.168.77.20/24` |

Selected adapter fields were checked again in the local VM configuration files on 17 November 2026. Both active adapters referenced the same private segment identifier. This review did not power on the guests or repeat the network measurements. Raw VM configuration files, segment UUIDs, disk locations and host paths are not published.

The accompanying November guest captures supply the routing and mutual-connectivity evidence. The network type alone does not establish every aspect of isolation.
