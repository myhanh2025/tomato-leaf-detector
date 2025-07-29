import streamlit as st
import requests
from PIL import Image
import io
import base64

# --- Cấu hình mô hình Roboflow ---
KHOA_API = "rSUzaeMGYrBA449orJYK"  # Ẩn thông tin API Key nếu chia sẻ công khai
TEN_MO_HINH = "tomato-leaf-diseases-lmem9"
PHIEN_BAN = "1"
DIA_CHI_API = f"https://detect.roboflow.com/{TEN_MO_HINH}/{PHIEN_BAN}?api_key={KHOA_API}"

# --- Hàm gửi ảnh lên Roboflow để dự đoán ---
def du_doan_benh(anh):
    bo_dem = io.BytesIO()
    anh.save(bo_dem, quality=90, format="JPEG")
    anh_mahoa = base64.b64encode(bo_dem.getvalue()).decode("utf-8")
    phan_hoi = requests.post(DIA_CHI_API, data=anh_mahoa, headers={"Content-Type": "application/x-www-form-urlencoded"})
    return phan_hoi.json()

# --- Giao diện Streamlit ---
st.set_page_config(page_title="Nhận diện bệnh lá cà chua", layout="centered")
st.title("🍅 Nhận diện bệnh trên lá cà chua")
st.write("Tải ảnh lá cà chua để nhận diện bệnh (Bấm vào nút Browser files)")

tep_anh = st.file_uploader("📤 Tải ảnh lên", type=["jpg", "jpeg", "png"])

if tep_anh is not None:
    anh = Image.open(tep_anh).convert("RGB")
    st.image(anh, caption="📷 Ảnh gốc", use_container_width=True)

    with st.spinner("🔎 Đang phân tích..."):
        ket_qua = du_doan_benh(anh)

    du_doan = ket_qua.get("predictions", [])
    if du_doan:
        benh = du_doan[0]
        ten_benh = benh["class"]
        do_tin_cay = round(benh["confidence"] * 100, 2)
        st.success(f"✅ Phát hiện: **{ten_benh}** (Độ tin cậy: {do_tin_cay}%)")

        mo_ta_benh = {
            "Bacterial_spot": "Bệnh đốm vi khuẩn – Nguyên nhân: Do vi khuẩn Xanthomonas campestris pv. vesicatoria gây ra. Triệu chứng: Xuất hiện các đốm nhỏ màu đen hoặc nâu trên lá, sau đó lan rộng và làm lá bị rách.Tác hại: Làm giảm khả năng quang hợp, ảnh hưởng đến sự phát triển và năng suất cây cà chua.",
            "Late_blight": "Bệnh mốc sương muộn – Nguyên nhân: Do nấm Phytophthora infestans gây ra.Triệu chứng: Các mảng màu nâu sẫm xuất hiện trên lá, thân và quả; có thể kèm theo viền màu vàng.Tác hại: Lây lan rất nhanh trong điều kiện ẩm ướt, gây héo rũ và chết cây hàng loạt.",
            "Leaf_Mold": "Mốc lá – Nguyên nhân: Do nấm Cladosporium fulvum gây ra.Triệu chứng: Mặt trên lá có đốm vàng, mặt dưới có lớp mốc màu xám hoặc xanh ô liu.Tác hại: Gây rụng lá sớm, ảnh hưởng nghiêm trọng đến năng suất.",
            "Septoria_leaf_spot": "Đốm lá Septoria – Nguyên nhân: Do nấm Septoria lycopersici gây ra.Triệu chứng: Các đốm tròn nhỏ, màu nâu với viền sẫm, xuất hiện chủ yếu ở lá già.Tác hại: Làm lá bị rụng sớm, cây sinh trưởng kém.",
            "Yellow_Leaf_Curl_Virus": "xoăn vàng lá – Nguyên nhân: Do virus TYLCV lây truyền qua bọ phấn trắng.Triệu chứng: Lá non bị xoăn lại, chuyển vàng, cây còi cọc và ít ra hoa, đậu quả.Tác hại: Làm giảm nghiêm trọng năng suất và chất lượng cà chua.",
            "healthy": "Lá khỏe mạnh – Không có dấu hiệu bệnh lý. Lá có màu xanh tươi, không đốm, không xoăn, không héo."
        }

        st.info(f"📖 {mo_ta_benh.get(ten_benh, 'Không có mô tả chi tiết')}")
    else:
        st.warning("😕 Không phát hiện bệnh nào trên lá.")
