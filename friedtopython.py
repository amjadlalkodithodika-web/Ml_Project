

# --- Imports ---
import numpy as np
import joblib
import streamlit as st 
from PIL import Image
import qrcode
from io import BytesIO

# --- Load Models/Encoders ---
model=joblib.load('model.pkl')
le=joblib.load('le.pkl')
# me2=joblib.load('me2.pkl')
# me3=joblib.load("me3.pkl")
oe1=joblib.load('oe1.pkl')
oe2=joblib.load('oe2.pkl')
oe3=joblib.load('oe3.pkl')

# --- Page Config ---
st.set_page_config(page_title="KFC Preference App", layout="wide")

# --- Sidebar (Theme only) ---
# st.sidebar.title("⚙️ Settings")
# theme = st.sidebar.radio("Choose Theme", ["Light", "Dark", "KFC Red"])

# if theme == "Light":
#     st.markdown("<style>.stApp { background-color: #ffffff; color: #1e1e1e .stButton { background-color: #ffffff !important; color: #d32f2f !important;border-radius: 8px; }</style>", unsafe_allow_html=True)
# elif theme == "Dark":
#     st.markdown("<style>.stApp { background-color: #1e1e1e; color: white .stButton { background-color: #ffffff !important; color: #d32f2f !important;border-radius: 8px; }</style>", unsafe_allow_html=True)
# elif theme == "KFC Red":
#     st.markdown("<style>.stApp { background-color: #d32f2f; color: white .stButton { background-color: #ffffff !important; color: #d32f2f !important;border-radius: 8px;}</style>", unsafe_allow_html=True)

# import streamlit as st

st.sidebar.title("⚙️ Settings")
theme = st.sidebar.radio("Choose Theme", ["Teal", "Dark", "KFC Red"])

if theme == "Teal":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #008080;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #1e1e1e !important;
            color: #ffffff !important;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

elif theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        .stButton>button {
            background-color: #ffffff !important;
            color: #1e1e1e !important;
            border-radius: 8px;
        }
      
        </style>
        """,
        unsafe_allow_html=True
    )

elif theme == "KFC Red":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #d32f2f;
            color: white;
        }
        .stButton>button {
            background-color: #ffffff !important;
            color: #1e1e1e !important;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )



# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["Home", "About", "Details"])

# ---------------- HOME TAB ----------------
with tab1:
    col1, col2, col3 = st.columns([2,4,1])  # center content
    with col2:
        col1, col2, col3 = st.columns([2,6,1])
        with col2:
            st.title('CHECK YOUR TASTE')
        # col1, col2, col3 = st.columns([.5,5,.5])
        with col2:
            st.header('KFC FRIED CHICKEN PREFERENCE')
        st.subheader('“Finding Out What Makes You Go ‘Mmm’”')
        st.write("“Hello, loyal KFC fan — we’re capturing customer fried chicken preferences to serve the right flavor, "
                 "to the right person, at the right time — making every bite feel made just for them.”")

        st.image(r"C:\Users\amjad\OneDrive\ML project\KFC_friedchicken\assets\KFCPROJECTpic.jpg", use_container_width=True)

        # --- Input Widgets (with placeholders) ---
        age = st.number_input("Enter Your Age *", min_value=0, max_value=100, step=1,
                              key="age", value=st.session_state.get("age", 0))

        # gender = st.selectbox("Choose Your Gender *", ["Gender", "Male", "Female"],
                            #   key="gender", index=["Gender","Male","Female"].index(st.session_state.get("gender","Gender")))

        # location = st.selectbox("Choose Your Location", ["Location","Rural", "Urban"],
                                # key="location", index=["Location","Rural","Urban"].index(st.session_state.get("location","Location")))

        amount = st.number_input("Enter Your Expected Amount", min_value=0,
                                 key="amount", value=st.session_state.get("amount", 0))

        spicy = st.selectbox("Choose Your Spicy_Tolerances *", ["Spicy","Low","Medium","High"],
                             key="spicy", index=["Spicy","Low","Medium","High"].index(st.session_state.get("spicy","Spicy")))

        sweet = st.selectbox("Choose Your Sweetness_Pref *", ["Sweet","Low","Medium","High"],
                             key="sweet", index=["Sweet","Low","Medium","High"].index(st.session_state.get("sweet","Sweet")))

        crispy = st.selectbox("Choose Your Crunchiness_Pref *", ["Crispy","Low","Medium","High"],
                              key="crispy", index=["Crispy","Low","Medium","High"].index(st.session_state.get("crispy","Crispy")))

        # --- Buttons ---
        colA, colB = st.columns([1,1])
        with colA:
            predict_btn = st.button("🔮 Click")
        with colB:
            clear_inputs = st.button("🧹 Clear Inputs")

        # --- Clear Inputs Logic ---
        if clear_inputs:
            for key in ["age", "amount", "spicy", "sweet", "crispy"]: #"gender", "location"
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        # --- Prediction with Validation ---
        if predict_btn:
#             st.markdown(
#     """
#     <style>
#     /* Target st.warning box */
#     .stAlert {
#         background-color: #fff3cd !important;  /* light yellow background */
#         color: #1e1e1e !important;             /* dark yellow/brown text */
#         border: 1px solid #ffeeba;
#         border-radius: 8px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
            
            if age == 0  or spicy == "Spicy" or sweet == "Sweet" or crispy == "Crispy":#or gender == "Gender"
                st.warning("⚠️ Please fill in all required fields (marked with *) before predicting.")
            else:
                try:
                    # gender_val = me2[gender]
                    # location_val = me3[location]
                    spicy_val = oe1.transform([[spicy]])[0][0]
                    sweet_val = oe2.transform([[sweet]])[0][0]
                    crispy_val = oe3.transform([[crispy]])[0][0]

                    features = [[age, amount, spicy_val, sweet_val, crispy_val]]#, gender_val, location_val
                    prediction = model.predict(features)

                    # --- Show Prediction ---
                    if prediction == 0:
                        st.success('✅ BBQ Chicken')
                    elif prediction == 1:
                        st.success('🔥 Crispy Chicken')
                    elif prediction == 2:
                        st.success("🍔 Original Recipe")
                    elif prediction == 3:
                        st.success("🌶️ Peri Peri Chicken")
                    else:
                        st.success("🥳 Zinger Chicken")

                    # --- QR Code ---
                    menu_url = "https://share.google/abYSUjAdtLglMmU5z"
                    qr = qrcode.QRCode(box_size=8, border=2)
                    qr.add_data(menu_url)
                    qr.make(fit=True)

                    img = qr.make_image(fill_color="#d32f2f", back_color="white")
                    buf = BytesIO()
                    img.save(buf)
                    buf.seek(0)

                    st.subheader("📱 Scan to View Full Menu")
                    c1, c2, c3 = st.columns([1,2,1])
                    with c2:
                        st.image(buf, use_container_width=False, caption="Scan me for the KFC Menu")

                except Exception as e:
                    st.error(f'Error in prediction {e}')
        else:
            st.info("Fill in your details (fields with * are required) and click **Predict** to see your flavor match!")

# ---------------- ABOUT TAB ----------------
with tab2:
    st.header("About This App")
    st.write("""
    This app is designed to understand customer fried chicken preferences using machine learning.  
    By analyzing inputs like age, location, and taste choices, it predicts whether someone prefers spicy, sweet, or crispy flavors.  

    **Why It Matters**  
    - Helps KFC personalize recommendations and promotions  
    - Ensures the right flavor reaches the right customer at the right time  
    - Shows how data science improves customer experience in the food industry  

    **How It Works**  
    1. Collects user inputs (age, gender, location, taste preferences)  
    2. Encodes and scales the data  
    3. Runs the trained ML model (Gradient Boosting/XGBoost)  
    4. Returns the predicted flavor instantly  

    **Key Insight**  
    - Boosting models achieved ~99.9% accuracy  
    - Tree‑based methods clearly outperform simpler models  
    - Customer preferences follow strong, consistent patterns
    
    
    **Note :**

    - This project shows how ML can turn everyday choices — like fried chicken flavor — into actionable insights for smarter, tastier customer experiences.  
    - “Powered by AI: The dataset behind this app was created using artificial intelligence to simulate real KFC customer preferences.”  
    - “No real customers were harmed in the making of this dataset — it’s 100% AI‑generated for learning and demo purposes.”  
""")
  
  
# ---------------- DETAILS TAB ----------------
with tab3:
    st.title("👤 My Details")
    st.markdown("""
    **Name:** Amjad Lal K  
    **Role:** Data+Business Analyst (Intern)  
    **Project:** KFC Fried Chicken Preference Prediction  
    **LinkedIn:** [linkedin.com/in/amjad](https://linkedin.com/in/amjadlalk)  

    **Skills:**  
    - Python  
    - pandas  
    - scikit-learn  
    - Data simulation  
    - Model building  

    **Interests:**  
    - Realistic ML workflows  
    - Feature engineering  
    - Model evaluation  
    """)


# cloudflared tunnel --url http://localhost:8501