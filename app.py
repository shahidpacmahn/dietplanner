import streamlit as st
import google.generativeai as genai

# Load API key from Streamlit secrets
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error initializing Gemini API: {e}")
    st.stop()

st.set_page_config(page_title="Shaik Bite", page_icon="🥗", layout="wide")

# --- Custom CSS for a futuristic, healthy lifestyle theme ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

body {
    color: #f1f1f1;
    background-color: #0e1117;
    font-family: 'Roboto', sans-serif;
}
.stApp {
    background-image: linear-gradient(to right top, #051937, #004d7a, #008793, #00bf72, #a8eb12);
}
.st-container {
    border: 2px solid #4CAF50;
    border-radius: 10px;
    padding: 2rem;
    background-color: rgba(0, 0, 0, 0.5);
    margin-bottom: 2rem;
}
.st-subheader {
    color: #4CAF50;
    font-weight: 700;
}
.st-form {
    border: none;
}
.st-button>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 5px;
    padding: 0.5rem 1rem;
    border: none;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #a8eb12;'>🥗 Shaik Bite 🥩</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #f1f1f1;'>Your Futuristic Personalized Diet Assistant!</h3>", unsafe_allow_html=True)

with st.container():
    st.subheader("👤 Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        height = st.number_input("Height (cm)", min_value=50, max_value=300, value=170)
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", min_value=10, max_value=300, value=70)

with st.container():
    st.subheader("🎯 Dietary & Health Goals")
    dietary_restrictions = st.text_area("Dietary Restrictions (e.g., vegetarian, gluten-free)")
    health_goals = st.selectbox("Primary Goal", ["Build Muscle", "Getting Lean / Weight Loss"])
    physical_activity = st.selectbox(
        "Physical Activity Level",
        ["Lite exercise", "Medium (3-4 days of exercise)", "Hardcore (intense daily exercise)"]
    )

with st.container():
    st.subheader("🍽️ Current Meal Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Breakfast**")
        breakfast_food = st.text_input("What do you usually eat?", key="breakfast_food")
        breakfast_quantity = st.text_input("How much?", key="breakfast_quantity")
        is_breakfast_cooked = st.checkbox("Cooked?", key="is_breakfast_cooked")

    with col2:
        st.markdown("**Lunch**")
        lunch_food = st.text_input("What do you usually eat?", key="lunch_food")
        lunch_quantity = st.text_input("How much?", key="lunch_quantity")
        is_lunch_cooked = st.checkbox("Cooked?", key="is_lunch_cooked")

    with col3:
        st.markdown("**Dinner**")
        dinner_food = st.text_input("What do you usually eat?", key="dinner_food")
        dinner_quantity = st.text_input("How much?", key="dinner_quantity")
        is_dinner_cooked = st.checkbox("Cooked?", key="is_dinner_cooked")

with st.container():
    st.subheader(" snacking habits")
    extra_food = st.text_area("Do you eat anything extra apart from the 3 main meals? If so, what and how much?")

if st.button("Generate My Diet Plan"):
    with st.spinner("Generating your personalized diet plan..."):
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

        Please provide a new, healthier diet plan. The plan should be futuristic and exciting.
        """
        response = model.generate_content(prompt)
        st.markdown(response.text)

st.markdown("---")
st.markdown("<div style='text-align: center;'>© 2024 Shaik Bite. All rights reserved.</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>Developed by pacman</div>", unsafe_allow_html=True)