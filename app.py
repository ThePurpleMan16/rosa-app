import streamlit as st

from starter import ZONES, TIME_BLOCKS, COSTS
from rosa_logic import best_promise, late_order_cost

st.title("Rosa's Pizza: best delivery promise")

# --- Inputs ---
col1, col2 = st.columns(2)
zone = col1.selectbox("Zone", ZONES, index=ZONES.index("Far West"))
time_block = col2.selectbox(
  "Time block", TIME_BLOCKS, index=TIME_BLOCKS.index("Fri/Sat eve")
)

st.subheader("Promised times to try (minutes)")
c1, c2, c3 = st.columns(3)
p_min = c1.number_input("Min", value=25, step=1)
p_max = c2.number_input("Max", value=70, step=1)
p_step = c3.number_input("Step", value=5, step=1)

st.subheader("Costs")
k1, k2, k3 = st.columns(3)
margin = k1.number_input(
  "Profit margin per order ($)", value=COSTS["margin"], min_value=0.0, step=0.5
)
churn = k2.number_input(
  "Churn per late order (lost orders)",
  value=COSTS["churn_orders"], min_value=0.0, step=0.1,
)
refund = k3.number_input(
  "Refund per late order ($)", value=COSTS["refund"], min_value=0.0, step=0.5
)

# --- Validation ---
if p_min >= p_max:
  st.error("Min must be less than max.")
  st.stop()
if p_step <= 0:
  st.error("Step must be greater than 0.")
  st.stop()

costs = {"refund": refund, "churn_orders": churn, "margin": margin}
promises = range(int(p_min), int(p_max) + 1, int(p_step))

# --- Compute (button only saves the result) ---
if st.button("Find best promise", type="primary"):
  promise, profit = best_promise(zone, time_block, promises, costs)
  st.session_state["result"] = {
    "zone": zone,
    "time_block": time_block,
    "promise": promise,
    "profit": float(profit),
    "late_cost": late_order_cost(costs),
    "min": promises[0],
    "max": promises[-1],
  }

# --- Display (outside the button block, survives reruns) ---
result = st.session_state.get("result")
if result:
  st.subheader(f"{result['zone']}, {result['time_block']}")
  m1, m2, m3 = st.columns(3)
  m1.metric("Recommended promise", f"{result['promise']} min")
  m2.metric("Net profit", f"${result['profit']:,.2f}")
  m3.metric("Cost per late order", f"${result['late_cost']:,.2f}")
  if result["promise"] in (result["min"], result["max"]):
    st.warning(
      "The recommended promise is at the edge of the range tried; "
      "the true best may lie outside it. Try widening the range."
    )
