import datetime as dt
import json
import pathlib
import re
import time
import urllib.request
import urllib.parse

GROUPS = {
    "OS & Kernel": ["linux kernel", "linux_kernel", "ubuntu", "debian", "red hat", "rhel", "rocky linux", "almalinux", "windows server", "systemd", "glibc", "sudo"],
    "Web & Proxy": ["nginx", "apache http", "http_server", "haproxy", "traefik", "tomcat", "php", "openssl", "curl"],
    "Cloud & Virtualization": ["proxmox", "cloudstack", "openstack", "qemu", "libvirt", "vmware", "esxi", "vcenter", "xen", "hyper-v"],
    "Storage & Database": ["ceph", "zfs", "samba", "nfs", "postgresql", "mysql", "mariadb", "redis", "mongodb", "minio"],
    "Container & DevOps": ["kubernetes", "docker", "containerd", "runc", "rancher", "rke2", "jenkins", "gitlab", "ansible", "terraform", "helm", "prometheus", "grafana"],
    "Network & Security": ["openssh", "bind", "bind9", "unbound", "dnsmasq", "pfsense", "opnsense", "routeros", "fortios", "fortigate", "pan-os", "frrouting", "openvpn", "wireguard", "strongswan", "cisco", "chrony"],
    "Mail & Hosting": ["zimbra", "mailcow", "postfix", "dovecot", "exim", "roundcube", "cpanel", "directadmin", "plesk", "sendmail", "asterisk", "freepbx"]
}
def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"SysAdmin-CVE-Watch"}), timeout=90) as r:
                return json.load(r)
        except Exception:
            if i == 3:
                raise
            time.sleep(15*(i+1))

def matches(c):
    def walk(obj):
        if isinstance(obj, dict):
            if obj.get("vulnerable") is True and "criteria" in obj:
                yield obj
            for v in obj.values():
                yield from walk(v)
        elif isinstance(obj, list):
            for v in obj:
                yield from walk(v)
    return list(walk(c.get("configurations", [])))

def classify(description, cpes):
    products = []
    for group, names in GROUPS.items():
        for name in names:
            pattern = r"(?<![\w])" + re.escape(name).replace("_", "[_ -]") + r"(?![\w])"
            hits = [m for m in cpes if re.search(pattern, m["criteria"].split(":",5)[4].replace("_"," "), re.I) or re.search(pattern, m["criteria"].split(":",5)[3].replace("_"," "), re.I)]
            if hits or re.search(pattern, description, re.I):
                label = {"linux_kernel":"Linux kernel","linux kernel":"Linux kernel","http_server":"Apache HTTP Server","apache http":"Apache HTTP Server"}.get(name,name)
                if not any(p["name"] == label for p in products):
                    products.append({"name":label,"group":group,"basis":"CPE" if hits else "keyword"})
    return products

def main():
    now=dt.datetime.now(dt.timezone.utc)
    kev={v["cveID"]:v for v in get("https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json")["vulnerabilities"]}
    params={"lastModStartDate":(now-dt.timedelta(days=14)).isoformat(timespec="milliseconds"),"lastModEndDate":now.isoformat(timespec="milliseconds"),"resultsPerPage":2000}
    items=[]
    start=0
    while True:
        params["startIndex"]=start
        d=get("https://services.nvd.nist.gov/rest/json/cves/2.0?"+urllib.parse.urlencode(params))
        for v in d["vulnerabilities"]:
            c=v["cve"]
            if c.get("vulnStatus")=="Rejected": continue
            desc=next((x["value"] for x in c["descriptions"] if x["lang"]=="en"),"No description")
            cpes=matches(c)
            products=classify(desc,cpes)
            if not products: continue
            metrics=c.get("metrics",{})
            m=next((next((x for x in metrics[k] if x.get("type")=="Primary"),metrics[k][0]) for k in ("cvssMetricV40","cvssMetricV31","cvssMetricV30","cvssMetricV2") if metrics.get(k)),{})
            cv=m.get("cvssData",{})
            k=kev.get(c["id"])
            items.append({"id":c["id"],"description":desc,"products":products,"affected":cpes,"published":c["published"],"modified":c["lastModified"],"score":cv.get("baseScore"),"severity":cv.get("baseSeverity",m.get("baseSeverity","UNKNOWN")),"vector":cv.get("vectorString"),"cvssVersion":cv.get("version"),"status":c.get("vulnStatus"),"kev":bool(k),"action":k.get("requiredAction") if k else None,"due":k.get("dueDate") if k else None,"references":c.get("references",[])})
        start+=len(d["vulnerabilities"])
        if start>=d["totalResults"]: break
        if not d["vulnerabilities"]: raise RuntimeError("Incomplete NVD response")
        time.sleep(6)
    path=pathlib.Path("data/cve.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps({"schema":2,"updated":now.isoformat(),"items":items},ensure_ascii=False),encoding="utf-8")
if __name__=="__main__":
    main()
