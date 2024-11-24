import streamlit as st

st.title("Virtual Fencing Assistant")
st.write("Welcome to the Virtual Fencing Assistant!")
ranch_size = st.number_input("How big is your ranch? (in acres)", min_value=0.0, step=1.0)
exterior_fence = st.number_input("How many miles of exterior fencing does your ranch have?", min_value=0.0, step=0.1)

# Display the collected information
if st.button("Submit"):
    if ranch_size > 0 and exterior_fence > 0:
        st.success(f"Thank you! You have a ranch size of {ranch_size} acres and {exterior_fence} miles of exterior fencing.")
        st.write("Next, we'll ask about the condition of your fencing and other details.")
    else:
        st.error("Please provide valid inputs for both the ranch size and exterior fencing.")


