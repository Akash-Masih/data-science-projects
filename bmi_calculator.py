import streamlit as st 
 
st.title(" BMI Calculator") 
 
# Input weight (kg) and height (cm) 
weight = st.number_input("Enter your weight (kg):", min_value=1.0) 
height = st.number_input("Enter your height (cm):", min_value=1.0) 
 
if st.button("Calculate BMI"): 
    height_in_m = height / 100                     # Convert cm to meters 
    bmi = weight / (height_in_m ** 2) 
    st.success(f"Your BMI: {bmi:.2f}") 
 
    # BMI Categories 
    if bmi < 18.5: 
        st.warning("Underweight") 
    elif 18.5 <= bmi < 25: 
        st.success("Normal weight") 
    elif 25 <= bmi < 30: 
        st.warning("Overweight") 
    else: 
        st.error("Obese")