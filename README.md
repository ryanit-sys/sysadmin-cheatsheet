# SysAdmin & DevOps Cheatsheet

Kho tài liệu tra cứu nhanh câu lệnh Linux, System Administration, Networking và DevOps phục vụ vận hành hệ thống và troubleshooting hằng ngày.

**Website:** https://ryanit-sys.github.io/sysadmin-cheatsheet/

## Tính năng

- Tìm kiếm theo tên, nội dung và mô tả câu lệnh, hỗ trợ tiếng Việt không dấu.
- Copy câu lệnh với một thao tác.
- Phân loại theo công cụ, kèm giải thích và lưu ý thực tế.
- Dark Mode, giao diện responsive cho desktop và mobile.
- Static website, không cần backend hay thư viện bên ngoài.

## Danh mục

| Danh mục | Nội dung | Trạng thái |
| --- | --- | --- |
| Search Commands | grep, find, awk, sed, cut, sort, uniq, xargs, journalctl | 30 câu lệnh |
| Linux | System, process, storage, memory | Kế hoạch |
| Networking | Open vSwitch QoS, HTB, ingress policing, kiểm tra và rollback | 10 câu lệnh |
| Ceph | Cluster, OSD, PG, health | Kế hoạch |
| Proxmox | VM, cluster, storage, SDN | Kế hoạch |
| Docker | Container, image, network | Kế hoạch |
| Kubernetes | Pod, deployment, service | Kế hoạch |
| Services | Nginx, Apache, database | Kế hoạch |
| CVE Watch | CVE hạ tầng, CVSS, KEV, advisory | Đã triển khai mã nguồn |

## Cách sử dụng

1. Truy cập website và chọn danh mục.
2. Nhập từ khóa hoặc chọn nhóm công cụ.
3. Đọc mô tả, nhấn **Copy** và điều chỉnh tham số trước khi chạy.

Ví dụ: lọc tham số build Nginx chứa phiên bản module:

```bash
nginx -V 2>&1 | grep -oE '[^[:space:]]*0\.0\.20rc4[^[:space:]]*'
```

## Kiến trúc và triển khai

HTML, CSS và JavaScript thuần; dữ liệu và logic hiển thị hiện nằm trong `index.html`.

```text
sysadmin-cheatsheet/
├── index.html
└── README.md
```

Chạy thử local:

```bash
git clone https://github.com/ryanit-sys/sysadmin-cheatsheet.git
cd sysadmin-cheatsheet
python3 -m http.server 8000
```

Truy cập http://localhost:8000.

GitHub Pages: **Settings → Pages → Deploy from a branch → main → / (root)**. Theo dõi deployment tại tab Actions.

## Bổ sung câu lệnh

Thêm mục vào mảng `commands` trong `index.html`:

```javascript
["grep", "Tìm lỗi trong log", "grep -in 'error' application.log", "Hiển thị số dòng, không phân biệt hoa thường."]
```

Các trường lần lượt là nhóm công cụ, tiêu đề, câu lệnh và mô tả. Networking sử dụng mảng `networkingCommands` cùng cấu trúc. Các tab dự phòng cần bổ sung dữ liệu và logic hiển thị khi triển khai nội dung mới.

## Open vSwitch Rate Limit

Tab **Networking → Open vSwitch** có 10 mục cấu hình, kiểm tra và rollback.

- Egress: Linux HTB QoS/Queue, 40 Mbps = 40000000 bit/s.
- Ingress: policing, 40 Mbps = 40000 kbit/s; burst ví dụ 4000 kbit. Policing drop gói vượt ngưỡng, khác với shaping.
- Chiều traffic được xác định theo port/interface OVS, không mặc định theo chiều upload/download của VM.
- Kiểm tra bằng ovs-vsctl, ovs-appctl, tc và iperf3 hai chiều.
- Port fwln9990o0 là ví dụ; thay bằng port thực tế. Kiểm tra QoS hiện hữu trước khi ghi đè.
- Rollback: tắt policing, lưu UUID, clear Port qos, chỉ destroy QoS/Queue bằng UUID khi không còn tham chiếu. Không dùng tên port thay UUID, không xóa toàn bộ QoS/Queue trên host.
- Lệnh HTB tạo bản ghi mới mỗi lần chạy; cần quản lý bản ghi cũ để tránh tích tụ. Yêu cầu datapath hỗ trợ Linux HTB.

## System CVE Watch

Trang: https://ryanit-sys.github.io/sysadmin-cheatsheet/cve.html

- Ưu tiên OS/kernel, web/proxy, cloud/virtualization, storage/database, container/DevOps, network/security, mail/hosting.
- Tên service nổi bật, thống kê Critical/High/KEV, tìm kiếm, lọc theo nhóm/service/mức độ, sắp xếp theo rủi ro hoặc ngày cập nhật.
- Chi tiết CVE: mô tả gốc tiếng Anh, CVSS/vector, CPE và giới hạn phiên bản, ngày công bố/cập nhật, advisory và hành động CISA nếu có.
- Nguồn NVD API 2.0 và CISA KEV. Phạm vi CVE được sửa đổi trong 14 ngày gần nhất, không phải toàn bộ CVE lịch sử.
- Phân loại theo CPE và từ khóa trong mô tả; dấu (?) là kết quả từ khóa chưa xác nhận. Danh sách theo dõi không bao phủ mọi sản phẩm. CPE hiển thị dạng rút gọn, cần kiểm tra điều kiện đầy đủ tại NVD và advisory vendor.
- GitHub Actions chạy lúc 00:00 UTC (07:00 ICT) mỗi ngày hoặc chạy thủ công. Dữ liệu quá 36 giờ được cảnh báo. Không cần API key; có retry và phân trang.
- `scripts/update_cve.py`: collector và danh sách sản phẩm theo dõi; `data/cve.json`: dữ liệu sinh tự động; `cve.html`: giao diện; `.github/workflows/cve.yml`: lịch cập nhật.
- Chạy local: `python3 scripts/update_cve.py`, sau đó `python3 -m http.server 8000`.

## Changelog

- 2026-11-26: Bổ sung 10 mục Open vSwitch Rate Limit vào Networking, hỗ trợ tìm kiếm, copy, kiểm tra và rollback.

- 2026-11-26: CVE Watch, dashboard ưu tiên service, phân loại hạ tầng, bổ sung thông tin phiên bản và advisory, lịch cập nhật hằng ngày.

## Quy trình bảo trì

Mỗi thay đổi mã nguồn hoặc tính năng phải cập nhật README và changelog tương ứng, commit mô tả rõ ràng, kiểm tra workflow và deployment. Maintainer cho phép tự commit các cập nhật được yêu cầu, không cần xác nhận lại.

## Lưu ý

Ví dụ chủ yếu dành cho GNU/Linux. Kiểm tra quyền, phiên bản công cụ, đường dẫn và tham số trước khi chạy trên production. Không đưa mật khẩu, token hoặc thông tin nội bộ lên repository public.

## Maintainer

[ryanit-sys](https://github.com/ryanit-sys)
