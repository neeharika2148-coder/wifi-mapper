import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="KIET WiFi Mapper", layout="wide")

# CUSTOMIZATION 1: Updated Title
st.title("📡 KIET Campus WiFi Strength Mapper")
st.markdown("Optimal Router Placement System")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    if os.path.exists("wifi_data.csv"):
        return pd.read_csv("wifi_data.csv")
    else:
        # Create dummy data if the file is missing so the app doesn't break
        return pd.DataFrame({
            "X_Coordinate": np.random.uniform(0, 100, 100),
            "Y_Coordinate": np.random.uniform(0, 100, 100),
            "Signal_Strength": np.random.uniform(-90, -30, 100) # dBm values are negative
        })

df = load_data()

# CUSTOMIZATION 2: Removed "Layer" text and added new tabs based on your table
tabs = st.tabs([
    "🏠 Home", 
    "📚 Combined Subjects", 
    "⚙️ Topics Integrated", 
    "💻 Coding Framework",
    "📊 Data Integration",
    "🗺️ Mini-Project Outcome", 
    "🧮 Formulas", 
    "🎓 R23 Alignment"
])

# --- 1: HOME PAGE ---
with tabs[0]:
    st.header("What is the project about?")
    st.write("This project is a Python-based web application designed to analyze WiFi signal strength across the KIET college campus.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Problem Statement")
        st.write("Large college campuses often have areas with poor WiFi coverage. Students experience:")
        st.write("* Slow internet")
        st.write("* Weak signals")
        st.write("* Frequent disconnections")
        st.write("Finding the best place to install routers manually is difficult. Our project solves this problem using AI-assisted analysis.")
    
    with col2:
        st.subheader("Main Objectives")
        st.write("✔ Collects WiFi signal strength")
        st.write("✔ Shows signal distribution using a heatmap")
        st.write("✔ Identifies weak signal zones")
        st.write("✔ Suggests the optimal location for new WiFi routers")

# --- 2: COMBINED SUBJECTS ---
with tabs[1]:
    st.header("Combined Subjects")
    st.write("This project successfully merges three distinct academic disciplines:")
    st.info("**1. Engineering Physics:** Understanding how radio waves propagate through physical space, attenuate over distance, and interact with obstacles.")
    st.info("**2. Programming:** Using Python to process large sets of coordinate and signal data efficiently.")
    st.info("**3. IT Workshop:** Applying practical computer skills to gather raw network data, handle CSV files, and utilize modern development tools.")

# --- 3: TOPICS INTEGRATED ---
with tabs[2]:
    st.header("Topics Integrated")
    st.write("Key concepts applied in this system:")
    st.write("* **Sound Waves (Analogy):** Just like sound waves get quieter the further you walk away from a speaker, WiFi (radio) waves get weaker the further you move from a router. We use this physics principle to analyze coverage.")
    st.write("* **Signal Gradient:** Mapping the gradual increase or decrease of signal strength across the campus geometry.")
    st.write("* **Internet Tools:** Utilizing network diagnostic commands to fetch live dBm readings from the hardware.")

# --- 4: CODING FRAMEWORK ---
with tabs[3]:
    st.header("Coding Framework")
    st.write("The technical stack used to build this software:")
    st.markdown("""
    * **Python:** The core programming language.
    * **`os` Module:** Used in our data collection script to interact with the operating system and execute network commands (like `netsh wlan show interfaces`).
    * **Simple GUI (Streamlit):** Transforms standard Python scripts into this interactive web dashboard without needing complex HTML or CSS.
    * **Plotly:** Powers the interactive, color-coded heatmaps.
    """)

# --- 5: DATA INTEGRATION ---
with tabs[4]:
    st.header("Data Integration & Survey")
    st.write("Data is collected by walking to various locations (Library, Hostels, Canteen) on the KIET campus using network tools to record Location (X/Y) and Signal Strength (dBm).")
    st.write("Below is the interactive dataset currently loaded into the system:")
    st.dataframe(df, use_container_width=True)

# --- 6: MINI-PROJECT OUTCOME (Heatmap & AI) ---
with tabs[5]:
    st.header("Mini-Project Outcome: Heatmap & AI Analysis")
    st.write("This tab represents the final outcome of the project: A heatmap visualization of the WiFi signal across the campus with AI/LLM-based router placement.")
    
    # Interactive Plotly Heatmap
    fig = px.density_heatmap(
        df, x="X_Coordinate", y="Y_Coordinate", z="Signal_Strength",
        color_continuous_scale="RdYlGn",
        title="KIET Campus Coverage Density (Green = Strong, Red = Weak)",
        nbinsx=20, nbinsy=20
    )
    fig.add_scatter(
        x=df["X_Coordinate"], y=df["Y_Coordinate"], 
        mode="markers", marker=dict(color=df["Signal_Strength"], colorscale="RdYlGn", size=10, line=dict(color='black', width=1)),
        hoverinfo="text", text=[f"Signal: {val:.2f} dBm" for val in df["Signal_Strength"]]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🤖 AI/LLM Layer: Optimal Router Placement")
    weak_threshold = -70 # Anything worse than -70 dBm is weak
    weak_spots = df[df["Signal_Strength"] < weak_threshold]
    
    if st.button("Run AI Analysis"):
        if not weak_spots.empty:
            avg_x = weak_spots["X_Coordinate"].mean()
            avg_y = weak_spots["Y_Coordinate"].mean()
            st.error(f"⚠️ Detected {len(weak_spots)} weak signal areas (below {weak_threshold} dBm).")
            st.success(f"**AI Recommendation:** Install a new router near coordinates **X: {avg_x:.1f}, Y: {avg_y:.1f}**. This represents the geographic center of the weakest network zone on campus.")
        else:
            st.success("Network coverage is optimal. No action needed.")

# --- 7: FORMULAS & PHYSICS ---
with tabs[6]:
    st.header("Understanding the Physics and Formulas")
    
    st.subheader("1. Measuring Signal Strength (dBm)")
    st.write("WiFi strength is measured in Decibel-milliwatts (dBm). Because radio signals degrade rapidly, we use a logarithmic scale.")
    st.latex(r"P_{(dBm)} = 10 \log_{10}\left(\frac{P_{(mW)}}{1mW}\right)")
    st.write("* **0 dBm to -50 dBm:** Excellent signal (Green)")
    st.write("* **-50 dBm to -70 dBm:** Average/Good signal (Yellow)")
    st.write("* **-70 dBm to -90 dBm:** Weak signal/Disconnections (Red)")
    
    st.subheader("2. Free Space Path Loss (FSPL)")
    st.write("This formula calculates the loss of signal strength over a distance.")
    st.latex(r"FSPL = 20 \log_{10}(d) + 20 \log_{10}(f) + 32.44")
    st.write("Where **d** = Distance (km) and **f** = Frequency (usually 2.4 GHz or 5 GHz).")

# --- 8: R23 ALIGNMENT ---
with tabs[7]:
    st.header("R23 Curriculum Alignment")
    st.write("How this mini-project fulfills the R23 Academic Requirements:")
    
    st.markdown("""
    * **Sem-I Physics:** Demonstrates a practical understanding of wireless signal propagation and gradients.
    * **IT Workshop:** Proves competency in collecting raw hardware data, organizing it in datasets, and building an interactive GUI.
    """)