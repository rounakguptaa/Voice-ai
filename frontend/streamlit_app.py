import streamlit as st
import requests
import base64
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

SYLLABUS_MAP = {
    "Science": {
        "Chapter 1: Chemical Reactions and Equations": [
            "Section 1.1: Chemical Equations",
            "Section 1.2: Types of Chemical Reactions",
            "Section 1.3: Effects of Oxidation in Everyday Life"
        ],
        "Chapter 2: Acids, Bases and Salts": [
            "Section 2.1: Understanding the Chemical Properties of Acids and Bases",
            "Section 2.2: What do all Acids and all Bases have in Common?",
            "Section 2.3: How Strong are Acid or Base Solutions?",
            "Section 2.4: More about Salts"
        ],
        "Chapter 3: Metals and Non-metals": [
            "Section 3.1: Physical Properties of Metals and Non-Metals",
            "Section 3.2: Chemical Properties of Metals",
            "Section 3.3: How do Metals and Non-metals React?",
            "Section 3.4: Occurrence and Extraction of Metals",
            "Section 3.5: Corrosion and Prevention"
        ],
        "Chapter 4: Carbon and its Compounds": [
            "Section 4.1: Bonding in Carbon - The Covalent Bond",
            "Section 4.2: Versatile Nature of Carbon",
            "Section 4.3: Chemical Properties of Carbon Compounds",
            "Section 4.4: Some Important Carbon Compounds - Ethanol and Ethanoic Acid",
            "Section 4.5: Soaps and Detergents"
        ],
        "Chapter 5: Life Processes": [
            "Section 5.1: What are Life Processes?",
            "Section 5.2: Nutrition (Autotrophic & Heterotrophic)",
            "Section 5.3: Respiration",
            "Section 5.4: Transportation (Humans & Plants)",
            "Section 5.5: Excretion"
        ],
        "Chapter 6: Control and Coordination": [
            "Section 6.1: Animals - Nervous System & Reflex Actions",
            "Section 6.2: Coordination in Plants",
            "Section 6.3: Hormones in Animals"
        ],
        "Chapter 7: How do Organisms Reproduce?": [
            "Section 7.1: Do Organisms Create Exact Copies of Themselves?",
            "Section 7.2: Modes of Reproduction used by Single Organisms",
            "Section 7.3: Sexual Reproduction in Flowering Plants & Humans"
        ],
        "Chapter 8: Heredity": [
            "Section 8.1: Accumulation of Variation during Reproduction",
            "Section 8.2: Heredity & Inherited Traits",
            "Section 8.3: Mendel's Contribution & Rules for Inheritance of Traits",
            "Section 8.4: Sex Determination"
        ],
        "Chapter 9: Light – Reflection and Refraction": [
            "Section 9.1: Reflection of Light & Spherical Mirrors",
            "Section 9.2: Refraction of Light & Lenses",
            "Section 9.3: Lens Formula, Magnification, and Power of Lenses"
        ],
        "Chapter 10: The Human Eye and the Colourful World": [
            "Section 10.1: Human Eye & Power of Accommodation",
            "Section 10.2: Defects of Vision and their Correction",
            "Section 10.3: Refraction of Light through a Prism",
            "Section 10.4: Atmospheric Refraction & Scattering of Light"
        ],
        "Chapter 11: Electricity": [
            "Section 11.1: Electric Current, Circuit, and Potential Difference",
            "Section 11.2: Ohm's Law & Factors on which Resistance Depends",
            "Section 11.3: Resistance of System of Resistors (Series & Parallel)",
            "Section 11.4: Heating Effect of Electric Current & Electric Power"
        ],
        "Chapter 12: Magnetic Effects of Electric Current": [
            "Section 12.1: Magnetic Field and Field Lines",
            "Section 12.2: Magnetic Field due to Current-carrying Conductor",
            "Section 12.3: Force on Current-carrying Conductor in Magnetic Field",
            "Section 12.4: Electric Motor & Electromagnetic Induction",
            "Section 12.5: Domestic Electric Circuits"
        ],
        "Chapter 13: Our Environment": [
            "Section 13.1: Ecosystem - What are its Components?",
            "Section 13.2: Food Chains and Food Webs",
            "Section 13.3: How do our Activities Affect the Environment?"
        ]
    },
    "Mathematics": {
        "Chapter 1: Real Numbers": [
            "Section 1.1: Introduction",
            "Section 1.2: The Fundamental Theorem of Arithmetic",
            "Section 1.3: Revisiting Irrational Numbers"
        ],
        "Chapter 2: Polynomials": [
            "Section 2.1: Introduction",
            "Section 2.2: Geometrical Meaning of the Zeroes of a Polynomial",
            "Section 2.3: Relationship between Zeroes and Coefficients of a Quadratic Polynomial"
        ],
        "Chapter 3: Pair of Linear Equations in Two Variables": [
            "Section 3.1: Introduction",
            "Section 3.2: Graphical Method of Solution of Pair of Linear Equations",
            "Section 3.3: Algebraic Methods of Solving (Substitution & Elimination)"
        ],
        "Chapter 4: Quadratic Equations": [
            "Section 4.1: Introduction",
            "Section 4.2: Solution of Quadratic Equation by Factorisation",
            "Section 4.3: Nature of Roots (Discriminant Method)"
        ],
        "Chapter 5: Arithmetic Progressions": [
            "Section 5.1: Introduction",
            "Section 5.2: Arithmetic Progressions definition",
            "Section 5.3: nth Term of an AP",
            "Section 5.4: Sum of First n Terms of an AP"
        ],
        "Chapter 6: Triangles": [
            "Section 6.1: Introduction",
            "Section 6.2: Similar Figures",
            "Section 6.3: Similarity of Triangles",
            "Section 6.4: Criteria for Similarity of Triangles"
        ],
        "Chapter 7: Coordinate Geometry": [
            "Section 7.1: Introduction",
            "Section 7.2: Distance Formula",
            "Section 7.3: Section Formula"
        ],
        "Chapter 8: Introduction to Trigonometry": [
            "Section 8.1: Trigonometric Ratios",
            "Section 8.2: Ratios of Some Specific Angles (0, 30, 45, 60, 90)",
            "Section 8.3: Trigonometric Identities"
        ],
        "Chapter 9: Some Applications of Trigonometry": [
            "Section 9.1: Introduction",
            "Section 9.2: Heights and Distances (Angle of Elevation & Depression)"
        ],
        "Chapter 10: Circles": [
            "Section 10.1: Tangent to a Circle",
            "Section 10.2: Number of Tangents from a Point on a Circle"
        ],
        "Chapter 11: Areas Related to Circles": [
            "Section 11.1: Areas of Sector and Segment of a Circle"
        ],
        "Chapter 12: Surface Areas and Volumes": [
            "Section 12.1: Surface Area of Combination of Solids",
            "Section 12.2: Volume of Combination of Solids"
        ],
        "Chapter 13: Statistics": [
            "Section 13.1: Mean of Grouped Data",
            "Section 13.2: Mode of Grouped Data",
            "Section 13.3: Median of Grouped Data"
        ],
        "Chapter 14: Probability": [
            "Section 14.1: Probability - A Theoretical Approach"
        ]
    }
}

st.set_page_config(

    page_title="GuruAI - Smart Board Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern Smart Board aesthetics
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stAppHeader {
        background-color: transparent;
    }
    .css-1d3av2a {
        background-color: #1e293b;
    }
    .smart-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #38bdf8;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 25px -5px rgba(56, 189, 248, 0.1);
        margin-bottom: 20px;
    }
    .quiz-card {
        background: #1e1b4b;
        border: 2px solid #818cf8;
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.title("🎓 GuruAI: Voice Teaching Assistant")
st.caption("Haryana Government Smart Board System • NCERT Class 10 Science & Mathematics")

# Sidebar Controls
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/teacher.png", width=120)
    st.header("⚙️ Classroom Settings")
    
    class_option = st.selectbox("📚 Select Class", ["10"], index=0, help="Currently Class 10 NCERT curriculum is active.")
    subject_option = st.selectbox("🔬 Select Subject", ["Science", "Mathematics"], index=0)
    mode_option = st.radio("🎯 Assistant Mode", ["Explanation", "Interactive Quiz"], index=0)
    
    st.divider()
    st.markdown(f"**System Status:** 🟢 Backend Online (`{BACKEND_URL}`)")

# Main Content Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("🎙️ Ask GuruAI (Live Microphone)")
    
    # Live recording widget
    voice_query_file = st.audio_input("Record your question (e.g. 'What is respiration?' or 'Explain real numbers')")
    
    # Fallback manual file uploader
    audio_file = st.file_uploader("Or upload an existing WAV audio file", type=["wav", "mp3", "m4a"])
    
    # Determine the audio input source
    active_audio = voice_query_file if voice_query_file is not None else audio_file
    
    if st.button("🚀 Ask Virtual Teacher", type="primary", use_container_width=True):
        if active_audio is None:
            st.warning("⚠️ Kripya record karein ya check karein ki microphone enabled hai!")
        else:
            with st.spinner("⏳ Transcribing audio and searching NCERT vector store..."):
                try:
                    # Package the audio file
                    file_name = active_audio.name if hasattr(active_audio, 'name') else "query.wav"
                    files = {"file": (file_name, active_audio.getvalue(), "audio/wav")}
                    
                    data = {
                        "class_id": class_option,
                        "subject": subject_option.lower(),
                        "mode": "quiz" if mode_option == "Interactive Quiz" else "explain"
                    }
                    
                    response = requests.post(f"{BACKEND_URL}/process-voice", files=files, data=data, timeout=60)
                    
                    if response.status_code == 200:
                        res_json = response.json()
                        st.session_state["result"] = res_json
                        st.success("✅ Complete!")
                    else:
                        st.error(f"❌ Server Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"❌ Backend connection failed: {e}")

    # Display Transcribed Query if available
    if "result" in st.session_state:
        res = st.session_state["result"]
        st.info(f"🗣️ **GuruAI Transcribed:** '{res.get('user_query', '')}'")

    st.divider()
    st.subheader("📖 Browse & Learn Chapters")
    
    # Get active subject syllabus
    subject_map = SYLLABUS_MAP.get(subject_option, {})
    chapters = list(subject_map.keys())
    
    selected_chapter = st.selectbox("📚 Select Chapter", chapters)
    sections = subject_map.get(selected_chapter, [])
    
    selected_section = st.selectbox("📝 Select Section / Sub-section", sections)
    
    if st.button("👨‍🏫 Explain Selected Section", use_container_width=True):
        # Extract clean chapter & section titles to bypass search query filler words
        clean_chapter = selected_chapter.split(":")[-1].strip() if ":" in selected_chapter else selected_chapter
        clean_section = selected_section.split(":")[-1].strip() if ":" in selected_section else selected_section
        text_query = f"{clean_chapter} {clean_section}"
        
        with st.spinner(f"⏳ Querying GuruAI about '{clean_section}'..."):
            try:
                data = {
                    "text_query": text_query,
                    "class_id": class_option,
                    "subject": subject_option.lower(),
                    "mode": "quiz" if mode_option == "Interactive Quiz" else "explain"
                }
                # Pass dummy file to guarantee multipart/form-data structure
                files = {"file": ("query.wav", b"", "audio/wav")}
                
                response = requests.post(f"{BACKEND_URL}/process-voice", files=files, data=data, timeout=60)

                
                if response.status_code == 200:
                    res_json = response.json()
                    st.session_state["result"] = res_json
                    st.success("✅ Explanation Loaded!")
                else:
                    st.error(f"❌ Server Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"❌ Backend connection failed: {e}")


with col2:
    st.subheader("💡 GuruAI Interactive Board")
    
    if "result" in st.session_state:
        res = st.session_state["result"]
        blocked = res.get("blocked_flag", False)
        
        if blocked:
            st.error("🛡️ Guardrail Triggered - Off-Topic Question")
            st.markdown(f"**GuruAI Response:**\n{res.get('text_response')}")
            audio_url = res.get("audio_url")
            if audio_url:
                # Play immediately
                autoplay_html = f'<audio src="{audio_url}" autoplay></audio>'
                st.markdown(autoplay_html, unsafe_allow_html=True)
                st.audio(audio_url)
        else:
            # Response Text
            st.markdown(res.get("text_response", ""))
            
            # Audio Player with Autoplay
            audio_url = res.get("audio_url")
            if audio_url:
                # Inject HTML with autoplay enabled
                autoplay_html = f'<audio src="{audio_url}" autoplay></audio>'
                st.markdown(autoplay_html, unsafe_allow_html=True)
                # Show native player so the user can pause/replay
                st.audio(audio_url)
                
            # Visual Summary Image Card
            visual_b64 = res.get("visual_base64")
            if visual_b64:
                st.image(visual_b64, caption="📊 Concept Summary Card", use_container_width=True)
                
            # Quiz Card
            quiz_data = res.get("quiz_data")
            if quiz_data and mode_option == "Interactive Quiz":
                st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
                st.markdown(f"### ❓ Quick Quiz: {quiz_data.get('question')}")
                opts = quiz_data.get("options", {})
                
                selected_opt = st.radio(
                    "Select your answer:",
                    options=list(opts.keys()),
                    format_func=lambda x: f"{x}) {opts[x]}"
                )
                
                if st.button("Submit Answer"):
                    if selected_opt == quiz_data.get("answer"):
                        st.balloons()
                        st.success(f"🎉 Sahi Jawab! Option ({selected_opt}) is correct!")
                    else:
                        st.error(f"❌ Nayi koshish karein! Correct option is ({quiz_data.get('answer')}).")
                    st.info(f"💡 **Explanation:** {quiz_data.get('explanation')}")
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👋 Use the microphone on the left to ask a question, and see/hear GuruAI explain topics live!")

