import streamlit as st
import requests
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv # Import thư viện dotenv

# --- Tải biến môi trường từ file .env ---
# Chỉ dùng khi chạy cục bộ. Khi triển khai lên Streamlit Cloud,
# API Key sẽ được lấy từ Streamlit Secrets.
load_dotenv()

# --- Cấu hình mô hình Roboflow ---
# LƯU Ý QUAN TRỌNG: ROBOFLOW_API_KEY được lấy từ biến môi trường (từ file .env khi chạy cục bộ,
# hoặc từ Streamlit Secrets khi triển khai lên Streamlit Cloud).
KHOA_API = os.getenv("ROBOFLOW_API_KEY")

TEN_MO_HINH = "tomato-leaf-diseases-lmem9"
PHIEN_BAN = "1"
DIA_CHI_API = f"https://detect.roboflow.com/{TEN_MO_HINH}/{PHIEN_BAN}?api_key={KHOA_API}"

# --- Hàm xử lý ảnh và gửi đến Roboflow ---
def du_doan_benh(anh):
    """Gửi ảnh đến API Roboflow để nhận dạng."""
    bo_dem = io.BytesIO()
    anh.save(bo_dem, quality=90, format="JPEG")
    anh_mahoa = base64.b64encode(bo_dem.getvalue()).decode("utf-8")
    phan_hoi = requests.post(DIA_CHI_API, data=anh_mahoa, headers={"Content-Type": "application/x-www-form-urlencoded"})
    return phan_hoi.json()

# --- Thông tin mô tả bệnh ---
mo_ta_benh = {
    "Bacterial_spot": "🔴 **Bệnh đốm vi khuẩn**\n* **Nguyên nhân:** Vi khuẩn Xanthomonas.\n* **Triệu chứng:** Xuất hiện các đốm nhỏ màu đen hoặc nâu trên lá, sau đó lan rộng và làm lá bị rách.\n* **Tác hại:** : Làm giảm khả năng quang hợp, ảnh hưởng đến sự phát triển và năng suất cây cà chua.",
    "Late_blight": "🔵 **Bệnh mốc sương muộn**\n* **Nguyên nhân:** Nấm Phytophthora infestans.\n* **Triệu chứng:** Các mảng màu nâu sẫm xuất hiện trên lá, thân và quả; có thể kèm theo viền màu vàng.\n* **Tác hại:** Lây lan rất nhanh trong điều kiện ẩm ướt, gây héo rũ và chết cây hàng loạt.",
    "Leaf_Mold": "🟡 **Bệnh Mốc lá**\n* **Nguyên nhân:** Nấm Cladosporium fulvum.\n* **Triệu chứng:** Mặt trên lá có đốm vàng, mặt dưới có lớp mốc màu xám hoặc xanh ô liu.\n* **Tác hại:** Gây rụng lá sớm, ảnh hưởng nghiêm trọng đến năng suất.",
    "Septoria_leaf_spot": "🟠 **Đốm lá Septoria**\n* **Nguyên nhân:** Nấm Septoria lycopersici.\n* **Triệu chứng:** Các đốm tròn nhỏ, màu nâu với viền sẫm, xuất hiện chủ yếu ở lá già.\n* **Tác hại:** Làm lá bị rụng sớm, cây sinh trưởng kém.",
    "Yellow_Leaf_Curl_Virus": "🟣 **Bệnh xoăn vàng lá**\n* **Nguyên nhân:** Virus TYLCV lây qua bọ phấn trắng.\n* **Triệu chứng:** Lá non bị xoăn lại, chuyển vàng, cây còi cọc và ít ra hoa, đậu quả.\n* **Tác hại:** Làm giảm nghiêm trọng năng suất và chất lượng cà chua.",
    "healthy": "✅ **Lá khỏe mạnh**\nKhông có dấu hiệu bệnh lý. Cây phát triển tốt, lá có màu xanh đều, không có biểu hiện xoăn, héo hay đốm bất thường."
}

# --- Cấu hình trang và CSS tùy chỉnh để làm đẹp giao diện ---
st.set_page_config(page_title="Ứng dụng Nhận diện Bệnh Lá Cà Chua", page_icon="🍅", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        color: #333;
        font-size: 1.1em;
    }
    .stApp {
        background-color: #f0f2f6;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 700px;
        margin: auto;
    }
    h1 {
        color: #B22222; /* Màu đỏ nổi bật hơn (FireBrick) */
        text-align: center;
        margin-bottom: 2rem; /* Tăng khoảng cách dưới tiêu đề */
        font-size: 3em;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* --- CSS ĐỂ TÙY CHỈNH KHUNG UPLOAD --- */
    .stFileUploader {
        border: 2px dashed #a7d9b5;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #e6ffe6;
        transition: all 0.3s ease-in-out;
        min-height: 150px; /* Thêm chiều cao tối thiểu */
        position: relative; /* Cần thiết để định vị pseudo-element */
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stFileUploader:hover {
        border-color: #28a745;
        background-color: #d4ffd4;
    }

    /* Ẩn hoàn toàn nội dung mặc định của streamlit (icon, text, button) */
    .stFileUploader [data-testid="stFileUploaderDropzone"] section {
        display: none;
    }

    /* Thêm văn bản tùy chỉnh vào bên trong khung */
    .stFileUploader::before {
        content: 'Bấm vào đây để chụp hoặc tải ảnh lá cà chua lên';
        display: block;
        color: #c62828; /* Màu đỏ cho nổi bật */
        font-weight: 900;
        font-size: 1.2rem;
        pointer-events: none; /* Để có thể click xuyên qua chữ */
        padding: 0 20px; /* Thêm padding để chữ không bị sát viền */
    }
    /* --- KẾT THÚC CSS TÙY CHỈNH --- */

    .stImage {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stSpinner > div > div {
        color: #28a745 !important;
    }

    /* === CSS ĐÃ CẬP NHẬT ĐỂ LÀM NỔI BẬT KẾT QUẢ === */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 8px;
        padding: 18px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
        font-size: 1.4em !important; /* Tăng kích thước chữ của kết quả */
        line-height: 1.6;
    }
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border-left: 6px solid #28a745;
        font-weight: 700 !important; /* Làm chữ đậm hơn */
    }
    .stInfo {
        background-color: #d1ecf1;
        color: #0c5460;
        border-left: 6px solid #17a2b8;
        font-weight: 500 !important; /* Cũng làm chữ đậm hơn */
    }
    /* === KẾT THÚC CSS CẬP NHẬT === */

    .stWarning {
        background-color: #fff3cd;
        color: #856404;
        border-left: 5px solid #ffc107;
    }
    .stError {
        background-color: #f8d7da;
        color: #721c24;
        border-left: 5px solid #dc3545;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid #eee;
        color: #777;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# --- Giao diện Streamlit ---
st.title("🍅 ỨNG DỤNG AI NHẬN DIỆN BỆNH QUA LÁ CÀ CHUA 🍃")

# Ẩn nhãn mặc định của file_uploader và sử dụng nhãn tùy chỉnh qua CSS
tep_anh = st.file_uploader(
    label="Tải ảnh lên", # Dòng chữ này sẽ không hiển thị
    type=["jpg", "jpeg", "png"],
    help="Hỗ trợ các định dạng: JPG, JPEG, PNG. Dung lượng tối đa 200MB.",
    label_visibility="collapsed" # Thuộc tính quan trọng để ẩn nhãn mặc định
)


if tep_anh is not None:
    anh = Image.open(tep_anh).convert("RGB")
    st.image(anh, caption="📷 Ảnh đã tải lên", use_container_width=True)

    with st.spinner("🔍 Đang phân tích... Vui lòng chờ ⏳"):
        ket_qua = du_doan_benh(anh)

    du_doan = ket_qua.get("predictions", [])
    if du_doan:
        benh = du_doan[0]
        ten_benh_goc = benh["class"]
        do_tin_cay = round(benh["confidence"] * 100, 2)

        # Định dạng tên bệnh để hiển thị đẹp hơn
        formatted_ten_benh = ' '.join([word.capitalize() for word in ten_benh_goc.split('_')])

        st.success(f"**Phát hiện:** {formatted_ten_benh} (Độ tin cậy: {do_tin_cay:.1f}%)")

        # Hiển thị mô tả bệnh
        st.info(f"**Thông tin bệnh:**\n{mo_ta_benh.get(ten_benh_goc, 'Không có mô tả chi tiết cho loại bệnh này.')}")
    else:
        st.warning("🥺 Không phát hiện được bệnh nào. Vui lòng thử ảnh khác hoặc đảm bảo ảnh rõ ràng.")

# Thêm footer
st.markdown("---")
st.markdown('<div class="footer">Dự án được thực hiện bởi nhóm nghiên cứu AI.</div>', unsafe_allow_html=True)
