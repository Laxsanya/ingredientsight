import streamlit as st
import pytesseract
from PIL import Image

# ---------------------------
# Fallback categories if not found in dataset
# ---------------------------
fallback_map = {
    "sugar": {"category": "Sweetener", "health": "Unhealthy in excess"},
    "salt": {"category": "Salt", "health": "High sodium risk"},
    "palm oil": {"category": "Fat", "health": "High in saturated fat"},
    "wheat flour": {"category": "Carbohydrate", "health": "Refined grain"},
    "milk": {"category": "Dairy", "health": "Good source of calcium"},
    "tomato": {"category": "Vegetable", "health": "Rich in vitamins"},
    "spinach": {"category": "Vegetable", "health": "Iron rich"},
    "preservative": {"category": "Additive", "health": "Should be limited"},
    "flavor": {"category": "Additive", "health": "Artificial ingredient"},
    "lecithin": {"category": "Emulsifier", "health": "Generally safe"},
    "caffeine": {"category": "Stimulant", "health": "Limit intake"},
}

# ---------------------------
# Function to get info
# ---------------------------
def get_ingredient_info(ingredient):
    ingredient = ingredient.lower().strip()
    if ingredient in fallback_map:
        return fallback_map[ingredient]
    return {"category": "Unknown", "health": "No info available, use with caution"}

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🍪 Ingredient Insight")
st.write("Upload an image of a food label to see ingredient health info.")

uploaded_file = st.file_uploader("Upload food label image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # OCR to extract text
    text = pytesseract.image_to_string(image)
    st.subheader("📃 Extracted Text")
    st.write(text)

    # Process ingredients (split by comma or newline)
    extracted_ingredients = [i.strip() for i in text.replace("\n", ",").split(",") if i.strip()]

    st.subheader("🥗 Ingredient Analysis")
    for ingredient in extracted_ingredients:
        info = get_ingredient_info(ingredient)
        st.write(f"**{ingredient.title()}** → {info['category']} | {info['health']}")
