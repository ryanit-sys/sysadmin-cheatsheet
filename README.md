# SysAdmin & DevOps Cheatsheet

A quick-reference collection of Linux, system administration, networking, and DevOps commands for day-to-day infrastructure operations and troubleshooting.

**Website:** https://ryanit-sys.github.io/sysadmin-cheatsheet/

## Features

- Search by command name, content, or description, with accent-insensitive Vietnamese search.
- Copy commands with a single click.
- Browse commands by tool, with explanations and practical notes.
- Dark mode and a responsive layout for desktop and mobile.
- Static website with no backend or external library dependencies.

## Categories

| Category | Content | Status |
| --- | --- | --- |
| Search Commands | grep, find, awk, sed, cut, sort, uniq, xargs, journalctl | 30 commands |
| Linux | System, processes, storage, memory | Planned |
| Networking | Open vSwitch QoS, HTB, ingress policing, verification, and rollback | 10 entries |
| Ceph | Cluster, OSD, PG, health | Planned |
| Proxmox | VMs, cluster, storage, SDN | Planned |
| Docker | Containers, images, networking | Planned |
| Kubernetes | Pods, deployments, services | Planned |
| Services | Nginx, Apache, databases | Planned |
| CVE Watch | Infrastructure CVEs, CVSS, KEV, advisories | Implemented |

## Usage

1. Open the website and select a category.
2. Enter a search keyword or select a tool group.
3. Read the description, click **Copy**, and adjust the parameters before executing the command.

Example: extract Nginx build arguments containing a specific module version:

~~~bash
nginx -V 2>&1 | grep -oE '[^[:space:]]*0\.0\.20rc4[^[:space:]]*'
~~~

## Architecture and Deployment

The website uses plain HTML, CSS, and JavaScript. Command data and rendering logic are stored in index.html.

~~~text
sysadmin-cheatsheet/
├── index.html
├── cve.html
├── data/
│   └── cve.json
├── scripts/
│   └── update_cve.py
├── .github/
│   └── workflows/
│       └── cve.yml
└── README.md
~~~

Run locally:

~~~bash
git clone https://github.com/ryanit-sys/sysadmin-cheatsheet.git
cd sysadmin-cheatsheet
python3 -m http.server 8000
~~~

Open http://localhost:8000.

For GitHub Pages deployment, navigate to **Settings → Pages → Deploy from a branch**, select **main** and **/ (root)**. Monitor deployment status in the Actions tab.

## Adding Commands

Add an entry to the commands array in index.html:

~~~javascript
["grep", "Find errors in logs", "grep -in 'error' application.log", "Show line numbers and ignore case."]
~~~

The fields represent the tool group, title, command, and description, respectively. The Networking category uses the networkingCommands array with the same structure. Placeholder tabs require additional data and rendering logic when new content is introduced.

## Open vSwitch Rate Limiting

The **Networking → Open vSwitch** section contains 10 entries covering configuration, verification, and rollback.

- Egress: Linux HTB QoS/Queue; 40 Mbps = 40,000,000 bit/s.
- Ingress: policing; 40 Mbps = 40,000 kbit/s, with an example burst of 4,000 kbit. Unlike shaping, policing drops packets that exceed the configured limits.
- Traffic direction is relative to the OVS port/interface, not necessarily the VM's upload or download direction.
- Verify configuration using ovs-vsctl, ovs-appctl, tc, and bidirectional iperf3 tests.
- Replace the example port fwln9990o0 with the actual port. Inspect existing QoS before overwriting it.
- Rollback: disable policing, record UUIDs, clear the Port qos reference, and destroy QoS/Queue records by UUID only after confirming they are no longer referenced. Do not substitute a port name for a UUID or delete all QoS/Queue records on the host.
- The HTB creation command creates new records each time it runs. Manage obsolete records to avoid accumulation. A datapath supporting Linux HTB is required.

## System CVE Watch

**Dashboard:** https://ryanit-sys.github.io/sysadmin-cheatsheet/cve.html

- Focuses on operating systems and kernels, web servers and proxies, cloud and virtualization, storage and databases, containers and DevOps, networking and security, and mail and hosting.
- Highlights service names, Critical/High/KEV statistics, search, category/service/severity filters, and sorting by risk or update date.
- CVE details include original English descriptions, CVSS scores and vectors, CPE and version constraints, publication and modification dates, advisories, and CISA required actions where available.
- Data sources: NVD API 2.0 and CISA KEV. Coverage is limited to CVEs modified within the last 14 days, not the complete historical CVE database.
- Classification uses CPE and description keywords. A question mark (?) indicates an unconfirmed keyword match. The watchlist does not cover every product. CPE information is abbreviated; consult NVD and vendor advisories for complete applicability conditions.
- GitHub Actions runs daily at 00:00 UTC (07:00 ICT) and supports manual execution. Data older than 36 hours triggers a warning. No API key is required; retries and pagination are supported.
- scripts/update_cve.py: collector and product watchlist; data/cve.json: generated data; cve.html: dashboard; .github/workflows/cve.yml: scheduled updates.
- To run locally, execute python3 scripts/update_cve.py, then python3 -m http.server 8000.

## Maintenance

Keep the README aligned with code and feature changes. Use descriptive commit messages, test changes before committing, and verify workflows and deployment. The maintainer authorizes direct commits for requested updates without additional confirmation.

## Important Notes

Examples primarily target GNU/Linux. Verify permissions, tool versions, paths, and parameters before running commands in production. Never publish passwords, tokens, or internal infrastructure information in this public repository.

## Maintainer

[ryanit-sys](https://github.com/ryanit-sys)
