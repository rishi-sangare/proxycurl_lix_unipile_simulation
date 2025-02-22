import streamlit as st

# 🎨 Custom Styling
st.markdown(
    """
    <style>
        .main {background-color: #000000;}
        .title {color: #2E86C1; font-size: 28px; font-weight: bold;}
        .subtitle {color: #1B4F72; font-size: 22px; font-weight: bold;}
        .highlight {color: #D35400; font-size: 20px; font-weight: bold;}
        .section {border-bottom: 2px solid #D5D8DC; padding-bottom: 10px;}
    </style>
    """,
    unsafe_allow_html=True
)

# 🏷️ Function Definitions
def calculate_lix_cost(credits):
    return credits * 0.098

def calculate_proxycurl_payg_cost(credits):
    payg_tiers = [(46297, 1000), (20834, 500), (3788, 100), (834, 50), (100, 10)]
    remaining = credits
    selected = []
    total_cost = 0
    
    for tier in payg_tiers:
        if remaining <= 0:
            break
        count = remaining // tier[0]
        if count > 0:
            selected.append((tier[0], tier[1], count))
            total_cost += tier[1] * count
            remaining -= tier[0] * count
    
    if remaining > 0:
        selected.append((payg_tiers[-1][0], payg_tiers[-1][1], 1))
        total_cost += payg_tiers[-1][1]
    
    return total_cost, selected

def calculate_proxycurl_subscription_cost(credits, months):
    subscription_plans = [
        (2500, 49), (25000, 299), (89900, 899), (211000, 1899)
    ]
    for plan in subscription_plans:
        if credits <= plan[0]:
            return plan[1] * months, plan[0]
    return 2000 * months, "Enterprise (>211000)"

def calculate_unipile_cost(months):
    return 55 * months

# 🎯 App Title
st.markdown('<p class="title">📊 API Pricing Simulator</p>', unsafe_allow_html=True)

# 🔽 User Inputs
with st.sidebar:
    st.markdown('<p class="subtitle">🔧 Adjust Parameters</p>', unsafe_allow_html=True)
    months = st.number_input("Select Duration (Months)", min_value=1, value=1)
    credits = st.number_input("Enter Required Credits", min_value=1, value=1000)

# 📌 Lix API Pricing
st.markdown('<p class="subtitle">🔹 Lix API</p>', unsafe_allow_html=True)
lix_cost = calculate_lix_cost(credits)
st.markdown(f"<p class='highlight'>💰 Total Cost: ${lix_cost:.2f} (Pay-as-you-go)</p>", unsafe_allow_html=True)

# 📌 ProxyCurl API Pricing
st.markdown('<div class="section"><p class="subtitle">🔹 ProxyCurl API</p></div>', unsafe_allow_html=True)

# 🛠️ Pay-as-you-go Plan
payg_cost, payg_combo = calculate_proxycurl_payg_cost(credits)
st.markdown(f"<p class='highlight'>💰 Optimal Pay-as-you-go Cost: ${payg_cost:.2f}</p>", unsafe_allow_html=True)

st.write("🔽 **Best Pay-as-you-go Plan Selection:**")
payg_table = "| Credits | Cost per Batch | Quantity | Total Cost |\n|---------|---------------|----------|------------|\n"
for tier in payg_combo:
    payg_table += f"| {tier[0]} | ${tier[1]} | {tier[2]}x | ${tier[1] * tier[2]} |\n"
st.markdown(payg_table, unsafe_allow_html=True)

# 📜 Subscription Plan
subscription_cost, chosen_plan = calculate_proxycurl_subscription_cost(credits, months)
st.markdown(f"<p class='highlight'>💰 Optimal Subscription Cost: ${subscription_cost:.2f}</p>", unsafe_allow_html=True)
st.write(f"✅ **Best Subscription Plan:** {chosen_plan} credits per month")

# 📌 Unipile API Pricing
st.markdown('<div class="section"><p class="subtitle">🔹 Unipile API</p></div>', unsafe_allow_html=True)
unipile_cost = calculate_unipile_cost(months)
st.markdown(f"<p class='highlight'>💰 Total Cost: ${unipile_cost:.2f}</p>", unsafe_allow_html=True)

# 🔹 Stop Streamlit from running indefinitely
st.stop()
