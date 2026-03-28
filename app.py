import streamlit as st
from transformers import pipeline

st.markdown("""
<style>
.stApp {
    background-color: #f0fff4;
}

h1, h2, h3 {
    color: #2d6a4f;
}

.stButton>button {
    background-color: #2ecc71;
    color: white;
    border-radius: 10px;
    padding: 10px;
}

.stButton>button:hover {
    background-color: #27ae60;
}

.stTextInput>div>div>input {
    border: 2px solid #2ecc71;
}

.stTextArea textarea {
    border: 2px solid #2ecc71;
}
</style>
""", unsafe_allow_html=True)

# --- 1. AI MODEL ---
@st.cache_resource
def load_ai_model():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# --- 2. HARD-CODED DATA (NO CSV) ---

# Buzzwords list
buzzwords = [
    {"word": "eco-friendly", "category": "Vague Descriptors"},
    {"word": "sustainable", "category": "Vague Sustainability Terms"},
    {"word": "natural", "category": "Vague Descriptors"},
    {"word": "biodegradable", "category": "Misleading Technical Terms"},
    {"word": "non-toxic", "category": "Unverified Claims"},
    {"word": "green", "category": "Vague Descriptors"},
]

# Penalty logic
penalty_dict = {
    "Vague Descriptors": 5,
    "Unverified Claims": 20,
    "Vague Sustainability Terms": 15,
    "Misleading Technical Terms": 5
}

# Certified brands (optional use later)
certified_brands = {
    "patagonia": "B-corp",
    "allbirds": "B-corp",
    "organic basics": "GOTS",
    "pangaia": "B-corp",
    "Nike": "LEED",
    "Apple": "EPEAT",
    "Tesla": "LEED"
}

# --- 3. INITIALIZE ---
st.set_page_config(page_title="Green-Truth Auditor", page_icon="🌿")

classifier = load_ai_model()

# --- 4. UI ---
st.title("🌿 AI Green-Truth Auditor")
st.markdown("### Semantic Transparency Check for Marketing")

brand_input = st.text_input("Enter Brand Name:", placeholder="e.g. Apple")
brand_input.title
desc_input = st.text_area("Paste Product Description:", placeholder="e.g. Our natural process is eco-friendly...")
desc_input.title

# --- 5. RUN ANALYSIS ---
if st.button("🚀 Run AI Audit"):
    if not brand_input or not desc_input:
        st.warning("Please fill in both fields.")
    else:
        score = 100
        report = []

        desc_lower = desc_input.lower()

        # --- LOGIC A: Keyword Scan ---
        for item in buzzwords:
            word = item["word"]
            category = item["category"]

            if word in desc_lower:
                pts = penalty_dict.get(category, 10)
                score -= pts
                report.append(f"🚩 **Keyword Match:** '{word}' detected. (-{pts} pts)")

        # --- LOGIC B: AI Analysis ---
        with st.spinner("AI analyzing claim context..."):
            labels = ["vague green claim", "scientific fact", "misleading", "certified statement"]
            result = classifier(desc_input, labels)

            top_label = result['labels'][0]
            confidence = result['scores'][0]

            if top_label == "vague green claim" and confidence > 0.5:
                score -= 20
                report.append(f"🤖 **AI Analysis:** Found **Vague Language** ({confidence:.1%}). (-20 pts)")

            elif top_label == "misleading" and confidence > 0.4:
                score -= 30
                report.append(f"🤖 **AI Analysis:** High risk of **Misleading Content** ({confidence:.1%}). (-30 pts)")

        # --- BONUS: Certified Brand Boost ---
        brand_lower = brand_input.lower()
        if brand_lower in certified_brands:
            score += 10
            report.append(f"✅ Certified Brand Detected ({certified_brands[brand_lower]}). (+10 pts)")

        # --- FINAL SCORE ---
        st.divider()
        final_score = max(0, min(100, score))
        st.header(f"Trust Score: {final_score}/100")

        # --- VERDICT ---
        if final_score >= 80:
            st.success("🌱Verdict: **LIKELY TRUSTWORTHY**")
        elif final_score >= 50:
            st.warning("Verdict: **PROCEED WITH CAUTION**")
        else:
            st.error("Verdict: **HIGH RISK OF GREENWASHING**")

        # --- REPORT ---
        st.subheader("Audit Details:")
        if report:
            for item in report:
                st.write(item)
        else:
            st.write("✅ No major issues detected.")