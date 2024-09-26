import streamlit as st
import numpy as np
from PIL import Image
import disease_backend  
import emotion_backend 
import assistant 

# CSS for styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
    
    /* General body style */
    .stApp {
        background: linear-gradient(120deg, #ffffff 0%, #f3f4f6 100%);
        font-family: 'Poppins', sans-serif;
        color: #2E4053;
    }

    /* Main title styling */
    h1, h2 {
        color: #1F618D;
        text-align: center;
        padding-top: 20px;
        font-weight: 700;
        font-size: 2.5rem;
    }

    /* Subheading styling */
    h3 {
        color: #154360;
        margin-top: 30px;
        font-weight: 500;
        font-size: 1.8rem;
    }

    /* Card for section containers */
    .card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }

    /* Button styling */
    .stButton button {
        background-color: #1F618D !important;
        color: white !important;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
    }

    /* Sidebar styling */
    sidebar .sidebar-content {
        background: linear-gradient(100deg, #ffffff 0%, #f3f4f6 100%) !important; /* Add !important */
        padding: 20px;
        border-radius: 10px; /* Optional: to match card style */
    }

    /* Text input field styling */
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #BDC3C7;
        padding: 10px;
        font-size: 16px;
    }

    /* General paragraph text */
    p {
        color: black;
        font-size: 16px;
    }
    
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Health Care AI</h1>", unsafe_allow_html=True)

# Sidebar for selecting between Emotion Detection and Disease Detection
section = st.sidebar.radio(
    "Select an option",
    ("🩺 Disease Detection", "😊 Emotion Detection","Health Assistant AI"),
)

# Disease Detection Section
if section == "🩺 Disease Detection":
    st.markdown("<h2>Disease Detection</h2>", unsafe_allow_html=True)
    #st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    symptoms_input = st.text_input("Enter symptoms separated by commas (e.g., itching, skin rash, fatigue):")

    if st.button("🔍 Predict Disease"):
        if symptoms_input:
            with st.spinner('Analyzing Symptoms...'):
                user_symptoms = [s.strip() for s in symptoms_input.split(',')]
                try:
                    predicted_disease = disease_backend.get_predicted_value(user_symptoms)
                    dis_des, precautions, medications, rec_diet, workout = disease_backend.helper(predicted_disease)

                    # Display disease prediction results
                    st.markdown(f"<h3>Predicted Disease: {predicted_disease}</h3>", unsafe_allow_html=True)
                    st.write(f"**Description**: {dis_des}")

                    st.write("### Precautions")
                    st.write("\n".join([f"- {pre}" for pre in precautions[0]]))

                    st.write("### Medications")
                    st.write("\n".join([f"- {med}" for med in medications]))

                    st.write("### Recommended Diet")
                    st.write("\n".join([f"- {diet}" for diet in rec_diet]))

                    st.write("### Suggested Workout")
                    st.write(workout)
                except KeyError:
                    st.error("Some symptoms might be misspelled or not recognized. Please try again.")
        else:
            st.error("Please enter symptoms to predict the disease.")

    st.markdown("</div>", unsafe_allow_html=True)

# Emotion Detection Section
elif section == "😊 Emotion Detection":
    st.markdown("<h2>Emotion Detection and Motivation</h2>", unsafe_allow_html=True)
    #st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    camera_option = st.radio("Select Input Method", ("Upload Image", "Use Camera"))

    if camera_option == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image for emotion detection...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            image_array = np.array(image)
    elif camera_option == "Use Camera":
        captured_image = st.camera_input("Capture an image for emotion detection")
        if captured_image is not None:
            image = Image.open(captured_image)
            image_array = np.array(image)

    if 'image_array' in locals() and image_array is not None:
        st.image(image_array, caption='Captured Image', use_column_width=True)

        with st.spinner('Analyzing Emotion...'):
            dominant_emotion = emotion_backend.detect_emotion(image_array)

        if dominant_emotion:
            st.markdown(f"<h3>Detected Emotion: {dominant_emotion.capitalize()}</h3>", unsafe_allow_html=True)
            quote = emotion_backend.get_motivational_content()
            st.success(f"**Motivational Quote:** {quote}")
        else:
            st.error("Could not detect any emotion. Please try again.")

    st.markdown("</div>", unsafe_allow_html=True)
elif section == "Health Assistant AI":
    # Adding a new section to the Streamlit app for health assistance
    st.markdown("<h2>💬 Health Assistance via AI</h2>", unsafe_allow_html=True)

    # User inputs their query
    user_query = st.text_input("Ask any health-related question (e.g., symptoms, treatments, fitness advice):")

    # User selects the type of health assistance they need
    category = st.radio(
        "What kind of advice are you looking for?",
        ("Symptoms & Diagnosis", "Nutrition & Diet", "Mental Health", "Fitness & Exercise")
    )

    if st.button("💡 Get AI Assistance"):
        if user_query and category:
            with st.spinner("Thinking..."):
                ai_response = get_health_assistance(user_query, category)
                st.markdown(f"**AI Response:**\n\n{ai_response}")
        else:
            st.error("Please enter a question and select a category.")
