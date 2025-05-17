# 8-Puzzle Solver with AI Algorithms

## Mục lục
1. [Mục tiêu dự án](#1-mục-tiêu-dự-án)  
2. [Nội dung dự án](#2-nội-dung-dự-án)  
3. [Thuật toán](#3-thuật-toán)  
4. [Cách sử dụng](#4-cách-sử-dụng)  
5. [Trực quan hóa](#5-trực-quan-hóa)  
6. [So sánh hiệu suất](#6-so-sánh-hiệu-suất)  
7. [Kết luận](#7-kết-luận)  
8. [Tác giả](#8-tác-giả)  

---

## 1. Mục tiêu dự án

Dự án 8-Puzzle Solver with AI Algorithms hướng đến việc triển khai và so sánh đa dạng các thuật toán trí tuệ nhân tạo nhằm giải quyết bài toán 8-puzzle - một bài toán kinh điển trong lĩnh vực AI và khoa học máy tính.

- Cụ thể:

Triển khai các thuật toán AI đa dạng: Tích hợp các nhóm thuật toán tìm kiếm khác nhau bao gồm tìm kiếm không thông tin, tìm kiếm có thông tin, tìm kiếm cục bộ, tìm kiếm trong môi trường phức tạp, tìm kiếm có ràng buộc, và học tăng cường. Việc này giúp người dùng hiểu sâu sắc cơ chế hoạt động và sự khác biệt giữa các phương pháp trong cùng một bài toán cụ thể.

Phân tích và so sánh hiệu suất: Đánh giá chi tiết các thuật toán dựa trên các tiêu chí quan trọng như thời gian chạy thực tế, bộ nhớ sử dụng, số bước giải thuật thực hiện, và tính tối ưu của lời giải (chuỗi di chuyển ít bước nhất hoặc chi phí thấp nhất). Kết quả so sánh sẽ làm rõ ưu, nhược điểm cũng như hiệu quả ứng dụng thực tiễn của từng thuật toán.

Trực quan hóa kết quả: Xây dựng giao diện đồ họa (GUI) tương tác, thể hiện trực quan quá trình giải bài toán 8-puzzle qua từng bước, giúp người dùng dễ dàng quan sát, so sánh và đánh giá cách thức vận hành cũng như hiệu quả của từng thuật toán thông qua các hoạt ảnh (GIF), biểu đồ hiệu suất và các chỉ số đo lường.

---

## 2. Nội dung dự án

Dự án bao gồm triển khai và trình bày toàn diện bài toán 8-puzzle dưới dạng một hệ thống giải thuật AI đa thuật toán với các thành phần và đặc điểm sau:

### 2.1 Bài toán 8-puzzle
**Mô tả:** Bàn cờ gồm 9 ô (8 ô có số từ 1 đến 8 và 1 ô trống). Mục tiêu là sắp xếp các ô số theo thứ tự từ 1 đến 8, sao cho ô trống nằm cuối cùng (trạng thái mục tiêu).

**Thành phần bài toán:**

Trạng thái: Cấu hình của các ô trên bàn cờ.

Hành động: Di chuyển ô trống sang trái, phải, lên, hoặc xuống (nếu hợp lệ).

Kiểm tra mục tiêu: So sánh trạng thái hiện tại với trạng thái mục tiêu.

Hàm heuristic (nếu có): Ước lượng khoảng cách từ trạng thái hiện tại đến mục tiêu (ví dụ số ô sai vị trí, khoảng cách Manhattan).


### 2.2 Nhóm thuật toán triển khai
*Tìm kiếm không thông tin (Uninformed Search):*

Bao gồm BFS, DFS, UCS, và IDS - các thuật toán duyệt trạng thái mà không dựa vào thông tin heuristic. Phù hợp với bài toán nhỏ, đảm bảo tính đầy đủ và tối ưu trong một số trường hợp.

*Tìm kiếm có thông tin (Informed Search):*

Bao gồm Greedy Best-First Search, A*, và IDA* - tận dụng thông tin heuristic để tăng tốc độ tìm kiếm và nâng cao chất lượng lời giải.

*Tìm kiếm cục bộ (Local Search):*

Bao gồm các phương pháp Hill Climbing (đơn giản, steepest-ascent, stochastic), Simulated Annealing, Genetic Search, và Beam Search. Các thuật toán này ưu tiên cải thiện trạng thái hiện tại theo hướng tối ưu cục bộ, thích hợp với không gian trạng thái lớn.

*Tìm kiếm trong môi trường phức tạp (Complex Environment Search):*

Triển khai các thuật toán xử lý môi trường không chắc chắn như AND-OR Search, Partially Observable Search, và No Observation Search, cho phép giải quyết bài toán trong điều kiện quan sát thiếu hoặc hành động không chắc chắn.

*Tìm kiếm có điều kiện ràng buộc (Constraint Satisfaction Problem):*

Bao gồm Constraint Testing, Backtracking CSP, và Backtracking AC-3, tập trung xử lý các ràng buộc phức tạp trong bài toán, giúp thu hẹp không gian tìm kiếm hiệu quả.

*Học tăng cường (Reinforcement Learning):*

Ứng dụng Q-Learning để học từ kinh nghiệm và tối ưu chính sách giải quyết bài toán mà không cần mô hình môi trường chính xác.

### 2.3 Tích hợp trực quan hóa (Visualization)
*Giao diện GUI:*

Hiển thị rõ ràng trạng thái ban đầu, quá trình chuyển đổi qua từng bước hành động và trạng thái mục tiêu.

Hiển thị đồ họa bàn cờ với các ô số và ô trống động, cập nhật theo từng bước.

Các chỉ số hiệu suất trực quan như thời gian chạy, số bước đã thực hiện, số trạng thái đã duyệt, hiển thị kèm.

*GIF minh họa:*

Tạo các hình ảnh động minh họa quá trình giải theo từng thuật toán, giúp người dùng dễ dàng so sánh trực quan cách thuật toán vận hành.

### 2.4 So sánh hiệu suất và nhận xét
*Bảng so sánh:*

Thời gian thực thi trên cùng bộ dữ liệu đầu vào.

Số bước tìm được (độ dài chuỗi di chuyển).

Số trạng thái duyệt (độ lớn không gian tìm kiếm).

*Nhận xét chi tiết:*

Đánh giá ưu, nhược điểm của từng thuật toán dựa trên kết quả thực nghiệm.

Phân tích khả năng mở rộng, hiệu quả ứng dụng thực tế trong các trường hợp khác nhau (ví dụ không gian trạng thái lớn, môi trường không chắc chắn).

Gợi ý thuật toán phù hợp với các tình huống khác nhau trong thực tiễn.

---

## 3. Thuật toán

(Phần này mô tả chi tiết các thuật toán, bạn có thể thêm nội dung từng thuật toán hoặc liên kết đến file riêng)

---

## 4. Cách sử dụng

1. Cài đặt môi trường Python:
   ```bash
   pip install -r requirements.txt
