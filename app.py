import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# === NLP Library Setup ===
VF_DOCUMENTS = {
    "What is VF?": "Virtual Fencing (VF) is a technology that uses GPS and sensors to manage livestock without physical barriers.",
    "Cost of VF": "The cost of VF depends on the size of your ranch and the number of animals. It often includes hardware, software, and a subscription fee.",
    "Benefits of VF": "Benefits of VF include reduced labor costs, improved grazing efficiency, and better environmental management.",
    "Rotational Grazing": "Rotational grazing involves dividing pasture into smaller areas and rotating livestock to allow pastures to recover.",
    "Metal Fence Costs": "Metal fencing costs include material costs (posts, wire) and labor. Maintenance costs depend on fence quality and wear."
}

# Precompute embeddings for NLP
@st.cache_resource
def load_embeddings():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    docs = list(VF_DOCUMENTS.values())
    embeddings = model.encode(docs, convert_to_tensor=True)
    return model, docs, embeddings

model, docs, embeddings = load_embeddings()

def nlp_assistant(query):
    """
    Search VF_DOCUMENTS for relevant information based on user query.
    """
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, embeddings)
    top_result_idx = scores.argmax().item()
    return list(VF_DOCUMENTS.keys())[top_result_idx], docs[top_result_idx]

# === Modular Functions ===

def gather_inputs():
    """
    Collect rancher inputs for cost comparison.
    """
    st.subheader("Step 1: Tell Us About Your Ranch")
    ranch_size = st.number_input("How big is your ranch? (in acres)", min_value=0.0, step=1.0, format="%.2f")
    exterior_fence = st.number_input("How many miles of exterior fencing does your ranch currently have?", min_value=0.0, step=0.1, format="%.2f")
    Number_cattle = st.number_input("How many cattle are in your ranch?", min_value=0.0, step=10.0, format="%.2f")
    fence_condition = st.selectbox("What is the current condition of your fencing?", ("Excellent", "Good", "Fair", "Poor"))
    rotational_grazing = st.radio("Do you use rotational grazing?", ("Yes", "No"))
    annual_maintenance_cost = st.number_input("What is your annual fencing maintenance cost? (in dollars)", min_value=0.0, step=50.0, format="%.2f")
    ranch_size = float(ranch_size)
    exterior_fence = float(exterior_fence)
    annual_maintenance_cost = float(annual_maintenance_cost)
    Number_cattle = float(Number_cattle)


    return ranch_size, exterior_fence, Number_cattle,fence_condition, rotational_grazing, annual_maintenance_cost

def calculate_vf_cost(ranch_size, Number_cattle, grazing_benefit_per_acre, vf_cost_per_acre, subscription_cost):
    """
    Calculate the total cost of Virtual Fencing.
    """
    grazing_benefit = ranch_size * grazing_benefit_per_acre
    total_cost = 10000*2.5*(ranch_size/12000)*vf_cost_per_acre + subscription_cost*Number_cattle*20 - grazing_benefit
#   total_cost = 35.0 * ranch_size 
    return total_cost

def calculate_mf_cost(exterior_fence, mf_cost_per_mile, annual_maintenance_cost):
    """
    Calculate the total cost of Metal Fencing.
    """
    total_cost = (exterior_fence * mf_cost_per_mile) + annual_maintenance_cost*20
    return total_cost

def generate_comparison_table(vf_cost, mf_cost):
    """
    Generate a DataFrame for the cost comparison table.
    """
    data = {
        "Cost Factor": ["Initial Setup Cost", "Annual Maintenance Cost", "Labor Savings", "Grazing Benefits", "Total Cost"],
        "Virtual Fence": [f"${vf_cost:,.2f}", "-", "-", "-", f"${vf_cost:,.2f}"],
        "Metal Fence": [f"${mf_cost:,.2f}", "-", "-", "-", f"${mf_cost:,.2f}"]
    }
    return pd.DataFrame(data)

# === Main Application ===

def main():
    st.title("Virtual Fencing Cost Comparison with NLP Assistance")
    st.write("Hi! Welcome to the Virtual Fencing Assistant. You can ask questions about Virtual Fencing at any time.")

    # NLP Assistant
    st.subheader("Ask About Virtual Fencing")
    user_query = st.text_input("Type your question here:")
    if st.button("Ask"):
        if user_query:
            title, answer = nlp_assistant(user_query)
            st.write(f"**{title}**")
            st.write(answer)

    st.write("---")

    # Gather Inputs
    ranch_size, exterior_fence,  Number_cattle, fence_condition,rotational_grazing, annual_maintenance_cost = gather_inputs()

    # Cost Comparison
    if st.button("Compare Costs"):
        if ranch_size > 0 and exterior_fence > 0:
            # Constants (replace with actual values)
            grazing_benefit_per_acre = 20  # Example: $20 benefit per acre
            vf_cost_per_acre = 1         # Example: $15 per acre for VF
            vf_subscription_cost = 40    # Example: $500 annual subscription for VF
            mf_cost_per_mile = 15000       # Example: $5000 per mile for MF

            grazing_benefit_per_acre = float(grazing_benefit_per_acre)
            vf_cost_per_acre = float(vf_cost_per_acre)
            vf_subscription_cost = float(vf_subscription_cost)
            mf_cost_per_mile = float(mf_cost_per_mile)

            vf_cost = calculate_vf_cost(ranch_size, Number_cattle,grazing_benefit_per_acre, vf_cost_per_acre, vf_subscription_cost)
            mf_cost = calculate_mf_cost(exterior_fence, mf_cost_per_mile, annual_maintenance_cost)

            # Generate Comparison Table
            comparison_table = generate_comparison_table(vf_cost, mf_cost)

            # Display Results
            st.write("### Cost Comparison Table")
            st.table(comparison_table)

            if vf_cost < mf_cost:
                st.success("Virtual Fencing seems to be the better option for your ranch! 🎉")
            else:
                st.warning("Metal Fencing might be more cost-effective for your ranch. 🤔")
        else:
            st.error("Please provide valid inputs for all fields.")

if __name__ == "__main__":
    main()
