import streamlit as st
import pandas as pd
st.image("logo.jpg")
# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# TIÊU ĐỀ
# ==============================
st.title("💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.write(
    "Ứng dụng tính tiền lãi theo phương pháp lãi đơn hoặc lãi kép "
    "với nhiều hình thức nhận lãi."
)

st.divider()

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# ==============================
# NHẬP THÔNG TIN
# ==============================
st.subheader("📋 Thông tin khoản tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1
)

phuong_phap = st.selectbox(
    "Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc = st.selectbox(
    "Hình thức lãnh lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.divider()

# ==============================
# NÚT TÍNH TOÁN
# ==============================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    r = lai_suat / 100

    # Số tháng của kỳ hạn
    months = int(ky_han)

    # ==============================
    # XÁC ĐỊNH SỐ KỲ TRẢ LÃI
    # ==============================
    if hinh_thuc == "Lãnh lãi hàng tháng":
        so_ky = months
        thang_moi_ky = 1

    elif hinh_thuc == "Lãnh lãi hàng quý":
        so_ky = months // 3

        # Nếu kỳ hạn không chia hết cho 3
        # thì phần tháng còn lại được tính cuối kỳ
        thang_moi_ky = 3

    else:
        so_ky = 1
        thang_moi_ky = months

    # ==============================
    # LÃI ĐƠN
    # ==============================
    if phuong_phap == "Lãi đơn":

        # Tổng số năm gửi
        thoi_gian_nam = months / 12

        # Tổng tiền lãi
        tong_lai = so_tien * r * thoi_gian_nam

        # Tiền lãi mỗi kỳ
        if hinh_thuc == "Lãnh lãi hàng tháng":
            lai_dinh_ky = so_tien * r / 12

        elif hinh_thuc == "Lãnh lãi hàng quý":
            lai_dinh_ky = so_tien * r / 4

        else:
            lai_dinh_ky = tong_lai

        tong_tien = so_tien + tong_lai

        # ==============================
        # BẢNG CHI TIẾT
        # ==============================
        data = []

        for i in range(1, so_ky + 1):

            if hinh_thuc == "Lãnh lãi hàng tháng":
                lai_ky = so_tien * r / 12
                thang = i

            elif hinh_thuc == "Lãnh lãi hàng quý":
                lai_ky = so_tien * r / 4
                thang = i * 3

            else:
                lai_ky = tong_lai
                thang = months

            data.append({
                "Kỳ": i,
                "Tháng": thang,
                "Tiền gốc": format_money(so_tien),
                "Tiền lãi kỳ này": format_money(lai_ky)
            })

    # ==============================
    # LÃI KÉP
    # ==============================
    else:

        data = []

        # ------------------------------
        # LÃNH LÃI CUỐI KỲ
        # ------------------------------
        if hinh_thuc == "Lãnh lãi cuối kỳ":

            # Lãi kép theo tháng
            so_ky_lai = months
            lai_suat_ky = r / 12

            tien_hien_tai = so_tien

            for i in range(1, so_ky_lai + 1):

                lai_ky = tien_hien_tai * lai_suat_ky
                tien_hien_tai += lai_ky

                data.append({
                    "Kỳ": i,
                    "Tháng": i,
                    "Tiền gốc đầu kỳ": format_money(
                        tien_hien_tai - lai_ky
                    ),
                    "Tiền lãi kỳ này": format_money(lai_ky),
                    "Tổng sau kỳ": format_money(tien_hien_tai)
                })

            tong_tien = tien_hien_tai
            tong_lai = tong_tien - so_tien

            # Lãi kỳ cuối
            lai_dinh_ky = data[-1]["Tiền lãi kỳ này"]

        # ------------------------------
        # LÃNH LÃI HÀNG THÁNG
        # ------------------------------
        elif hinh_thuc == "Lãnh lãi hàng tháng":

            # Với lãi kép, tiền lãi được nhập vào gốc
            # sau mỗi tháng.
            lai_suat_ky = r / 12
            tien_hien_tai = so_tien

            for i in range(1, months + 1):

                tien_dau_ky = tien_hien_tai

                lai_ky = tien_dau_ky * lai_suat_ky

                tien_hien_tai += lai_ky

                data.append({
                    "Kỳ": i,
                    "Tháng": i,
                    "Tiền gốc đầu kỳ": format_money(tien_dau_ky),
                    "Tiền lãi kỳ này": format_money(lai_ky),
                    "Tổng sau kỳ": format_money(tien_hien_tai)
                })

            tong_tien = tien_hien_tai
            tong_lai = tong_tien - so_tien
            lai_dinh_ky = data[-1]["Tiền lãi kỳ này"]

        # ------------------------------
        # LÃNH LÃI HÀNG QUÝ
        # ------------------------------
        else:

            so_quy = months // 3

            # Nếu kỳ hạn nhỏ hơn 3 tháng
            if so_quy == 0:
                st.error(
                    "Kỳ hạn phải từ 3 tháng trở lên nếu chọn lãnh lãi hàng quý."
                )
                st.stop()

            lai_suat_ky = r / 4
            tien_hien_tai = so_tien

            for i in range(1, so_quy + 1):

                tien_dau_ky = tien_hien_tai

                lai_ky = tien_dau_ky * lai_suat_ky

                tien_hien_tai += lai_ky

                data.append({
                    "Kỳ": i,
                    "Tháng": i * 3,
                    "Tiền gốc đầu kỳ": format_money(tien_dau_ky),
                    "Tiền lãi kỳ này": format_money(lai_ky),
                    "Tổng sau kỳ": format_money(tien_hien_tai)
                })

            tong_tien = tien_hien_tai
            tong_lai = tong_tien - so_tien
            lai_dinh_ky = data[-1]["Tiền lãi kỳ này"]

    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================
    st.divider()
    st.subheader("📊 KẾT QUẢ")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(
                float(
                    str(lai_dinh_ky)
                    .replace(".", "")
                    .replace(" VNĐ", "")
                )
            )
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_lai)
        )

    with col3:
        st.metric(
            "💰 Tổng gốc + lãi",
            format_money(tong_tien)
        )

    # ==============================
    # THÔNG TIN TÓM TẮT
    # ==============================
    st.subheader("📝 Thông tin khoản gửi")

    st.write(f"**Số tiền gửi:** {format_money(so_tien)}")
    st.write(f"**Kỳ hạn:** {months} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Phương pháp:** {phuong_phap}")
    st.write(f"**Hình thức:** {hinh_thuc}")

    # ==============================
    # BẢNG CHI TIẾT
    # ==============================
    st.subheader("📅 Chi tiết theo từng kỳ")

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ==============================
    # CÔNG THỨC
    # ==============================
    with st.expander("📚 Xem công thức tính"):

        if phuong_phap == "Lãi đơn":
            st.latex(
                r"I = P \times r \times t"
            )

            st.write(
                "Trong đó: P là số tiền gốc, r là lãi suất năm "
                "và t là thời gian gửi tính theo năm."
            )

        else:
            st.latex(
                r"A = P(1+r)^n"
            )

            st.write(
                "Trong đó: P là tiền gốc, r là lãi suất mỗi kỳ, "
                "n là số kỳ nhập lãi và A là tổng tiền nhận được."
            )

    st.success("✅ Đã tính toán khoản tiền gửi thành công!")
