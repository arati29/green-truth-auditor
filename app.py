import streamlit as st
import pandas as pd

# --- LOAD ALL DATA ---
try:
    brands_df = pd.read_csv("certified_brands.csv")
    buzz_df = pd.read_csv("buzzwords.csv")
    penalty_df = pd.read_csv("penalty_logic.csv")
    
    # Create a quick "Lookup Table" for penalties
    penalty_dict = dict(zip(penalty_df['category'], penalty_df['penalty_score']))
except FileNotFoundError:
    st.error("Error: Make sure all 3 CSV files are in the same folder as app.py!")

# --- USER INTERFACE ---
st.set_page_config(page_title="Green-Truth Auditor", page_icon="🌿")
st.title("🛡️ Green-Truth Auditor")
st.markdown("### Transparency Check for Sustainable Marketing")

brand_input = st.text_input("Enter Brand Name:", placeholder="e.g. Patagonia")
desc_input = st.text_area("Paste Product Description:", placeholder="e.g. Our 100% natural shirt is eco-friendly...")

if st.button("🚀 Run Audit"):
    score = 100
    report = []

    # LOGIC 1: Brand Verification
    is_verified = brands_df['brand_name'].str.contains(brand_input, case=False).any()
    if is_verified:
        st.success(f"✅ {brand_input} is a Verified Sustainable Brand!")
        score += 5 
    else:
        report.append(f"⚠️ Brand Record: {brand_input} is NOT in our certified database. (-15 pts)")
        score -= 15

    # LOGIC 2: Buzzword & Penalty Scan
    found_any_buzz = False
    for index, row in buzz_df.iterrows():
        if row['word'].lower() in desc_input.lower():
            found_any_buzz = True
            category = row['category']
            # Get the penalty from our 3rd file, default to 10 if category missing
            pts = penalty_dict.get(category, 10)
            score -= pts
            report.append(f"🚩 {category}: Found '{row['word']}' (-{pts} pts)")

    # --- FINAL VERDICT ---
    st.divider()
    final_score = max(0, min(100, score)) # Keep score between 0-100
    st.header(f"Final Trust Score: {final_score}/100")

    st.subheader("Reasoning Summary:")
    for item in report:
        st.write(item)
    
    if not found_any_buzz and is_verified:
        st.write("No major red flags detected. High transparency!")

    # UI Feedback based on score
    if final_score >= 80:
        st.balloons()
        st.info("Verdict: **LIKELY TRUSTWORTHY**")
    elif final_score >= 50:
        st.warning("Verdict: **PROCEED WITH CAUTION**")
    else:
        st.error("Verdict: **HIGH RISK OF GREENWASHING**")