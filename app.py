import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Tourism Dashboard")

st.write(
    """
    This dashboard explores tourism development across towns using the Tourism Index
    and the availability of tourism-related facilities such as hotels, cafes,
    restaurants, and guest houses. Use the filters below to compare different groups
    of towns and see how tourism infrastructure relates to tourism development.
    """
)

# Load dataset
df = pd.read_csv("dataset.csv")

# -----------------------------
# Interaction 1: Facility type
# -----------------------------
facility = st.selectbox(
    "Choose a tourism facility",
    ["Hotels", "Cafes", "Restaurants", "Guest Houses"]
)

facility_columns = {
    "Hotels": "Total number of hotels",
    "Cafes": "Total number of cafes",
    "Restaurants": "Total number of restaurants",
    "Guest Houses": "Total number of guest houses"
}

selected_column = facility_columns[facility]

with st.expander("Why use the facility dropdown?"):
    st.write(
        """
        This dropdown helps answer the question: how does a specific type of tourism
        infrastructure relate to tourism development? I used a dropdown because it
        allows the user to focus on one facility at a time instead of showing several
        separate charts at once. This reduces clutter and helps focus attention on the
        selected comparison.
        """
    )

# -----------------------------
# Interaction 2: Availability
# -----------------------------
availability = st.radio(
    f"Show towns based on {facility.lower()} availability",
    ["All towns", f"With {facility}", f"Without {facility}"]
)

if availability == f"With {facility}":
    filtered_df = df[df[selected_column] > 0]

elif availability == f"Without {facility}":
    filtered_df = df[df[selected_column] == 0]

else:
    filtered_df = df.copy()

with st.expander("Why use the availability filter?"):
    st.write(
        """
        This filter helps answer the question: how do towns with the selected facility
        compare with towns without it? I used radio buttons because there are only
        three mutually exclusive choices, so keeping them visible makes comparison
        faster than hiding them inside another dropdown. The options also depend on
        the facility selected above, which creates a linked drill-down experience.
        This supports the course concepts of providing context, reducing cognitive load,
        and focusing attention.
        """
    )

# -----------------------------
# Visualization 1: Histogram
# -----------------------------
fig = px.histogram(
    filtered_df,
    x="Tourism Index",
    nbins=10,
    title=f"Distribution of Tourism Index - {availability}"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Insight 1")

st.write(
    """
    The Tourism Index is concentrated toward the lower end of the scale.
    The median Tourism Index is 3, meaning that half of the towns have
    a score of 3 or lower. The average score is approximately 3.07,
    while the maximum score reaches 10.
    """
)

# --------------------------------------
# Visualization 2: With vs Without
# --------------------------------------
comparison_df = df.copy()

comparison_df["Facility Status"] = comparison_df[selected_column].apply(
    lambda x: f"With {facility}" if x > 0 else f"Without {facility}"
)

fig2 = px.box(
    comparison_df,
    x="Facility Status",
    y="Tourism Index",
    points="all",
    title=f"Tourism Index: With vs Without {facility}"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Insight 2")

st.write(
    f"""
    The chart compares towns with {facility.lower()} to towns without
    {facility.lower()}. This helps show whether the presence of the selected tourism
    facility is associated with differences in Tourism Index values and makes the
    comparison between the two groups more direct.
    """
)