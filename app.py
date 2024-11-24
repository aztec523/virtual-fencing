import streamlit as st

st.title("Virtual Fencing Assistant")
st.write("Welcome to the Virtual Fencing Assistant!")
ranch_size = st.number_input("How big is your ranch? (in acres)", min_value=0.0, step=1.0)
exterior_fence = st.number_input("How many miles of exterior fencing does your ranch have?", min_value=0.0, step=0.1)
if st.button("Submit"):
    st.success(f"Ranch Size: {ranch_size} acres, Exterior Fence: {exterior_fence} miles")
