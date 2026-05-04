import streamlit as st
import numpy as np
import joblib
from PIL import Image

# ----------------------------
# Load ML model
# ----------------------------
model = joblib.load("FkN_ExtraTrees_Model.pkl")

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="Column Capacity Predictor", layout="wide")

# ----------------------------
# Custom CSS for styling
# ----------------------------
st.markdown("""
<style>
/* Compact numeric inputs */
div.stNumberInput > div > input {
    width: 60px !important;
    height: 30px !important;
    font-size: 14px;
}

/* Selectbox font size */
div.stSelectbox > div > div > div {
    font-size: 14px;
}

/* Labels font size */
label, span {
    font-size: 14px !important;
    font-weight: bold;
}

/* Card-like container for inputs */
div.stContainer {
    background-color: #f7f7f7;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 1px 1px 10px #d3d3d3;
}

/* Prediction result box */
.result-box {
    background-color: #d4edda;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #c3e6cb;
    font-size: 18px;
    font-weight: bold;
    color: #155724;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Top banner image
# ----------------------------
image = Image.open("Column_Section.png")
image_resized = image.resize((900, 180))
st.image(image_resized, caption="Column Section", use_container_width=True)

# ----------------------------
# Title & description
# ----------------------------
st.title("Axial Capacity Prediction Software")
st.markdown("""
**Machine Learning Model:** ExtraTrees  
Predict the **axial capacity (F_kN)** of columns for various shapes and reinforcement configurations.
""")

# ----------------------------
# Input panel card
# ----------------------------
with st.container():
    st.markdown("### Input Parameters", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Concrete & Steel Properties**")
        shape = st.selectbox("Shape", ["Square", "Rectangular", "Circular"])
        fc = st.number_input("fc (MPa)", 0.0)
        ts = st.number_input("ts (mm)", 0.0)
        fy = st.number_input("fy (MPa)", 0.0)
        w = st.number_input("w (mm)", 0.0)
        d = st.number_input("d (mm)", 0.0)

    with col2:
        st.markdown("**Geometric & Derived Ratios**")
        L = st.number_input("L (mm)", 0.0)
        A = st.number_input("A (mm²)", 0.0)
        Lw = st.number_input("L/w", 0.0)
        Ld = st.number_input("L/d", 0.0)
        dw = st.number_input("d/w", 0.0)
        D = st.number_input("D", 0.0)
        LD = st.number_input("L/D", 0.0)
        Dts = st.number_input("D/ts", 0.0)

# ----------------------------
# Convert shape to numeric
# ----------------------------
shape_dict = {"Square": 0, "Rectangular": 1, "Circular": 2}
shape_num = shape_dict[shape]

# ----------------------------
# Prediction button
# ----------------------------
if st.button("Predict Axial Capacity"):
    X = np.array([[shape_num, fc, ts, fy, w, d, L, A, Lw, Ld, dw, D, LD, Dts]])
    pred = model.predict(X)

    # Display result in a colored panel
    st.markdown(f"""
    <div class="result-box">
        ✅ Predicted Axial Capacity F_kN = {pred[0]:.2f} kN
    </div>
    """, unsafe_allow_html=True)
    st.info("Use this result for design validation or further analysis.")