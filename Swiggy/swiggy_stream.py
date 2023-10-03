import streamlit as st
# read csv on streamlit
import pandas as pd
df = pd.read_csv("swiggy.csv")
st.write("Hey lets get work started")
list_city = df["city"].unique()
with st.sidebar:
    st.info("This is a side bar")
    city_selected = st.selectbox("Select or type your city",list_city)
st.write("You selected",city_selected)
# st.background("red")
# list of available restaurants
name_of_restaurants = df[df["city"] == city_selected]["name"].values
st.write(f"List of available restaurants in {city_selected}")
# st.write(name_of_restaurants)

selected_restaurant = st.selectbox("Select the restaurant",name_of_restaurants)

st.write(f"Information About the restaurant : {selected_restaurant}")

seelected_df = df[(df["city"] == city_selected) & (df["name"] == selected_restaurant)].values.tolist()
# st.write(df[df["name"] == selected_restaurant])
# st.write(seelected_df)

st.write(f'''
    the cost {seelected_df[0][5]}

the rating {seelected_df[0][3]}

No of Reviws {seelected_df[0][4]}

Cuisine Famous For {seelected_df[0][6]}

Address: {seelected_df[0][9]}


Head over to book from this restaurant : {seelected_df[0][8]}

    ''')
result_df = df[df["city"] == city_selected][["name", "cost"]]
result_df['cost'] = result_df['cost'].str.replace('₹', '').astype(int)  # Convert cost column to integer
result_df = result_df.sort_values(by='cost', ascending=False)
st.line_chart(result_df, x="name", y="cost")
st.map(df[df["city"] == city_selected])