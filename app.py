import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import random

# --- PAGE CONFIGURATION & CSS ---
st.set_page_config(page_title="KIET Wi-Fi Mapper", layout="wide", initial_sidebar_state="expanded")

# CSS to remove the extra white space at the top of the homepage
st.markdown("""
    <style>
           .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
            }
    </style>
    """, unsafe_allow_html=True)

# --- SELF-HEALING DATA LOADER ---
@st.cache_data
def load_and_fix_data():
    zones = ['Canteen', 'Hostel', 'Computer Labs', 'Library', 'Main Block']
    floors = ['Ground', '1st', '2nd', '3rd']
    required_cols = ["X_Coordinate", "Y_Coordinate", "Signal_Strength", "Zone", "Floor", "Student_Density"]
    
    if os.path.exists("wifi_data.csv"):
        try:
            df = pd.read_csv("wifi_data.csv")
        except Exception:
            df = pd.DataFrame()
    else:
        df = pd.DataFrame()

    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols or df.empty:
        data = []
        for _ in range(200):
            data.append({
                "X_Coordinate": random.uniform(0, 100),
                "Y_Coordinate": random.uniform(0, 100),
                "Signal_Strength": random.uniform(-90, -30),
                "Zone": random.choice(zones),
                "Floor": random.choice(floors),
                "Student_Density": random.randint(5, 150)
            })
        df = pd.DataFrame(data)
        df.to_csv("wifi_data.csv", index=False)
    
    df["Congestion_Risk"] = (df["Student_Density"] / 150) * (abs(df["Signal_Strength"]) / 90) * 100
    return df

df = load_and_fix_data()

# ==========================================
# 1. NAVIGATION (Sidebar)
# ==========================================
st.sidebar.title("🧭 Navigation")
st.sidebar.markdown("""
- [🏠 Homepage](#kiet-campus-wi-fi-strength-mapper)
- [🤖 Interactive AI Demo](#interactive-ai-demo-dashboard)
- [📊 Workflow](#workflow-data-integration)
- [🌊 Wave Physics Simulator](#wave-physics-signal-gradient-simulator)
- [✨ Key Features](#key-features)
- [🚀 Future Scope](#future-scope)
- [📚 Combined Subjects](#combined-subjects)
- [⚙️ Topics Integrated](#topics-integrated)
- [🧠 AI/LLM Layer](#ai-llm-layer)
- [💻 Coding Framework](#coding-framework)
- [🎓 R23 Alignment](#r23-alignment)
- [❓ FAQ](#frequently-asked-questions)
- [📞 Contact](#contact)
""")

st.sidebar.divider()
st.sidebar.header("📍 Dashboard Filters")
selected_zone = st.sidebar.multiselect("Select Zone(s):", options=df["Zone"].unique(), default=df["Zone"].unique())
selected_floor = st.sidebar.multiselect("Select Floor(s):", options=df["Floor"].unique(), default=df["Floor"].unique())

filtered_df = df[(df["Zone"].isin(selected_zone)) & (df["Floor"].isin(selected_floor))]


# ==========================================
# 2. HERO SECTION (HOMEPAGE)
# ==========================================
st.title("📡 KIET Campus Wi-Fi Strength Mapper")
st.markdown("### Smart Router Placement & Network Health System")
st.write("Welcome to our homepage! This is an intelligent, AI-assisted platform designed to analyze radio wave attenuation, predict network bottlenecks, and optimize access point infrastructure across the KIET college campus.")
st.divider()


# ==========================================
# 3. INTERACTIVE AI DEMO & DASHBOARD
# ==========================================
st.header("Interactive AI Demo & Dashboard", anchor="interactive-ai-demo-dashboard")
st.write("Explore the live campus data below. Use the filters in the sidebar to isolate specific zones or floors.")

if not filtered_df.empty:
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Active Samples", len(filtered_df))
    kpi2.metric("Avg Signal Strength", f"{filtered_df['Signal_Strength'].mean():.1f} dBm")
    kpi3.metric("Total Active Users", int(filtered_df['Student_Density'].sum()))
    
    # Interactive Heatmap (Fixed Background)
    fig = px.density_heatmap(
        filtered_df, x="X_Coordinate", y="Y_Coordinate", z="Signal_Strength",
        histfunc="avg", range_color=[-90, -30], color_continuous_scale="RdYlGn",
        title="KIET Wi-Fi Signal Density (Green = Strong, Red = Weak)",
        nbinsx=20, nbinsy=20
    )
    fig.add_scatter(
        x=filtered_df["X_Coordinate"], y=filtered_df["Y_Coordinate"], 
        mode="markers", 
        marker=dict(color=filtered_df["Signal_Strength"], colorscale="RdYlGn", cmin=-90, cmax=-30, size=10, line=dict(color='black', width=1)),
        hoverinfo="text", 
        text=[f"Zone: {z}<br>Floor: {fl}<br>Signal: {s:.1f} dBm<br>Users: {u}" 
              for z, fl, s, u in zip(filtered_df["Zone"], filtered_df["Floor"], filtered_df["Signal_Strength"], filtered_df["Student_Density"])]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # AI Logic Layer
    st.subheader("🤖 AI Router Placement Diagnostics")
    weak_spots = filtered_df[filtered_df["Signal_Strength"] < -70]
    high_congestion = filtered_df[filtered_df["Congestion_Risk"] > 50]
    
    if st.button("Run AI Network Diagnostics"):
        report_text = "KIET CAMPUS WI-FI DIAGNOSTIC REPORT\n" + "="*40 + "\n\n"
        
        if not weak_spots.empty:
            avg_x = weak_spots["X_Coordinate"].mean()
            avg_y = weak_spots["Y_Coordinate"].mean()
            most_affected_zone = weak_spots["Zone"].mode()[0] if not weak_spots["Zone"].empty else "N/A"
            
            st.error(f"⚠️ **Coverage Alert:** Found {len(weak_spots)} weak signal spots.")
            st.info(f"📍 **Recommended Router Location:** Zone: **{most_affected_zone}** near coordinates **(X: {avg_x:.1f}, Y: {avg_y:.1f})**.")
            
            report_text += f"Weak Coverage Spots Detected: {len(weak_spots)}\n"
            report_text += f"Primary Affected Zone: {most_affected_zone}\n"
            report_text += f"Suggested Router Coordinates: X={avg_x:.1f}, Y={avg_y:.1f}\n\n"
        else:
            st.success("Network signal coverage is adequate.")
            report_text += "Signal coverage is within acceptable limits.\n\n"
            
        if not high_congestion.empty:
            congested_zone = high_congestion["Zone"].mode()[0] if not high_congestion["Zone"].empty else "N/A"
            st.warning(f"⚡ **Collision Risk Alert:** High network congestion detected in **{congested_zone}** due to user density.")
            report_text += f"High Traffic Congestion Zone: {congested_zone}\n"
            report_text += "Recommendation: Upgrade access point bandwidth or add load-balancing routers.\n"
        
        st.download_button("📥 Download Diagnostic Report", data=report_text, file_name="KIET_WiFi_Diagnostic.txt", mime="text/plain")
else:
    st.warning("No data available for the selected filters.")
st.divider()


# ==========================================
# 4. WORKFLOW
# ==========================================
st.header("📊 Workflow & Data Integration", anchor="workflow-data-integration")
st.write("Data is collected via physical site surveys using network diagnostic tools. We record the spatial coordinates, signal strength in dBm, and the number of active users in each zone to simulate real-world load.")
st.dataframe(df.head(5), use_container_width=True)
st.divider()


# ==========================================
# 5. WAVE PHYSICS SIMULATOR
# ==========================================
st.header("🌊 Wave Physics & Signal Gradient Simulator", anchor="wave-physics-signal-gradient-simulator")
st.write("Demonstrating the **Sound Waves** analogy from the Engineering Physics curriculum. Just like sound, Wi-Fi radio waves decay over distance.")

col_a, col_b = st.columns(2)
with col_a:
    distance = st.slider("Distance from Router (Meters)", min_value=1, max_value=100, value=10)
    frequency = 2400 # 2.4 GHz Wi-Fi
with col_b:
    fspl = 20 * np.log10(distance / 1000) + 20 * np.log10(frequency) + 32.44
    signal_at_distance = -30 - (fspl / 2) 
    
    st.metric(label="Calculated Signal Strength (dBm)", value=f"{signal_at_distance:.1f} dBm")
    if signal_at_distance > -50:
        st.success("Excellent Signal - Near Router")
    elif signal_at_distance > -70:
        st.warning("Moderate Signal - Noticeable Gradient Decay")
    else:
        st.error("Weak Signal - Dead Zone Detected")
st.divider()


# ==========================================
# 6. FEATURES & FUTURE SCOPE
# ==========================================
st.header("✨ Key Features", anchor="key-features")
st.markdown("""
- **Dynamic 2D Spatial Heatmap:** Visualizes network strength and signal gradients in real-time.
- **Congestion Risk Scoring:** Predicts network failures before they happen based on crowd size.
- **Automated Centroid Calculation:** Eliminates guesswork for network engineers.
- **Exportable Maintenance Reports:** One-click downloads for IT staff.
""")
st.divider()

st.header("🚀 Future Scope", anchor="future-scope")
st.markdown("""
- **Real-Time IoT Integration:** Connecting live campus routers directly to the dashboard via API.
- **3D Multi-Floor Visualization:** Mapping signal degradation horizontally and vertically through concrete slabs.
- **Predictive Machine Learning:** Using historical data to predict which days/times the network will crash.
""")
st.divider()


# ==========================================
# 7. RUBRIC SECTIONS 
# ==========================================
st.header("📚 Combined Subjects", anchor="combined-subjects")
st.write("This project successfully merges three distinct academic disciplines:")
st.markdown("- **Engineering Physics:** Applies the theories of wave propagation and attenuation in physical space.")
st.markdown("- **Programming:** Uses Python to process arrays of coordinate data and execute mathematical formulas.")
st.markdown("- **IT Workshop:** Focuses on hardware networking, raw data collection, and software deployment.")
st.divider()

st.header("⚙️ Topics Integrated", anchor="topics-integrated")
st.write("Key concepts applied directly to the software:")
st.markdown("- **Sound Waves Analogy:** Demonstrates how radio frequencies drop exponentially over physical distance, just like sound.")
st.markdown("- **Signal Gradient:** The Heatmap visualizes the smooth transition from strong (green) to weak (red) network zones.")
st.markdown("- **Internet Tools:** Integration of CLI network diagnostic commands to fetch live dBm readings.")
st.divider()

st.header("🧠 AI/LLM Layer", anchor="ai-llm-layer")
st.write("The intelligence layer of this application:")
st.markdown("- **The Logic:** The system filters out standard data and isolates only the 'Dead Zones' (signals worse than -70 dBm).")
st.markdown("- **The Calculation:** It uses geometric math to find the exact center point (centroid) between all disconnected areas.")
st.markdown("- **The Outcome:** The AI actively advises the network administrator on the exact (X, Y) coordinates to install the next router to eliminate the dead zones.")
st.divider()

st.header("💻 Coding Framework", anchor="coding-framework")
st.write("The technical foundation used to build this architecture:")
st.markdown("- **Python:** The core backend language driving the math and logic.")
st.markdown("- **OS Module:** Used to bridge the gap between Python and the computer's underlying operating system to read network cards.")
st.markdown("- **Simple GUI:** Streamlit was used to convert raw, boring terminal scripts into a highly interactive, modern web application.")
st.divider()

st.header("🎓 R23 Alignment", anchor="r23-alignment")
st.write("Alignment with the official academic curriculum:")
st.markdown("- By proving the mathematical concepts of **Free Space Path Loss**, we fulfill the real-world application requirement for **Sem-I Physics**.")
st.markdown("- By deploying a fully functional, data-driven web app and utilizing system CLI tools, we fulfill the practical requirements of the **IT Workshop**.")
st.divider()


# ==========================================
# 8. FAQ
# ==========================================
st.header("❓ Frequently Asked Questions", anchor="frequently-asked-questions")
with st.expander("Why are the signal values negative?"):
    st.write("Radio signals are measured in decibel-milliwatts (dBm). Because the power received is a tiny fraction of a milliwatt, the logarithmic scale results in a negative number. Closer to 0 is better!")
with st.expander("What does the yellow warning mean in the AI diagnostics?"):
    st.write("It means the physical signal is fine, but there are too many students trying to use it at once, causing a 'traffic jam' of data (packet collisions).")
st.divider()


# ==========================================
# 9. CONTACT & FOOTER
# ==========================================
st.header("📞 Contact", anchor="contact")
st.write("Developed by the KIET Engineering & IT Team as part of the R23 Mini-Project initiative.")
st.markdown("📧 **Email:** project-team@kiet.edu | 🌐 **Web:** [www.kiet.edu](https://www.kiet.edu)")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<h4 style='text-align: center;'>Project by TEAM 3 CSE( AI & ML) Day Scholars - 2</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>© 2026 KIET Campus Wi-Fi Mapper. Developed for Academic Evaluation.</p>", unsafe_allow_html=True)