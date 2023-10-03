import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
st.set_page_config(theme="light")
st.set_page_config(layout="wide")
# Use caching to prevent re-loading data every time
@st.cache_data 
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/ChandrashekharRobbi/Data-Analysis/main/Swiggy/swiggy.csv")

df = load_data()

# Preliminary data checks
if df.empty:
    st.error("The data is empty!")
    st.stop()

# Sidebar and title improvements
with st.sidebar:
    st.header("🔴 About Me")
    st.markdown("""
**Chandrashekhar A Robbi** 🚀  
📍 Thane, Maharashtra  
📧 chandrashekarrobbi789@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/ChandrashekharRobbi) | [Github](https://github.com/ChandrashekharRobbi) | [Website](https://chandrashekharrobbi.github.io/Website/)  
""")
    st.info("Explore more !!!")
    city_selected = st.selectbox("Select or type your city",["Data Analysis"] + list(df["city"].unique().tolist()))

if city_selected == "Data Analysis":
    st.title("Data Analysis of the Swiggy Data Set")
    with st.expander("# Details  💎🎈",expanded=True):
        st.write("This app provides an exploratory data analysis of Swiggy Restaurants present in India. Dive in, explore, and let the numbers tell the story! 📊🏏")
        st.write("Created with ❤️ by **Chandrashekhar Robbi**, a CSE AI & ML Engineer. 🚀")
    st.subheader(f"There are `{len(df['city'].unique())}` cities in India 💝 associated with Swiggy.")
    st.success(f"{df['city'].value_counts().idxmax()} is the 🥇 highest revenue generating city with `{df['city'].value_counts().max()}` hotels 🏨.")

    st.subheader("Cities with Top Hotels 🌟")
    st.info("Ratings greater than 3.5")
    df["rating"] = df["rating"].replace("--", 0)
    ratings = df[df["rating"].astype(float) >= 3.5]["city"].value_counts()
    st.bar_chart(ratings)
    graph1, graph2 = st.columns(2)
    with graph1:
        # st.write(df.columns)
        st.subheader("Distribution of Ratings Count 📋")
        plt.figure(figsize=(6, 6))
        sns.countplot(df['rating_count'], color='green', order=df['rating_count'].value_counts().index[:10])
        plt.title('Distribution of Ratings Count')
        # plt.
        st.pyplot(plt)
    with graph2:
        st.subheader("Distribution of Ratings 🌈")
        plt.figure(figsize=(6, 6))
        sns.histplot(df[df['rating'] != 0]['rating'].astype(float), color='green')
        plt.title('Distribution of Ratings')
        # plt
        st.pyplot(plt)

else:
    st.header(f"Welcome to `{city_selected}`")
    col1 , col2 = st.columns(2)
    result_df = df[df["city"] == city_selected][["name", "cost"]]
    result_df['cost'] = result_df['cost'].str.replace('₹', '').astype(int)  # Convert cost column to integer
    result_df = result_df.sort_values(by='cost', ascending=True)
    with col1:

        data = df[df["city"] == city_selected]["cuisine"].value_counts().reset_index()['count'][:10]
        keys = df[df["city"] == city_selected]["cuisine"].value_counts().reset_index()['cuisine'][:10]
        st.header(f'Top 10 Cuisine Distribution in {city_selected}')
        st.plotly_chart(px.pie(data, values=data, names=keys), use_container_width=True,width=200, height=500)
    with col2:
        st.subheader("Top Restaurants with there Starting cost ")
        st.bar_chart(result_df, x="name", y="cost",use_container_width=True)

    
    # iterate through every row of selected cuisine and get all information such as name, cost, rating, rating_count, cuisine, address, link
    tab1, tab2 = st.tabs(["Restaurant By Name", "Restaurant By Cuisine"])
    with tab1:
        st.subheader("Dig into Restaurant Details 🍽️")
        selected_restaurant = st.selectbox("Available Restaurants:", df[df["city"] == city_selected]["name"].unique())
    
        restaurant_info = df[(df["city"] == city_selected) & (df["name"] == selected_restaurant)].iloc[0]
        
        st.markdown(f"""
            **Starting Cost**: {restaurant_info['cost']}  
            **Rating**: {restaurant_info['rating']}  
            **No of Reviews**: {restaurant_info['rating_count']}  
            **Cuisine**: {restaurant_info['cuisine']}  
            **Address**: {restaurant_info['address']}  
            [Link to the restaurant]({restaurant_info['link']})
        """)
    
    with tab2:
        st.subheader("Taste the Cuisines 🍜")
        selected_cuisine = st.selectbox("Available Cuisines:", df[df["city"] == city_selected]["cuisine"].unique())
        # st.write(df[(df["city"] == city_selected) & (df["cuisine"] == selected_cuisine)])

        for index, row in df[(df["city"] == city_selected) & (df["cuisine"] == selected_cuisine)].iterrows():
            st.divider()
            st.markdown(f"""
            **Name** : {row['name']}
            **Starting Cost**: {row['cost']}  
            **Rating**: {row['rating']}  
            **No of Reviews**: {row['rating_count']}  
            **Cuisine**: {row['cuisine']}  
            **Address**: {row['address']}  
            [Link to the restaurant]({row['link']})
        """)
        

