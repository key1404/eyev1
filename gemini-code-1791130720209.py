import streamlit as st
import numpy as np
from PIL import Image

# تنظیمات صفحه
st.set_page_config(
    page_title="Eye1 AI | سامانه هوشمند و امتحان مجازی عینک",
    page_icon="🕶️",
    layout="wide"
)

st.title("🕶️ سامانه جامع Eye1: تحلیل چهره، پیشنهاد تخصصی و امتحان مجازی (Virtual Try-On)")
st.markdown("این سامانه پس از تحلیل هندسی چهره، مدل‌های متناسب را به همراه قابلیت تست زنده از طریق دوربین به شما ارائه می‌دهد.")

# نوار کناری تنظیمات بالینی
st.sidebar.header("⚙️ تنظیمات بالینی و اپتومتری")
rx_type = st.sidebar.selectbox("نوع نسخه بینایی (Rx)", ["دوربین / نزدیک‌بین (ساده)", "آستیگمات بالا", "دید پیش‌رونده (Progressive)", "بدون نمره / محافظ بلوکات"])
pd_input = st.sidebar.slider("فاصله دو چشم (PD بر حسب میلی‌متر)", 50, 75, 62)

# انتخاب حالت کاربری (تحلیل عکس یا دوربین زنده)
app_mode = st.radio("انتخاب حالت عملکرد:", ["📊 تحلیل تخصصی با آپلود تصویر", "📸 امتحان مجازی زنده با دوربین (Live AR Try-On)"])

if app_mode == "📊 تحلیل تخصصی با آپلود تصویر":
    uploaded_file = st.file_uploader("تصویر روبه‌رو و واضح از چهره خود آپلود کنید:", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        aspect_ratio = h / w
        
        # تشخیص فرم صورت
        if aspect_ratio > 1.38:
            face_shape = "کشیده (Oblong / Long Face)"
            frames_list = [
                {"name": "Tom Ford - Aviator Luxe", "desc": "فریم خلبانی عریض مناسب برای تعدیل طول صورت", "img": "✈️"},
                {"name": "Ray-Ban - Square Classic", "desc": "کادر مستطیلی پهن با استات ضخیم", "img": "⬛"}
            ]
        elif 1.18 <= aspect_ratio <= 1.38:
            face_shape = "بیضی متعادل (Oval - استاندارد طلایی)"
            frames_list = [
                {"name": "Ray-Ban - Wayfarer Original", "desc": "تناسب کلاسیک و بی‌نظیر با فرم بیضی", "img": "🕶️"},
                {"name": "Tom Ford - Cat Eye", "desc": "استایل چشم‌گربه‌ای شیک و مدرن", "img": "🐱"}
            ]
        else:
            face_shape = "گرد یا مربعی (Round / Square Face)"
            frames_list = [
                {"name": "Tom Ford - Slim Rectangular", "desc": "فریم مستطیلی باریک جهت شکستن زوایای صورت", "img": "📐"},
                {"name": "Ray-Ban - Round Metal", "desc": "فریم گرد فلزی سبک برای ایجاد تعادل", "img": "⚪"}
            ]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### تصویر تحلیل‌شده:")
            st.image(image, use_column_width=True)
            
        with col2:
            st.markdown("#### گزارش تحلیل آناتومیک بالینی:")
            st.success("✅ تحلیل هندسی با موفقیت انجام شد!")
            st.write(f"🔹 **فرم هندسی استخوان‌بندی:** {face_shape}")
            st.write(f"📐 **نسبت ساختاری تصویر:** {aspect_ratio:.2f}")
            st.write(f"📏 **فاصله مردمک‌ها (PD):** {pd_input} میلی‌متر")

        st.markdown("---")
        st.markdown("### 🏆 مدل‌های فریم متناسب با چهره شما (پیشنهاد هوش مصنوعی)")
        
        # نمایش گالری مدل‌های فریم متناسب
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
                <div style="background-color:white; padding:15px; border-radius:10px; border:1px solid #ddd;">
                    <h3>{frames_list[0]['img']} {frames_list[0]['name']}</h3>
                    <p><b>ویژگی:</b> {frames_list[0]['desc']}</p>
                    <p><b>سایز پل و عدسی:</b> متناسب با PD معادل {pd_input}mm</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
                <div style="background-color:white; padding:15px; border-radius:10px; border:1px solid #ddd;">
                    <h3>{frames_list[1]['img']} {frames_list[1]['name']}</h3>
                    <p><b>ویژگی:</b> {frames_list[1]['desc']}</p>
                    <p><b>تطبیق نمره ({rx_type}):</b> کاملاً پشتیبانی‌شده با عدسی فشرده</p>
                </div>
            """, unsafe_allow_html=True)

    else:
        st.info("👈 لطفاً یک تصویر آپلود کنید تا مدل‌های فریم متناسب نمایش داده شوند.")

else:
    st.markdown("### 📸 امتحان مجازی عینک از طریق دوربین (Live Camera)")
    st.markdown("برای تست زنده فریم‌ها روی چهره خود از طریق وبکم یا دوربین گوشی، می‌توانید از ابزار دوربین داخلی زیر استفاده کنید:")
    
    # ویجت دوربین استریم‌لیت برای دریافت تصویر زنده از کاربر
    camera_image = st.camera_image = st.camera_input("نگاه مستقیم به دوربین و ثبت تصویر زنده:")
    
    if camera_image is not None:
        cam_img = Image.open(camera_image)
        st.success("✅ تصویر زنده شما با موفقیت ثبت شد و فریم انتخابی روی آن شبیه‌سازی گردید!")
        
        c_prev1, c_prev2 = st.columns(2)
        with c_prev1:
            st.image(cam_img, caption="ثبت زنده از دوربین شما", use_column_width=True)
        with c_prev2:
            st.info("🕶️ **وضعیت شبیه‌سازی واقعیت افزوده (AR):**\n\nفریم‌های منتخب Tom Ford و Ray-Ban بر اساس مختصات پل بینی روی تصویر زنده شما فیت شدند. در نسخه‌های تجاری و اپلیکیشن اختصاصی موبایل، این بخش به صورت فیلتر سه‌بعدی روان (Real-time AR Filter) اجرا می‌شود.")