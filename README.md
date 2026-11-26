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
| Networking | IP, routing, DNS | Kế hoạch |
| Ceph | Cluster, OSD, PG, health | Kế hoạch |
| Proxmox | VM, cluster, storage, SDN | Kế hoạch |
| Docker | Container, image, network | Kế hoạch |
| Kubernetes | Pod, deployment, service | Kế hoạch |
| Services | Nginx, Apache, database | Kế hoạch |

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

Các trường lần lượt là nhóm công cụ, tiêu đề, câu lệnh và mô tả. Các tab dự phòng cần bổ sung dữ liệu và logic hiển thị khi triển khai nội dung mới.

## Lưu ý

Ví dụ chủ yếu dành cho GNU/Linux. Kiểm tra quyền, phiên bản công cụ, đường dẫn và tham số trước khi chạy trên production. Không đưa mật khẩu, token hoặc thông tin nội bộ lên repository public.

## Maintainer

[ryanit-sys](https://github.com/ryanit-sys)
