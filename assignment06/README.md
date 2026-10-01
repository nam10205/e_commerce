# Assignment 06 - Multimodal E-Commerce Search System

**Sinh viên:** Trần Hải Nam  
**MSSV:** B23DCDT176  
**Lớp:** D23CQCE01-B

Nguyên mẫu tìm kiếm thương mại điện tử theo kiến trúc ba lớp. Bao gồm text search, voice search mô phỏng, tìm ảnh từ đặc trưng pixel, xếp hạng, fusion text + image, lọc giá/danh mục và tìm đơn hàng.

## 1. Môi trường

- Python 3.10 trở lên; đã chạy kiểm tra với Python 3.13.11.
- Gói ngoài duy nhất cho nguyên mẫu: Pillow. Phiên bản đã kiểm tra: 12.3.0.
- Các phần còn lại sử dụng thư viện chuẩn Python.
- Không cần GPU, khóa API, mô hình tải thêm hoặc kết nối Internet khi chạy demo.
- Visual Paradigm 18.1 để mở dự án `.vpp`. Chạy Python không cần Visual Paradigm.

## 2. Cài đặt và chạy

Giải nén gói ZIP, mở terminal trong thư mục `assignment06` (nơi có `main.py`).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Nếu PowerShell chưa cho chạy script kích hoạt, có thể gọi trực tiếp:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

Trên macOS/Linux, dùng `python3 -m venv .venv` và `source .venv/bin/activate`.

`python main.py` chạy bốn minh họa text, voice, image và multimodal; sau đó minh họa tìm đơn hàng. Kết quả chi tiết được ghi ở `demo/demo_results.json`.

## 3. Lệnh minh họa

```powershell
python main.py --mode text --query "black shoes"
python main.py --mode voice --query "find running shoes"
python main.py --mode image --image data/dataset/images/query_black_shoe.png
python main.py --mode multimodal --query "black shoes" --image data/dataset/images/query_black_shoe.png
python main.py --mode text --query "find Nike shoes under 100 dollars"
python main.py --mode text --query "black" --category shoes --max-price 100 --top-k 3
python main.py --mode order --query "find my order 20261001" --customer C001
python main.py --mode order --query "where is my latest order" --customer C001
python main.py --mode order --query "order O002" --customer C001
python main.py --mode product --product-id 5
```

Lệnh tra O002 dưới C001 trả `null` vì đơn thuộc C002. `--mode product` cho xem chi tiết sản phẩm; mã không tồn tại trả `null`.

Giọng nói là **mô phỏng bằng transcript**, không thu âm hay nhận dạng microphone. Với tìm ảnh, CLI nhận đường dẫn ảnh người dùng bất kỳ mà Pillow đọc được. Ảnh không có foreground, file lỗi hoặc thiếu file sẽ bị từ chối.

## 4. Giao diện web cục bộ

```powershell
python web.py
```

Mở http://127.0.0.1:8765 rồi chọn mode, nhập truy vấn và bấm Search. Giao diện gọi mã Python thực; chỉ lắng nghe trên máy cục bộ. Nhấn Ctrl+C ở terminal để dừng.

Web demo dùng sẵn `query_black_shoe.png` cho chế độ image/multimodal, và dùng khách hàng C001 cho tìm đơn. Muốn thử ảnh khác hoặc khách hàng khác, dùng CLI. Giao diện này không có chức năng thu âm hoặc tải ảnh từ trình duyệt.

## 5. Kiểm thử và đánh giá

```powershell
python -m unittest discover -s tests -v
python evaluate.py
```

- 13/13 kiểm thử chức năng đạt: text/voice, price/category filters, ảnh, trọng số, tồn kho, top-k và phạm vi đơn hàng.
- 12 truy vấn đánh giá với nhãn khai báo trước: 10 thành công, 2 thất bại; **83.33%**.
- Ca thất bại: `sneekers` (chính tả/từ đồng nghĩa) và `not black shoes` (phủ định).
- Đây là đánh giá chức năng trên dữ liệu giả lập nhỏ, không phải độ chính xác tổng quát.
- Một kết quả rỗng đúng với truy vấn không có sản phẩm được tính là thành công.
- `demo/timing.json` ghi 100 lượt truy vấn text sau khởi tạo; không tính thời gian mã hóa ảnh ban đầu hay giao diện web.

## 6. Cấu trúc dự án

```text
assignment06/
  main.py                    Điểm lắp ghép phụ thuộc và CLI
  web.py                     Điểm khởi động web
  evaluate.py                Bộ 12 truy vấn có nhãn
  requirements.txt
  presentation/
    search_ui.py             SearchUI, VoiceInput, ImageUpload, SearchResultView
    web_ui.py                WebHandler dùng SearchUI được truyền vào
  application/
    query_service.py         CommonQuery, chuẩn hóa, bộ lọc, trọng số
    speech_service.py        Speech-to-text mô phỏng
    image_service.py         Bộ mô tả pixel 64 chiều
    search_service.py        Truy hồi và lọc, tra sản phẩm/đơn hàng
    ranking_service.py       Điểm tổng hợp và Top-k
  data/
    product_repository.py    Đọc dữ liệu sản phẩm
    order_repository.py      Tra đơn trong phạm vi khách hàng
    vector_index.py          Cosine và chỉ mục vector trong RAM
    dataset/
      products.json          12 sản phẩm
      orders.json            3 đơn hàng và dòng hàng
      images/                12 ảnh sản phẩm + 1 ảnh truy vấn
  tests/test_system.py
  demo/                      Kết quả, ảnh chụp màn hình, đánh giá, kiểm chứng UML
  uml/
    assignment06_multimodal_search_final.vpp
    01_use_case.png
    02_architecture.png
    03_voice_sequence.png
    api_builder/             Mã Java và manifest tạo UML qua Open API
  report/
    Bao_cao_Assignment06_Tran_Hai_Nam.pdf
    Bao_cao_Assignment06_Tran_Hai_Nam_EDITABLE_DRAFT.docx
    Noi_dung_bao_cao.md       Nội dung báo cáo có thể chỉnh sửa
```

## 7. Cách hoạt động

Text và voice được chuẩn hóa thành token. Điểm text là số token khớp / số token truy vấn; truy hồi giữ sản phẩm có ít nhất một token khớp. Các kết quả liên quan một phần vẫn có thể xuất hiện sau kết quả khớp đầy đủ.

Ảnh được đưa về khung RGB 64×64, chia 4×4 ô. Mỗi ô có ba trung bình màu nghịch đảo và tỷ lệ foreground; kết quả là vector 64 chiều. Đây là đặc trưng thực tính từ ảnh, **không phải embedding học sâu**. Cosine đo sự gần nhau của đặc trưng.

```text
relevance = w_text * text_score + w_image * image_score
score = 0.95 * relevance + 0.05 * in_stock
```

Text/voice: trọng số `(1, 0)`; image: `(0, 1)`; multimodal: `(0.5, 0.5)`. Fusion kết hợp điểm, không cộng các vector ở những không gian khác nhau. Khi bằng điểm, ưu tiên giá thấp hơn rồi ID nhỏ hơn. `under 100` và `--max-price 100` đều nghĩa là **giá < 100**.

`main.py` tạo repository, mã hóa ảnh và truyền dịch vụ vào UI. Presentation không truy cập trực tiếp JSON/database. Retrieval và ranking được tách thành `SearchService.retrieve()` và `RankingService.rank()`.

## 8. Visual Paradigm và nội dung nộp

Mở `uml/assignment06_multimodal_search_final.vpp` bằng Visual Paradigm. Dự án có ba sơ đồ UML thực, có thể chỉnh sửa: Use Case, Component và Voice Sequence. Đã kiểm chứng mở lại qua Open API; kết quả nằm ở `demo/uml_verification.json`.

Mã tạo UML dùng `VPPlugin` và `VPPluginCommandLineSupport`, không phải file ảnh giả đổi đuôi `.vpp`. Các ảnh PNG được xuất trực tiếp từ dự án và có watermark bản dùng thử; watermark được giữ nguyên. `uml/api_builder` cung cấp mã Java để tham khảo; không cần cài plugin này khi chỉ mở `.vpp`.

Bài làm không kèm dữ liệu cấu hình hoặc thông tin giấy phép Visual Paradigm. Nếu muốn xuất sơ đồ theo cấu hình giấy phép của máy khác, mở `.vpp` trong môi trường đó rồi xuất ảnh bằng chức năng thông thường của Visual Paradigm.

## 9. Giới hạn

- Voice chỉ là transcript; chưa có speech recognition thật.
- Ảnh tự tạo có nền trắng, đơn giản; các ảnh giày đen 01 và 05 giống nhau nên không thể phân biệt thương hiệu bằng ảnh.
- Ảnh truy vấn là bản thu nhỏ từ ảnh sản phẩm 05; đây là ca kiểm tra pipeline, chưa phải kiểm tra tổng quát hóa trên ảnh độc lập.
- Chưa có sửa chính tả, hiểu phủ định hoặc tìm kiếm ngữ nghĩa.
- Bộ lọc thương hiệu không phải bộ lọc cứng; thương hiệu được dùng trong điểm khớp từ khóa.
- Phạm vi đơn hàng được kiểm tra bằng customer_id truyền vào; chưa có xác thực nên không phải mô hình bảo mật sản xuất.
- JSON và chỉ mục RAM phù hợp bài học nhỏ, chưa có cập nhật giao dịch hay cơ sở dữ liệu vector.
- Các điểm và tỷ lệ thành công không đại diện cho dữ liệu thương mại điện tử thật.

## 10. Tài liệu

- Đề Assignment 06 do người học cung cấp.
- [Visual Paradigm Plug-in API](https://www.visual-paradigm.com/support/documents/pluginapi.jsp)
- [Running plug-in silently](https://circle.visual-paradigm.com/docs/open-api/running-plug-in/running-visual-paradigm-plug-in-silently/)

Đề có một số đoạn ghi Assignment 05, nhưng gói này theo tiêu đề Assignment 06 và các Task 1-6 ở cuối đề.

## Screenshots and editable English report

Reopen `uml/assignment06_multimodal_search_final.vpp` before taking screenshots.
This final project contains the corrected reference layout with 12 use cases,
6 includes, 2 extends, and cyan shapes in all three diagrams.
See `SCREENSHOTS.txt` for the diagram names and how to replace Figures 1-3
in the plain English Word report. The supplied PNGs and PDF currently
contain native VP exports with the evaluation watermark.
