import streamlit as st
import openai
import os
from dotenv import load_dotenv
import tempfile
from datetime import datetime

# 🔐 Φόρτωσε το API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    model = st.selectbox("Μοντέλο", ["gpt-4", "gpt-3.5-turbo"])
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.7)

# 🎨 Κύρια σελίδα
st.title("📲 Smart Social Assistant")
st.subheader("Αυτόματη παραγωγή περιεχομένου για social media")

# 👉 Επιλογή επιχείρησης
selected_type = st.selectbox("Είδος επιχείρησης", business_types)

# 👉 Ανεβάζουμε media (εικόνα/βίντεο)
uploaded_file = st.file_uploader(
    "Ανέβασε μια εικόνα ή ένα video", 
    type=["png", "jpg", "jpeg", "mp4", "mov"]
)

# 👉 Προεπισκόπηση media
if uploaded_file:
    if uploaded_file.type.startswith('image'):
        st.image(uploaded_file, caption="Προεπισκόπηση εικόνας", use_column_width=True)
    elif uploaded_file.type.startswith('video'):
        st.video(uploaded_file)

# 👉 Περιγραφή περιεχομένου
description = st.text_area("Τι δείχνει περίπου το περιεχόμενο;", "")

# 🎯 Δημιουργία Post
if st.button("🎯 Δημιουργία Post") and uploaded_file:
    with st.spinner("⏳ Δημιουργία περιεχομένου..."):
        try:
            # 📝 Prompt engineering
            prompt = f"""
            Είμαι social media manager για {selected_type}.
            Το περιεχόμενο δείχνει: {description}

            Γράψε μου:
            1. Ένα ωραίο caption (2-3 προτάσεις) με emoji.
            2. 5 hashtags σχετικά με το niche.
            3. Μια πρόταση για τίτλο (για Reels/TikTok).
            """
            
            # 🚀 OpenAI API Call
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            
            content = response.choices[0].message.content
            
            # ✅ Εμφάνιση αποτελέσματος
            st.success("✅ Έτοιμο!")
            st.markdown("### ✍️ Περιγραφή Post")
            st.write(content)
            
            # 💾 Αποθήκευση σε TXT
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
