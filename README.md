Kịch bản
========

>   Client:

-   Gửi thông tin yêu cầu: tên chuyến, loại vé, số lượng.

>   Server:

-   Lấy yêu cầu xử lý từ client 1 trong hàng đợi

-   Xử lý yêu cầu của client 1:

    -   Trả về giá tiền thanh toán nếu thông tin hợp lệ

    -   Trả về mã lỗi tương ứng khi thông tin không hợp lệ.

>   Client:

-   Xác nhận và in ra tiền thanh toán.

-   Xác nhận kết thúc và đóng kết nối.

>   Server:

-   Xử lý yêu cầu tiếp theo trong hàng đợi.

Thuật toán
==========

>   Ngôn ngữ lập trình: Python.

Client:
-------

>   Bước 1: Tạo socket mới

-   Hàm thực hiện: createSocket()

>   Bước 2: Kết nối socket với server

-   connectSocket(mySocket, host, port)

>   Bước 3: Giao tiếp với server (gửi và nhận các gói dữ liệu giữa client và
>   server)

-   Gửi thông tin chuyến, loại vé, số lượng đến server.

-   Nhận lại thông tin giá thanh toán từ server.

>   Bước 4: Kết thúc và đóng kết nối với server

Server:
-------

>   Bước 1: Tạo socket

-   Hàm thực hiện: createSocket()

>   Bước 2: Kết nối server

-   Port: 8080

-   Hàm thực hiện: bindSocket()

>   Bước 3: Đợi kết nối từ client

-   Xóa kết nối cũ

-   Lắng nghe kết nối mới từ client

    -   Hàm chạy trên luồng riêng biệt để client khi kết nối không cần chờ đợi

>   Bước 4: Kết nối client khi lắng nghe được yêu cầu kết nối

-   Hàm thực hiện: acceptSocket()

>   Bước 5: Lắng nghe thông điệp từ client (xử lý tuần tự)

>   Bước 6: Phân giải thông điệp và xử lý theo yêu cầu

>   Bước 7: Server gửi gói tin kết quả cho client. Kết thúc phiên giao dịch với
>   client đó.

>   Bước 8: Lắng nghe và xử lý yêu cầu tiếp theo của client trong hàng đợi.

Cấu trúc dữ liệu
================

![https://github.com/liem18112000/socket/blob/master/Data%20structure%20%2B%20DB.jpeg](media/f704d3b8ce4908269751ba6f403eeda2.jpg)

Chương trình bao gồm 2 class:

-   Class Server

-   Class Client

Cơ sở dữ liệu được định nghĩa như trên:

-   Cơ sở dữ liệu được lưu trữ dưới dạng SQL trên localhost của Server:

![](media/501e4232b93460c50c7ac0fbee76352e.png)

Giải pháp truy cập đồng thời nhiều Clients – Server
===================================================

Tổng quát:
----------

-   Giải pháp bao gồm 2 yếu tố chính:

    -   Phía máy chủ :

        -   Các chương trình được thiết lập đa tiến trình (multi-programming)

        -   Máy chủ tạo ra một hàng đợi (Queue - FIFO) để chứa các yêu cầu tác
            vụ từ các máy khách =\> Các tác vụ của máy khách được xử lý tuần tự

        -   Có ba tiến trình chính chạy song:

            -   Tiến trình 1 : liên tục lắng nghe các yêu cầu kết nối từ các máy
                khách

            -   Tiến trình 2 : xử lý các yêu cầu từ phía máy khách đầu tiên
                trong hàng đợi

            -   Tiến trình 3: xử lý các yêu cầu từ người quản lý máy chủ
                (administrator) với các lệnh sẵn có trong hệ thống

    -   Phía máy khách:

        -   Lắng nghe lượt xử lý trong hàng đợi và kiểm tra xem đến lượt xử lý
