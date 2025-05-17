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

Dự án **8-Puzzle Solver with AI Algorithms** nhằm phát triển và so sánh đa dạng các thuật toán trí tuệ nhân tạo để giải bài toán 8-puzzle, một bài toán kinh điển trong AI. Mục tiêu bao gồm:

- Triển khai các thuật toán tìm kiếm đa dạng như tìm kiếm không thông tin, có thông tin, cục bộ, trong môi trường phức tạp, có ràng buộc và học tăng cường.
- Phân tích và so sánh hiệu suất các thuật toán qua các tiêu chí như thời gian chạy, bộ nhớ sử dụng, số bước và tính tối ưu của lời giải.
- Xây dựng giao diện đồ họa trực quan giúp người dùng quan sát quá trình giải và so sánh hiệu quả thuật toán.

---

## 2. Nội dung dự án

### 2.1. Bài toán 8-puzzle

Bàn cờ 3x3 với 8 ô số (1-8) và 1 ô trống. Mục tiêu sắp xếp các ô theo thứ tự từ 1 đến 8 với ô trống cuối cùng.

- **Trạng thái:** Cấu hình hiện tại của các ô.
- **Hành động:** Di chuyển ô trống sang các vị trí hợp lệ.
- **Hàm heuristic:** Ước lượng khoảng cách đến mục tiêu, hỗ trợ thuật toán tìm kiếm có thông tin.

### 2.2. Nhóm thuật toán

- **Tìm kiếm không thông tin:** BFS, DFS, UCS, IDS.
- **Tìm kiếm có thông tin:** Greedy Best-First Search, A*, IDA*.
- **Tìm kiếm cục bộ:** Hill Climbing (các biến thể), Simulated Annealing, Genetic Search, Beam Search.
- **Tìm kiếm môi trường phức tạp:** AND-OR Search, Partially Observable Search, No Observation Search.
- **Tìm kiếm có ràng buộc:** Constraint Testing, Backtracking CSP, Backtracking AC-3.
- **Học tăng cường:** Q-Learning.

### 2.3. Trực quan hóa

- GUI hiển thị trạng thái bài toán, quá trình giải, và các chỉ số hiệu suất.
- Hình ảnh động minh họa quá trình giải từng thuật toán.

---

## 3. Thuật toán

(Phần này mô tả chi tiết các thuật toán, bạn có thể thêm nội dung từng thuật toán hoặc liên kết đến file riêng)

---

## 4. Cách sử dụng

1. Cài đặt môi trường Python:
   ```bash
   pip install -r requirements.txt
