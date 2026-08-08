# Web Ôn Thi Trắc Nghiệm Chủ Nghĩa Xã Hội Khoa Học VHU (300 Câu)

Ứng dụng Web tĩnh (HTML5/CSS3/JavaScript) ôn thi trắc nghiệm môn **Chủ nghĩa xã hội khoa học (300 câu)** chuẩn chương trình Trường Đại học Văn Hiến (VHU), thiết kế theo phong cách **Glacier Dark Mode (Mosea Style)**.

---

## 🌟 TÍNH NĂNG NỔI BẬT

1. **Bộ dữ liệu 300 câu hoàn chỉnh**: Được bóc tách từ file `TRAC-NGHIEM-CNXH-300-CA_CC_82U.docx`. Các câu thiếu phương án được bổ sung đáp án nhiễu (distractors) chuẩn kiến thức triết học & CNXHKH Mác - Lênin.
2. **Giao diện Glacier Dark Mode (Mosea Style)**: Tone màu xanh băng/xanh mây hiện đại (`#0b1329`, Sky-500 `#0ea5e9`), Mint Green cho đáp án đúng, Rose Red cho đáp án sai.
3. **Bảng điều hướng nhanh 300 câu (Question Grid)**:
   - Hiển thị trực quan trạng thái từng câu (Chưa làm, Đúng, Sai, Đã chọn).
   - Click chuyển mượt (smooth scroll) tới câu tương ứng.
4. **Chế độ học linh hoạt**:
   - **Luyện tập**: Hiện đáp án ngay, tự động chuyển câu, đọc giải thích.
   - **Thi thử (Exam Mode)**: Đếm ngược thời gian (45 phút), nộp bài chấm điểm %, hiển thị báo cáo chi tiết.
5. **Sổ tay câu sai (LocalStorage)**: Tự động lưu lại các câu làm sai để lọc và cày lại nhanh chóng.

---

## 📂 CẤU TRÚC DỰ ÁN

```text
CHXHKH-VHU/
├── index.html
├── style.css
├── app.js
├── build_data.py
├── README.md
├── TRAC-NGHIEM-CNXH-300-CA_CC_82U.docx
└── data/
    ├── manifest.json
    └── cnxhkh_vhu.json
```

---

## 🚀 HƯỚNG DẪN PUSH LÊN GITHUB & BẬT GITHUB PAGES

### Bước 1: Khởi tạo Git repository (tại thư mục `CHXHKH-VHU/`)
Mở Terminal / PowerShell tại thư mục `CHXHKH-VHU/` và chạy các lệnh:

```bash
git init
git add .
git commit -m "Initial commit: Web On thi CNXHKH VHU 300 cau complete"
```

### Bước 2: Liên kết với GitHub Remote Repo
1. Tạo một repository mới trên GitHub (ví dụ đặt tên: `CHXHKH-VHU`).
2. Chạy các lệnh liên kết và push (thay `YOUR_USERNAME` bằng username GitHub của bạn):

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/CHXHKH-VHU.git
git push -u origin main
```

### Bước 3: Kích hoạt GitHub Pages
1. Vào repository trên GitHub: `https://github.com/YOUR_USERNAME/CHXHKH-VHU`.
2. Chuyển sang thẻ **Settings** -> Chọn mục **Pages** ở menu bên trái.
3. Tại phần **Build and deployment**:
   - **Source**: Chọn `Deploy from a branch`.
   - **Branch**: Chọn `main` và thư mục `/ (root)`.
4. Bấm **Save**. 

Sau 1 - 2 phút, GitHub sẽ cấp cho bạn đường link trang web tĩnh có dạng:  
👉 **`https://YOUR_USERNAME.github.io/CHXHKH-VHU/`**

---

## 💻 CHẠY TRỰC TIẾP TRÊN MÁY TÍNH (LOCAL)

Bạn có thể chạy trực tiếp bằng cách mở file `index.html` trong trình duyệt web (Chrome, Edge, Firefox) hoặc dùng Live Server trong VS Code:

```bash
# Hoặc dùng Python HTTP Server đơn giản:
python -m http.server 8000
```
Sau đó truy cập: `http://localhost:8000`

---
*Phát triển cho sinh viên VHU - Trường Đại học Văn Hiến.*
