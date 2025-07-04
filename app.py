import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
from datetime import datetime
import requests
from openai import OpenAI  # Για μελλοντική αναβάθμιση

# 🔐 Φόρτωσε API Keys
load_dotenv()
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")  # Δωρεάν

# 🎯 Κατηγορίες επιχειρήσεων
business_types = [
    "Content Creator", "Travel Creator", "Καφετέρια", "Κομμωτήριο", "Σπα",
    "Fast Food / Εστιατόριο", "Προσωπικά Social", "Γυμναστήριο", 
    "Real Estate", "Κατάστημα Ρούχων"
]

# ⚙️ Ρυθμίσεις
st.set_page_config(page_title="Smart Social Tool", layout="centered", page_icon="📲")

# 📌 Sidebar με ρυθμίσεις
with st.sidebar:
    st.header("⚙️ Ρυθμίσεις")
    
    # 👉 Επιλογή AI Provider
    ai_provider = st.radio(
        "AI Provider",
        ["DeepInfra (Δωρεάν)", "OpenAI (Αναβάθμιση)"],
        index=0  # Προεπιλογή DeepInfra
    )
    
    if ai_provider == "DeepInfra (Δωρεάν)":
        model = st.selectbox(
            "Μοντέλο", 
            ["mistralai/Mixtral-8x7B-Instruct-v0.1", "meta-llama/Llama-2-70b-chat-hf"]
        )
    else:
        model = st.selectbox(
            "Μοντέλο", 
            ["gpt-3.5-turbo", "gpt-4"]
        )
    
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.7)

# 🎨 Κύρια σελίδα (το ίδιο όπως πριν)
st.title("📲 Smart Social Assistant")
st.subheader("Αυτόματη παραγωγή περιεχομένου για social media")

# 👉 Επιλογή επιχείρησης (το ίδιο)
selected_type = st.selectbox("Είδος επιχείρησης", business_types)

# 👉 Ανεβάζουμε media (εικόνα/βίντεο) (το ίδιο)
uploaded_file = st.file_uploader(
    "Ανέβασε μια εικόνα ή ένα video", 
    type=["png", "jpg", "jpeg", "mp4", "mov"]
)

# 👉 Προεπισκόπηση media (το ίδιο)
if uploaded_file:
    if uploaded_file.type.startswith('image'):
        st.image(uploaded_file, caption="Προεπισκόπηση εικόνας", use_container_width=True)
    elif uploaded_file.type.startswith('video'):
        st.video(uploaded_file)

# 👉 Περιγραφή περιεχομένου (το ίδιο)
description = st.text_area("Τι δείχνει περίπου το περιεχόμενο;", "")

# 🎯 Δημιουργία Post
if st.button("🎯 Δημιουργία Post") and uploaded_file:
    with st.spinner("⏳ Δημιουργία περιεχομένου..."):
        try:
            # 📝 Prompt engineering (το ίδιο)
            prompt = f"""
            Είμαι social media manager για {selected_type}.
            Το περιεχόμενο δείχνει: {description}

            Γράψε μου:
            1. Ένα ωραίο caption (2-3 προτάσεις) με emoji.
            2. 5 hashtags σχετικά με το niche.
            3. Μια πρόταση για τίτλο (για Reels/TikTok).
            """
            
            # 🚀 AI API Call (Αυτό αλλάζει)
            if ai_provider == "DeepInfra (Δωρεάν)":
                headers = {
                    "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "inputs": prompt,
                    "parameters": {"max_new_tokens": 500, "temperature": temperature}
                }
                response = requests.post(
                    f"https://api.deepinfra.com/v1/inference/{model}",
                    headers=headers,
                    json=data
                )
                content = response.json()[0]["generated_text"]
            else:
                client = OpenAI
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature
                )
                content = response.choices[0].message.content
            
            # ✅ Εμφάνιση αποτελέσματος (το ίδιο)
            st.success(f"✅ Έτοιμο (με {ai_provider})!")
            st.markdown("### ✍️ Περιγραφή Post")
            st.write(content)
            
            # 💾 Αποθήκευση σε TXT (το ίδιο)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"social_post_{timestamp}.txt"
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                tmp.write(content.encode('utf-8'))
                st.download_button(
                    label="📥 Download Post",
                    data=open(tmp.name, "rb").read(),
                    file_name=filename,
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"❌ Σφάλμα: {e}")
else:
    st.info("📝 Συμπλήρωσε πληροφορίες και ανέβασε περιεχόμενο για να ξεκινήσεις")