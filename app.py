# ... previous app.py code above ...

st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")

filter_columns = [
    "company", "business_unit", "department", "function",
    "zone", "area", "band", "employment_type"
]
emp_df = data['employee_master']
filter_dict = {}

with st.sidebar.expander("Show Filters", expanded=False):
    n_cols = 2  # Two filters per row
    for row_start in range(0, len(filter_columns), n_cols):
        cols = st.columns(n_cols)
        for i in range(n_cols):
            col_idx = row_start + i
            if col_idx >= len(filter_columns):
                continue
            col = filter_columns[col_idx]
            options = sorted([str(x) for x in emp_df[col].dropna().unique()])
            key = f"sidebar_{col}"

            # --- Custom: Only show pills if not all selected, else show "All" label ---
            selected = st.session_state.get(key, options)
            with cols[i]:
                st.write(f"**{col.replace('_', ' ').title()}**")
                if set(selected) == set(options):
                    st.text_input(" ", value="All", key=f"all_{col}", disabled=True, label_visibility="collapsed")
                    # For backend: still pass all options as selected
                    filter_dict[col] = options
                else:
                    chosen = st.multiselect(
                        "",
                        options=options,
                        default=selected,
                        key=key,
                        label_visibility="collapsed"
                    )
                    filter_dict[col] = chosen
                    st.session_state[key] = chosen

# --- Apply filter to all reports globally ---
filtered_emp = filter_dataframe(emp_df, filter_dict)
filtered_emp = ensure_datetime(filtered_emp, ['date_of_joining', 'date_of_exit', 'date_of_birth'])
data['employee_master'] = filtered_emp

# ... rest of app.py unchanged ...
