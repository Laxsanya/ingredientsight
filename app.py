import streamlit as st
import requests
import pytesseract
from PIL import Image
import pandas as pd
import io

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="IngredientInsight AI",
    page_icon="🥗",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#d4fc79,#96e6a1);
background-size:400% 400%;
animation:bg 15s ease infinite;
}

@keyframes bg{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

.big-title{
font-size:55px;
font-weight:bold;
color:white;
text-align:center;
}

.subtitle{
font-size:22px;
text-align:center;
color:white;
margin-bottom:30px;
}

.card{

background:white;
padding:20px;
border-radius:18px;
box-shadow:0px 10px 25px rgba(0,0,0,.15);
margin-bottom:20px;
transition:.3s;

}

.card:hover{

transform:translateY(-6px);

}

.stButton>button{

width:100%;
height:55px;
font-size:20px;
border-radius:15px;
background:#16a34a;
color:white;
font-weight:bold;
border:none;

}

.stButton>button:hover{

background:#15803d;

}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------

st.markdown(
'<div class="big-title">🥗 IngredientInsight AI</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="subtitle">Understand What You Eat.</div>',
unsafe_allow_html=True
)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("Navigation")

page=st.sidebar.radio(

"Go To",

[
"Home",
"History",
"About"

]

)

if "history" not in st.session_state:
    st.session_state.history=[]
# -----------------------------
# HOME PAGE
# -----------------------------

if page == "Home":

    st.markdown("### 📷 Upload a Food Label")

    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"]
    )

    st.markdown("### ✍️ Or Type Food / Ingredient")

    manual_text = st.text_area(
        "",
        placeholder="Examples:\nPizza\nBurger\nTomato\nMaggi\nOreo\nMilk\nSugar\nSalt"
    )

    ingredients = []

    # -------------------------
    # OCR
    # -------------------------

    if uploaded_file:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

        with st.spinner("🔍 Reading Image..."):

            try:

                text = pytesseract.image_to_string(image)

                st.success("✅ Text Extracted")

                st.text(text)

                ingredients.extend(

                    [
                        x.strip()

                        for x in text.replace("\n", ",")

                        .split(",")

                        if x.strip()

                    ]

                )

            except Exception as e:

                st.error("OCR Failed")

    # -------------------------
    # Manual Input
    # -------------------------

    if manual_text:

        ingredients.extend(

            [

                x.strip()

                for x in manual_text.split(",")

                if x.strip()

            ]

        )

    # Remove duplicates

    ingredients = list(dict.fromkeys(ingredients))

    # -------------------------
    # Analyze Button
    # -------------------------

    if st.button("🔍 Analyze"):

        if len(ingredients) == 0:

            st.warning("Please upload an image or type some food names.")

        else:

            st.success(f"Found {len(ingredients)} item(s).")

            st.session_state.history.extend(ingredients)

            for item in ingredients:

                st.markdown("---")

                st.markdown(f"## 🍽️ {item.title()}")

                with st.spinner("Searching Database..."):

                    try:

                        url = "https://world.openfoodfacts.org/cgi/search.pl"

                        params = {

                            "search_terms": item,

                            "search_simple": 1,

                            "action": "process",

                            "json": 1,

                            "page_size": 1

                        }

                        response = requests.get(

                            url,

                            params=params,

                            timeout=10

                        )

                        data = response.json()
                                                if data.get("products"):

                            product = data["products"][0]

                            nutriments = product.get("nutriments", {})

                            calories = nutriments.get(
                                "energy-kcal_100g",
                                nutriments.get("energy-kcal", "N/A")
                            )

                            protein = nutriments.get(
                                "proteins_100g",
                                "N/A"
                            )

                            fat = nutriments.get(
                                "fat_100g",
                                "N/A"
                            )

                            carbs = nutriments.get(
                                "carbohydrates_100g",
                                "N/A"
                            )

                            sugar = nutriments.get(
                                "sugars_100g",
                                "N/A"
                            )

                            salt = nutriments.get(
                                "salt_100g",
                                "N/A"
                            )

                            fiber = nutriments.get(
                                "fiber_100g",
                                "N/A"
                            )

                            category = product.get(
                                "categories",
                                "Unknown"
                            )

                            score = 100

                            try:
                                if sugar != "N/A":
                                    score -= float(sugar) * 1.5
                            except:
                                pass

                            try:
                                if fat != "N/A":
                                    score -= float(fat) * 0.8
                            except:
                                pass

                            try:
                                if salt != "N/A":
                                    score -= float(salt) * 15
                            except:
                                pass

                            score = max(0, min(100, int(score)))

                            if score >= 85:
                                color = "🟢"
                                status = "Excellent"

                            elif score >= 70:
                                color = "🟢"
                                status = "Healthy"

                            elif score >= 55:
                                color = "🟡"
                                status = "Moderate"

                            elif score >= 40:
                                color = "🟠"
                                status = "Poor"

                            else:
                                color = "🔴"
                                status = "Avoid Frequent Consumption"

                            st.markdown(
                                f"""
<div class="card">

<h2>{item.title()}</h2>

<b>Category:</b> {category}<br><br>

<b>{color} Health Score:</b> {score}/100
({status})

</div>
""",
                                unsafe_allow_html=True
                            )

                            c1, c2 = st.columns(2)

                            with c1:
                                st.metric("🔥 Calories", calories)
                                st.metric("🥩 Protein (g)", protein)
                                st.metric("🍞 Carbs (g)", carbs)

                            with c2:
                                st.metric("🧈 Fat (g)", fat)
                                st.metric("🍬 Sugar (g)", sugar)
                                st.metric("🧂 Salt (g)", salt)

                            st.subheader("Nutrition Progress")

                            try:
                                st.progress(min(float(protein)/50,1.0))
                                st.caption("Protein")

                            except:
                                pass

                            try:
                                st.progress(min(float(fiber)/30,1.0))
                                st.caption("Fiber")

                            except:
                                pass

                            try:
                                st.progress(min(float(sugar)/50,1.0))
                                st.caption("Sugar")

                            except:
                                pass

                            st.subheader("💡 AI Health Advice")

                            advice = []

                            try:
                                if float(sugar) > 15:
                                    advice.append(
                                        "🍬 High sugar. Consume in moderation."
                                    )
                            except:
                                pass

                            try:
                                if float(fat) > 20:
                                    advice.append(
                                        "🧈 High fat content."
                                    )
                            except:
                                pass

                            try:
                                if float(salt) > 1.5:
                                    advice.append(
                                        "🧂 High sodium."
                                    )
                            except:
                                pass

                            if len(advice) == 0:
                                advice.append(
                                    "🥗 Looks like a balanced choice."
                                )

                            for tip in advice:
                                st.info(tip)

                        else:

                            st.warning(
                                f"No information found for '{item}'."
                            )

                    except Exception:

                        st.error(
                            "Unable to connect to the food database."
                        )
                        # -----------------------------
# HISTORY PAGE
# -----------------------------

elif page == "History":

    st.markdown("## 📜 Your Search History")

    if "history" not in st.session_state:
        st.session_state.history = []

    if len(st.session_state.history) == 0:
        st.info("No history yet. Analyze some food items first.")
    else:
        st.write("Previously analyzed items:")

        for i, item in enumerate(st.session_state.history[::-1], 1):
            st.markdown(f"{i}. {item}")

        # -------------------------
        # DOWNLOAD HISTORY
        # -------------------------

        import pandas as pd

        df = pd.DataFrame(st.session_state.history, columns=["Food Item"])

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download History as CSV",
            data=csv,
            file_name="food_history.csv",
            mime="text/csv"
        )


# -----------------------------
# ABOUT PAGE
# -----------------------------

elif page == "About":

    st.markdown("## ℹ️ About This App")

    st.markdown(
        """
        This AI-powered Food Ingredient Analyzer helps you:

        🍕 Scan food labels using OCR  
        🔍 Detect ingredients automatically  
        🧠 Analyze nutrition using OpenFoodFacts  
        📊 Generate health scores (0–100)  
        💡 Get AI-style health advice  

        ---
        ### 🚀 Features
        - Image Upload (OCR)
        - Manual Food Input
        - Nutrition Breakdown
        - Health Scoring System
        - Search History Tracking

        ---
        Built using **Streamlit + Python + OpenFoodFacts API**
        """
    )
