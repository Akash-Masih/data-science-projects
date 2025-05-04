import streamlit as st 
st.title(" Simple Calculator") 

# Input numbers 
num1 = st.number_input("Enter first number:") 
num2 = st.number_input("Enter second number:") 
 
# Operation selection 
operation = st.radio("Select operation:", ("Add", "Subtract", "Multiply", 
"Divide")) 
 
# Calculate result 
if st.button("Calculate"): 
    if operation == "Add": 
        result = num1 + num2 
    elif operation == "Subtract": 
        result = num1 - num2 
    elif operation == "Multiply": 
        result = num1 * num2 
    elif operation == "Divide": 
        result = num1 / num2 if num2 != 0 else "Error: Division by zero!" 
    st.success(f"Result: {result}")