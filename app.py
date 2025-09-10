# Install required packages (run once)
!pip install --quiet streamlit pyngrok

import os
import time
import subprocess
from pyngrok import ngrok

# Set your ngrok auth token (replace with your actual token)
NGROK_AUTH_TOKEN = "32HdDletE71AVZRIWsokJ1ecirm_4FZ56yBBSyxHsXTGR8aTf"
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Write a simple Streamlit app
app_code = """
import streamlit as st

st.title("🚀 EnviroScan Pollution Source Identifier")

city = st.text_input("Enter a city name", "Delhi")
if st.button("Analyze"):
    if not city.strip():
        st.warning("Please enter a valid city name.")
    else:
        st.success(f"Analyzing pollution sources for: {city}")
        st.markdown('''
        ### AI Analysis Results for **{city}** (Simulated)
        - **Main Pollutants:** PM2.5, NOx, SO2
        - **Likely Sources:**
          - Vehicle emissions
          - Industrial activity
          - Biomass/garbage burning
        - **Air Quality Index (AQI):** 185 (Unhealthy)
        - **Recommendation:** Limit outdoor activity. Use masks. Air purifiers recommended indoors.
        '''.format(city=city))
"""

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)
# Kill previous Streamlit instances
import platform
if platform.system() == "Windows":
    subprocess.run("taskkill /IM streamlit.exe /F", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
else:
    subprocess.run(["pkill", "-f", "streamlit"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# Disconnect any existing ngrok tunnels to avoid free-tier limits
for tunnel in ngrok.get_tunnels():
    ngrok.disconnect(tunnel.public_url)

# Start Streamlit app in the background
streamlit_process = subprocess.Popen(["streamlit", "run", "app.py"])

# Wait for Streamlit server to start
time.sleep(5)  # Increase if needed

# Open ngrok tunnel to port 8501
public_url = ngrok.connect(8501)
print(f"🌐 Your Streamlit app is live at: {public_url}")

# Keep process alive to maintain server & tunnel
try:
    streamlit_process.wait()
except KeyboardInterrupt:
    streamlit_process.terminate()
    ngrok.disconnect(public_url)
    print("Terminated Streamlit and ngrok tunnel.")
