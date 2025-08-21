import streamlit as st
import pandas as pd

# Load dataset (you can replace with bigger dataset later)
df = pd.read_csv("food_data.csv")

st.title("🍎 IngredientSight")
st.subheader("Turn confusing food labels into clear health insights")

# Input from user
ingredients_input = st.text_area("Enter ingredients (comma-separated):")

if st.button("Analyze"):
    if ingredients_input.strip() == "":
        st.warning("Please enter at least one ingredient.")
    else:
        ingredients = [i.strip().lower() for i in ingredients_input.split(",")]
        results = df[df["ingredient"].isin(ingredients)]
        
        if results.empty:
            st.info("No insights found in dataset for these ingredients.")
        else:
            st.success("Here are the insights:")
            for _, row in results.iterrows():
                st.write(f"- **{row['ingredient'].title()}** → {row['impact']}")
