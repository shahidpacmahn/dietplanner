
import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import base64

# Load API key from Streamlit secrets
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error initializing Gemini API: {e}")
    st.stop()

def get_pdf_download_link(text, filename="diet_plan.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf_output = pdf.output(dest='S').encode('latin-1')
    b64 = base64.b64encode(pdf_output).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download Diet Plan as PDF</a>'

st.set_page_config(page_title="Diet-Planner", page_icon="🍎", layout="wide")

st.title("🍎 Shaik Bite 🍎")
st.markdown("### Your Personalized Diet Assistant!")

st.write("This app helps you generate a personalized diet plan based on your specific needs and preferences.")

if 'response' not in st.session_state:
    st.session_state.response = ''

with st.form("user_input_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Personal Information")
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.number_input("Height (cm)", min_value=50, max_value=300, value=170)
        weight = st.number_input("Weight (kg)", min_value=10, max_value=300, value=70)

    with col2:
        st.subheader("Dietary & Health Goals")
        dietary_restrictions = st.text_area("Dietary Restrictions (e.g., vegetarian, gluten-free)")
        health_goals = st.selectbox("Primary Goal", ["Build Muscle", "Getting Lean / Weight Loss"])
        physical_activity = st.selectbox(
            "Physical Activity Level",
            ["Lite (walking)", "Medium (3-4 days of exercise)", "Hardcore (intense daily exercise)"]
        )

    st.subheader("Current Meal Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### Breakfast")
        breakfast_food = st.text_input("What do you usually eat for breakfast?", key="breakfast_food")
        breakfast_quantity = st.text_input("How much of it do you eat?", key="breakfast_quantity")
        is_breakfast_cooked = st.checkbox("Is it cooked?", key="is_breakfast_cooked")

    with col2:
        st.markdown("#### Lunch")
        lunch_food = st.text_input("What do you usually eat for lunch?", key="lunch_food")
        lunch_quantity = st.text_input("How much of it do you eat?", key="lunch_quantity")
        is_lunch_cooked = st.checkbox("Is it cooked?", key="is_lunch_cooked")

    with col3:
        st.markdown("#### Dinner")
        dinner_food = st.text_input("What do you usually eat for dinner?", key="dinner_food")
        dinner_quantity = st.text_input("How much of it do you eat?", key="dinner_quantity")
        is_dinner_cooked = st.checkbox("Is it cooked?", key="is_dinner_cooked")

    st.subheader("Extra Food/Snacks")
    extra_food = st.text_area("Do you eat anything extra apart from the 3 main meals? If so, what and how much?")

    submitted = st.form_submit_button("Generate Diet Plan")

    if submitted:
        breakfast_cooked_status = "cooked" if is_breakfast_cooked else "not cooked"
        lunch_cooked_status = "cooked" if is_lunch_cooked else "not cooked"
        dinner_cooked_status = "cooked" if is_dinner_cooked else "not cooked"

        prompt = f"""
        Create a personalized diet plan for a {age}-year-old {gender}, with a height of {height} cm and weight of {weight} kg.
        Their physical activity level is: {physical_activity}.
        Their primary health goal is: {health_goals}.
        Dietary restrictions: {dietary_restrictions}

        Here is their current diet:
        - Breakfast: {breakfast_quantity} of {breakfast_food} ({breakfast_cooked_status}).
        - Lunch: {lunch_quantity} of {lunch_food} ({lunch_cooked_status}).
        - Dinner: {dinner_quantity} of {dinner_food} ({dinner_cooked_status}).
        - Extra food/snacks: {extra_food}

        Please provide a new, healthier diet plan.
        """
        with st.spinner("Generating your diet plan..."):
            response = model.generate_content(prompt)
            st.session_state.response = response.text

if st.session_state.response:
    st.markdown(st.session_state.response)
    st.markdown(get_pdf_download_link(st.session_state.response), unsafe_allow_html=True)
