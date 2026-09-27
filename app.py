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
df = pd.read_csv("dataset.csv")

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





fig = px.histogram(
    filtered_df,
    x="Tourism Index",
    nbins=10,
    title="Distribution of Tourism Index"
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





filtered_df = filtered_df.copy()
filtered_df["Selection"] = availability

fig2 = px.box(
    filtered_df,
    x="Selection",
    y="Tourism Index",
    points="all",
    title=f"Tourism Index for {availability}"
)

st.plotly_chart(fig2, use_container_width=True)



st.subheader("Insight 2")

st.write(
    """
    Comparing towns with and without the selected tourism facility helps show
    whether tourism infrastructure is associated with stronger Tourism Index values.
    This makes it easier to identify differences between towns with more developed
    tourism services and those with fewer facilities.
    """
)