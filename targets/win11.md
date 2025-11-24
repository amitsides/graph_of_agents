# Windows 11 Network-Facing Services

## Overview
This document identifies **10 high-impact network-facing services** in Windows 11 that present potential security risks if vulnerable.

---

## Network-Facing Services and Ports

| # | Service/Protocol | Port(s) | Default Exposure | Purpose | Risk Profile |
|---|------------------|---------|------------------|---------|--------------|
| 1 | **SMB** | 445/TCP | Local network | File/printer sharing | Lateral movement, ransomware propagation |
| 2 | **RDP** | 3389/TCP | Disabled by default | Remote desktop access | Full system compromise, credential theft |
| 3 | **WinRM** | 5985/TCP (HTTP)<br>5986/TCP (HTTPS) | Local network | PowerShell remote management | Remote code execution |
| 4 | **LSASS** | N/A (Local APIs) | Local only | Credential/token handling | Credential dumping, lateral movement |
| 5 | **WMI/DCOM** | 135/TCP | Local network | System management | Remote execution, persistence |
| 6 | **Print Spooler** | RPC Dynamic | Local network | Print services | Privilege escalation (PrintNightmare) |
| 7 | **RPC Endpoint Mapper** | 135/TCP | Local network | Service discovery | Service enumeration, pivoting |
| 8 | **HTTP.sys** | 80/TCP, 443/TCP | Local network | Kernel-mode web server | Kernel-level RCE |
| 9 | **DNS Client** | 53/UDP | Local network | Name resolution | Cache poisoning, traffic redirection |
| 10 | **Bluetooth/Wi-Fi Stack** | N/A (Wireless) | Device proximity | Wireless connectivity | Proximity-based attacks |

---

## Quick Reference: Port Summary

```
445/TCP     - SMB
3389/TCP    - RDP
5985/TCP    - WinRM (HTTP)
5986/TCP    - WinRM (HTTPS)
135/TCP     - RPC/DCOM/WMI
80/443/TCP  - HTTP.sys
53/UDP      - DNS
```

---

## Notes
- **Local network** = typically not exposed to internet by default
- **RPC Dynamic** = ephemeral port range (49152-65535)
- Services marked "Local only" still pose risk via local exploitation or supply chain attacks

---

## Complete Reference: 50 Windows 11 Services & Associated Ports

### Core Network Services
| # | Service | Port(s) | Protocol | Binding Type |
|---|---------|---------|----------|--------------|
| 1 | RPC Endpoint Mapper | 135 | TCP | Local bind |
| 2 | SMB | 445 | TCP | Local bind |
| 3 | LLMNR | 5355 | UDP | Local bind |
| 4 | mDNS | 5353 | UDP | Local bind |
| 5 | WSDAPI / Web Services Discovery | 5357 | TCP | Local bind |
| 6 | WSDAPI Secure | 5358 | TCP | Local bind |
| 7 | DHCP Client | 68 | UDP | Outbound/Local |
| 8 | DNS Client | 53 | UDP/TCP | Outbound/Local |
| 9 | NTP | 123 | UDP | Outbound/Local |

### Windows Update & Transfer Services
| # | Service | Port(s) | Protocol | Binding Type |
|---|---------|---------|----------|--------------|
| 10 | Windows Update Service | 80 | TCP | Outbound |
| 11 | Windows Update Service | 443 | TCP | Outbound |
| 12 | BITS (Background Intelligent Transfer) | 443 | TCP | Outbound |
| 13 | Delivery Optimization | 7680 | TCP | Local bind |
| 14 | Delivery Optimization Peer Service | 7680 | UDP | Local bind |

### Discovery & UPnP Services
| # | Service | Port(s) | Protocol | Binding Type |
|---|---------|---------|----------|--------------|
| 15 | SSDP Discovery | 1900 | UDP | Local bind |
| 16 | UPnP Device Host | 2869 | TCP | Local bind |
| 17 | SSDP (IPv6) | 1900 | UDP | Local bind |

### VPN & Tunneling Services
| # | Service | Port(s) | Protocol | Binding Type |
|---|---------|---------|----------|--------------|
| 18 | IP Helper / Teredo | 3544 | UDP | Local bind |
| 19 | IP Helper / Teredo IPv6 | 3545 | UDP | Local bind |
| 20 | IKE / IPsec | 500 | UDP | Local bind |
| 21 | IPsec NAT-T | 4500 | UDP | Local bind |
| 22 | L2TP | 1701 | UDP | Local bind |

### Remote Management Services
| # | Service | Port(s) | Protocol | Binding Type |
|---|---------|---------|----------|--------------|
| 23 | WinRM HTTP | 5985 | TCP | Local bind |
| 24 | WinRM HTTPS | 5986 | TCP | Local bind |
| 25 | WMI (DCOM) | 135 | TCP | Local bind |
| 26 | WMI (Dynamic RPC High Ports) | 49152+ | TCP | Dynamic |
| 27 | Event Log Remoting | 5985 | TCP | Local bind |
| 28 | Task Scheduler Remoting | 135 | TCP | Local bind |
| 29 | COM+ Network Access | 135 | TCP | Local bind |
| 30 | Remote Procedure Call Locator | 135 | TCP | Local bind |

### Print & File Services
| # | Service | Port(s) | Protocol | Binding Type |
|---|---------|---------|----------|--------------|
| 31 | Print Spooler (RPC) | 135 | TCP | Local bind |
| 32 | Print Spooler (SMB) | 445 | TCP | Local bind |
| 33 | Remote File System API | 445 | TCP | Local bind |

### Time Services
| # | Service | Port(s) | Protocol | Binding Type |
|---|---------|---------|----------|--------------|
| 34 | Windows Time (W32Time) | 123 | UDP | Outbound/Local |

### Wireless & Proximity Services
| # | Service | Port(s) | Protocol | Binding Type |
|---|---------|---------|----------|--------------|
| 35 | Bluetooth Service | Dynamic | TCP/UDP | Local bind |
| 36 | Wi-Fi Direct Services | 7236 | TCP/UDP | Local bind |
| 37 | Device Association Framework | 50001 | TCP | Local bind |

### Cloud & Microsoft Services
| # | Service | Port(s) | Protocol | Binding Type |
|---|---------|---------|----------|--------------|
| 38 | Clipboard User Service (Cloud Clipboard) | 443 | TCP | Outbound |
| 39 | Web Account Manager | 443 | TCP | Outbound |
| 40 | Windows Push Notification Service | 443 | TCP | Outbound |
| 41 | Microsoft Store | 443 | TCP | Outbound |
| 42 | OneDrive Sync Engine | 443 | TCP | Outbound |
| 43 | Microsoft Account Sign-In | 443 | TCP | Outbound |
| 44 | Credential Manager | 443 | TCP | Outbound |
| 45 | Windows Hello Enrollment | 443 | TCP | Outbound |

### Gaming & Media Services
| # | Service | Port(s) | Protocol | Binding Type |
|---|---------|---------|----------|--------------|
| 46 | Xbox Live Networking Helper | 3074 | TCP/UDP | Local bind |
| 47 | Game Bar Services | 443 | TCP | Outbound |

### HTTP Kernel Services
| # | Service | Port(s) | Protocol | Binding Type |
|---|---------|---------|----------|--------------|
| 48 | HTTP.sys kernel listener | 80 | TCP | Local bind |
| 49 | HTTPS.sys kernel listener | 443 | TCP | Local bind |
| 50 | Edge WebView Runtime | 443 | TCP | Outbound |

---

## Port Categories Summary

### Most Common Inbound Ports (Local Bind)
```
135     - RPC/DCOM/WMI/Task Scheduler/COM+
445     - SMB/Print Spooler/Remote File System
1900    - SSDP/UPnP Discovery
5355    - LLMNR
5353    - mDNS
5357    - WSDAPI
5985    - WinRM HTTP/Event Log Remoting
7680    - Delivery Optimization
```

### Common Outbound Ports
```
53      - DNS
80      - HTTP (Windows Update, HTTP.sys)
123     - NTP/Windows Time
443     - HTTPS (Updates, Store, OneDrive, Cloud Services)
```

### VPN/Tunneling Ports
```
500     - IKE/IPsec
1701    - L2TP
3544    - Teredo
4500    - IPsec NAT-T
```

### Dynamic Port Ranges
```
49152-65535  - RPC Dynamic, WMI High Ports
```