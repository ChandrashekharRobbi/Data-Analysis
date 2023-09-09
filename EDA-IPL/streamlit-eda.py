import ast
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

# 🌟 Introduction & Credits 🌟
st.write("### 🌟 Welcome to the IPL EDA App 🌟")
with st.expander("# Details  💎🎈",expanded=True):
    st.write("This app provides an exploratory data analysis of IPL matches over the years. Dive in, explore, and let the numbers tell the story! 📊🏏")
    st.write("Created with ❤️ by **Chandrashekhar Robbi**, a CSE AI & ML Engineer. 🚀")

# set the app title
st.title("EDA of IPL Matches 🏆")

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/ChandrashekharRobbi/Data-Analysis/main/EDA-IPL/data/IPL_Matches_2008_2022.csv")
# st.dataframe(df, column_config={"Season":st.column_config.NumberColumn(format="%d")})
# df["Season"] = df["Season"].astype('str')
# Sidebar for user input
with st.sidebar:
    st.header("🔴 About Me")
    st.markdown("""
**Chandrashekhar A Robbi** 🚀  
📍 Thane, Maharashtra  
📧 chandrashekarrobbi789@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/ChandrashekharRobbi) | [Github](https://github.com/ChandrashekharRobbi) | [Website](https://chandrashekharrobbi.github.io/Website/)  

---
""")
    st.header("🔧 User Input Features 🔧")
    st.info("📆 You can select from year 2022 - 2008")
    selected_year = st.selectbox("Select Year", ["All Years"] + list(range(2022, 2007, -1)))

# Filtering data
if selected_year == "All Years":
    data_to_use = df
    st.subheader("Analysis for All Years `(2008-2022)` 🕰️")
    total_matches = len(data_to_use)
    st.write(f"##### 📈 Total number of matches played from 2008 to 2022: **{total_matches}**")
    # plot 
    plt.figure(figsize=(12, 15))
    # Using a color palette
    palette = sns.color_palette("viridis", len(data_to_use["WinningTeam"].value_counts().index))
    # Count plot with palette
    sns.countplot(y=data_to_use["WinningTeam"], order=data_to_use["WinningTeam"].value_counts().index, palette=palette)
    # Adding Annotations
    ax = plt.gca()
    for p in ax.patches:
        ax.text(p.get_width() + 1.3, p.get_y() + p.get_height() / 2,
                f'{int(p.get_width())}', va='center')
    st.pyplot(plt)
    st.warning("⚠️ Please note: This is the total number of wins for all years, not individual years.")
    st.write("Created with ❤️ by **Chandrashekhar Robbi**, a CSE AI & ML Engineer. 🚀")
else:
    data_to_use = df[df["Season"] == selected_year]
    st.subheader(f"Analysis for the Year: `{selected_year}` 📅")
    
    # plot the figure of wins
    plt.figure(figsize=(12,8))
    palette = sns.color_palette("viridis", len(data_to_use["WinningTeam"].value_counts().index))
    sns.countplot(y=data_to_use["WinningTeam"], order=data_to_use["WinningTeam"].value_counts().index, palette=palette)
    plt.title(f" Count of Wins per Team for {selected_year}")
    plt.xlabel("Number of Wins ")
    ax = plt.gca()
    for p in ax.patches:
        ax.text(p.get_width() + 0.3, p.get_y() + p.get_height() / 2,
                f'{int(p.get_width())}', va='center')
    st.pyplot(plt)

    # Display number of wins and losses for each team
    teams = pd.concat([data_to_use['Team1'], data_to_use['Team2']]).unique()
    win_counts = data_to_use["WinningTeam"].value_counts()
    # create a dataframe to store team statistics
    team_stats = []

    for team in teams:
        wins = win_counts.get(team, 0)
        total_matches_for_team = len(data_to_use[(data_to_use['Team1'] == team) | (data_to_use['Team2'] == team)])
        losses = total_matches_for_team - wins
        team_stats.append([team, wins, losses])

    # convert lists of lists to Data Frame
    df_team_stats = pd.DataFrame(data=team_stats, columns=['Team', 'Wins', 'Losses'])
    
    # Display as table
    st.subheader("📊 Wins and Losses for Teams:")
    st.write(df_team_stats)
    st.divider()
    
    with st.expander("🔍 Detailed Analysis",expanded=True):
        st.subheader(f"🔬 Deep Dive into the Year: `{selected_year}`")
        selected_match = st.select_slider(f"🔢 Select Match Number for Detailed Analysis (Out of {len(data_to_use['MatchNumber'].values)})",options=data_to_use["MatchNumber"].values[::-1] , help="Slide till end to view the `Semi Final` and `Final` Details 🥳")
        st.write(f"🎯 Selected Match Number is: {selected_match}")

        # Filter for the selected match
        details_of_match = data_to_use[data_to_use["MatchNumber"] == selected_match]

        def Values(colName):
            return details_of_match[colName].values[0]
        
        # Display Match Details
        st.write('### 🎉 Match Details:')
        st.write(f"🏟️ **Venue:** {Values('Venue')}")
        st.write(f"🏏 **Team 1:** {Values('Team1')}")
        
        if st.checkbox(f"👥 Show {Values('Team1')} Players"):
            st.subheader(f"{Values('Team1')} Squad")
            val = ", ".join(ast.literal_eval(details_of_match['Team1Players'].values[0]))
            st.write(val)
            st.divider()

        st.write(f"🏏 **Team 2:** {Values('Team2')}")
        if st.checkbox(f"👥 Show {Values('Team2')} Players"):
            st.subheader(f"{Values('Team2')} Squad")
            val = ", ".join(ast.literal_eval(details_of_match['Team2Players'].values[0]))
            st.write(val)
            st.divider()

        Sections = {'Toss Winner 🪙': 'TossWinner',
                    'Toss Decision 🔄': 'TossDecision',
                    'Winning Team 🎖️': 'WinningTeam',
                    'Player of the Match 🌟': 'Player_of_Match',
                    'Won By 🥇': 'WonBy'}
        for section, colName in Sections.items():
            st.write(f"**{section}:** {Values(colName)}")
        
        if st.checkbox("🕴️ Show Umpire Details"):
            st.write(f"👤 **Umpire 1:** {Values('Umpire1')}")
            st.write(f"👤 **Umpire 2:** {Values('Umpire2')}")
    
    st.write("Created with ❤️ by **Chandrashekhar Robbi**, a CSE AI & ML Engineer. 🚀")
