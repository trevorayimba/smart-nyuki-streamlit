import streamlit as st
import requests
import time

st.set_page_config(page_title="SMART NYUKI", layout="centered")

# === Epic Orange Honey Design ===
st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg,#ff6d00,#ff9e00,#ffb300);}
    h1 {font-size: 78px !important; font-weight: 900 !important; text-align: center;
        color: white; letter-spacing: 6px; text-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin: 20px 0 60px 0 !important;}
    .hive-card {
        background: rgba(255,255,255,0.18);
        backdrop-filter: blur(12px);
        border-radius: 25px;
        padding: 35px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.3);
        text-align: center;
        color: white;
    }
    .progress-bar {
        height: 40px; border-radius: 20px; overflow: hidden;
        background: rgba(255,255,255,0.25); position: relative; margin: 25px 0;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg,#ffab00,#ff6d00,#c43e00);
        transition: width 1.5s cubic-bezier(0.4,0,0.2,1);
    }
    .honey-pattern::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: repeating-linear-gradient(45deg,transparent,transparent 12px,
        rgba(255,255,255,0.15) 12px,rgba(255,255,255,0.15) 24px);
    }
    .stButton>button {
        width: 100%; padding: 22px; background:#c43e00; color:white;
        font-size:24px; font-weight:bold; border:none; border-radius:20px;
        box-shadow:0 12px 30px rgba(0,0,0,0.6); letter-spacing:2px;
    }
    .stButton>button:hover {
        background:#e64a19 !important; transform:translateY(-6px) !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>SMART NYUKI</h1>", unsafe_allow_html=True)

# Change this to your public Node-RED URL when deployed
BASE_URL = st.text_input("Node-RED URL", value="http://127.0.0.1:1880", help="Use your public Node-RED URL when live")

def get_hives():
    try:
        r = requests.get(f"{BASE_URL}/hives", timeout=5)
        return r.json() if r.status_code == 200 else {}
    except:
        return {}

def harvest_hive(id):
    try:
        requests.post(f"{BASE_URL}/harvest/{id}")
    except:
        pass

placeholder = st.empty()

while True:
    hives = get_hives()
    with placeholder.container():
        if hives:
            cols = st.columns(min(len(hives), 3))
            for idx, (hid, data) in enumerate(sorted(hives.items(), key=lambda x: int(x[0]))):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="hive-card">
                        <h2>Hive {hid}</h2>
                        <div class="progress-bar honey-pattern">
                            <div class="progress-fill" style="width: {data.get('level',0)}%"></div>
                        </div>
                        <p style="font-size:28px;margin:20px 0">
                            <strong>{data.get('weight_kg',0)} kg</strong> ({data.get('level',0)}% full)
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    if data.get('level', 0) >= 50:
                        if st.button("HARVEST HONEY", key=f"harvest_{hid}"):
                            harvest_hive(hid)
                            st.success(f"Hive {hid} harvested!")
                    else:
                        st.button("Not Ready", disabled=True, key=f"no_{hid}")
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("No hives detected. Make sure Node-RED is running and URL is correct.")

    time.sleep(4)
