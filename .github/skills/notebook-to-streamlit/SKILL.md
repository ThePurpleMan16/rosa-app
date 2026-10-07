---
name: notebook-to-streamlit
description: Use when turning analysis code from a Jupyter notebook into a
  Streamlit app, e.g. moving the Rosa's Pizza best-promise logic from the
  notebook into app.py. Covers extracting notebook functions into a plain
  Python module, mapping inputs to widgets, and rerun-safe state. Not for
  building a Streamlit app from scratch or for editing the notebook itself.
---

## Step 1 — Extract the pure core
- Copy the functions the app needs from the notebook into `rosa_logic.py`
  (e.g. `late_order_cost`, `best_promise`). Keep the logic identical.
- Remove print statements, test calls, `!pip` lines, and Colab-only code.
- No Streamlit imports in `rosa_logic.py`.
- Import ZONES, TIME_BLOCKS, COSTS, delivery_times from `starter`.
  Never redefine them.
- Check: `best_promise("Far West", "Fri/Sat eve", range(25, 75, 5), COSTS)`
  gives the same result as the notebook before moving on.

## Step 2 — Map notebook inputs to widgets

| Notebook input | Streamlit widget |
|---|---|
| zone | `st.selectbox` with options from ZONES |
| time_block | `st.selectbox` with options from TIME_BLOCKS |
| promises (range) | number inputs for min, max, and step |
| COSTS["margin"] | `st.number_input`, default = COSTS value |
| COSTS["churn_orders"] | `st.number_input`, default = COSTS value |
| COSTS["refund"] | `st.number_input`, default = COSTS value |
| print(result) | `st.metric` / `st.write`, outside the button block |

Build a new costs dict from the widget values and pass it to
`best_promise`. Defaults must match the notebook so both give the same
answer out of the box.

## Step 3 — State discipline
Streamlit reruns the whole script on every widget interaction.
- The `if st.button(...)` block only computes and saves the result to
  `st.session_state`.
- Displaying the result happens outside the button block, reading from
  `st.session_state`.

## Step 4 — Validate inputs
- If min >= max or step <= 0, show `st.error(...)` and `st.stop()`.
- If the recommended promise equals the min or max of the range, show a
  warning that the true best may lie outside the range.

## Done when
- [ ] `rosa_logic.py` reproduces the notebook's Part 2 result
- [ ] The app runs with `uv run streamlit run app.py`
- [ ] Clicking the button shows the recommended promise and net profit
- [ ] Changing another widget afterward doesn't make the result vanish