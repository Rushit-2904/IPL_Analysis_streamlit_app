import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

deliveries_df = pd.read_csv('deliveries.csv')
matches_df = pd.read_csv('matches.csv')

ddf = deliveries_df.copy()
mdf = matches_df.copy()

# changing the names of certain teams which are same but name is different in dataset
ddf.loc[ddf['batting_team'] == 'Rising Pune Supergiant' , 'batting_team'] = 'Rising Pune Supergiants'
ddf.loc[ddf['bowling_team'] == 'Rising Pune Supergiant' , 'bowling_team'] = 'Rising Pune Supergiants'

ddf.loc[ddf['batting_team'] == 'Kings XI Punjab' , 'batting_team'] = 'Punjab Kings'
ddf.loc[ddf['bowling_team'] == 'Kings XI Punjab' , 'bowling_team'] = 'Punjab Kings'

ddf.loc[ddf['batting_team'] == 'Royal Challengers Bangalore' , 'batting_team'] = 'Royal Challengers Bengaluru'
ddf.loc[ddf['bowling_team'] == 'Royal Challengers Bangalore' , 'bowling_team'] = 'Royal Challengers Bengaluru'

# lists of batsman, bowler, batting team and bowling team
batting_team_list = list(ddf['batting_team'].unique())
bowling_team_list = list(ddf['bowling_team'].unique())
batsman_list = list(ddf['batter'].unique())
bowler_list = list(ddf['bowler'].unique()) 

# Same changes in matches dataframe
mdf.loc[mdf['team1'] == 'Rising Pune Supergiant' , 'team1'] = 'Rising Pune Supergiants'
mdf.loc[mdf['team2'] == 'Rising Pune Supergiant' , 'team2'] = 'Rising Pune Supergiants'

mdf.loc[mdf['team1'] == 'Kings XI Punjab' , 'team1'] = 'Punjab Kings'
mdf.loc[mdf['team2'] == 'Kings XI Punjab' , 'team2'] = 'Punjab Kings'

mdf.loc[mdf['team1'] == 'Royal Challengers Bangalore' , 'team1'] = 'Royal Challengers Bengaluru'
mdf.loc[mdf['team2'] == 'Royal Challengers Bangalore' , 'team2'] = 'Royal Challengers Bengaluru'

mdf.loc[mdf['winner'] == 'Rising Pune Supergiant' , 'winner'] = 'Rising Pune Supergiants'
mdf.loc[mdf['winner'] == 'Kings XI Punjab' , 'winner'] = 'Punjab Kings'
mdf.loc[mdf['winner'] == 'Royal Challengers Bangalore' , 'winner'] = 'Royal Challengers Bengaluru'

# season changes ad well
mdf.loc[mdf['season'] == '2007/08' , 'season'] = '2008'
mdf.loc[mdf['season'] == '2009/10' , 'season'] = '2010'
mdf.loc[mdf['season'] == '2020/21' , 'season'] = '2020'


### BATSMAN CAREER DETAILS ###
def bat_info(batsman):
    a = batsman +"'s IPL Statistics"
    st.subheader(a)
    bmdf = ddf.groupby('batter').get_group(batsman)
    total_batsman_innings = bmdf['match_id'].nunique()
    balls_faced = ddf.groupby('batter').get_group(batsman).shape[0]
    total_batsman_runs = bmdf['batsman_runs'].sum()
    if batsman not in list(bmdf['player_dismissed'].value_counts().index):
        batsman_average = total_batsman_runs / total_batsman_innings
    else:
        batsman_average = round(total_batsman_runs/bmdf['player_dismissed'].value_counts()[batsman],2)    
    batsman_strike_rate = round(total_batsman_runs*100/bmdf.shape[0],2)
    batsman_highest_score = bmdf.groupby('match_id')['batsman_runs'].sum().max()
    ducks = (bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() == 0).sum()
    batsman_100 = (bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() >= 100).sum()
    batsman_50 = ((bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() >= 50).sum()) - (bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() >= 100).sum()
    boundries_4 = bmdf[bmdf['batsman_runs'] == 4].shape[0]
    boundries_6 = bmdf[bmdf['batsman_runs'] == 6].shape[0]

    temp = bmdf.groupby('match_id').agg({"ball": ["count"], "batsman_runs": ["sum"]}).reset_index()
    zeros_list = list(temp[(temp['ball']['count'] == 1) & (temp['batsman_runs']['sum'] == 0)]['match_id'].values)
    golden_ducks = bmdf.set_index('match_id').loc[zeros_list].shape[0]

    catches_taken = ddf[(ddf['fielder'] == batsman) & (ddf['dismissal_kind'] == 'caught')].shape[0]
    number_of_runouts = ddf[(ddf['fielder'] == batsman) & (ddf['dismissal_kind'] == 'run out')].shape[0]

    st.dataframe((pd.DataFrame(
            {'Innings': [total_batsman_innings],
             'Number of balls faced' : [balls_faced],
             'Total runs' : [total_batsman_runs],
             'Average': [batsman_average],
             'Strike rate': [batsman_strike_rate],
             'Highest score' : [batsman_highest_score],
            }
        )).transpose())
    st.dataframe((pd.DataFrame(
            {
            'Number of 100+ scores' : [batsman_100],
            'Number of 50+ scores' : [batsman_50],
            'Number of golden ducks' : [golden_ducks],
            'Number of ducks' : [ducks],
            "Number of 4's" : [boundries_4],
            "Number of 6's" : [boundries_6]
            }
        )).transpose())

    st.subheader('Dismissal Types')
    st.dataframe(pd.DataFrame(bmdf[bmdf['player_dismissed'] == batsman]['dismissal_kind'].value_counts()))


### BATSMAN VS A SINGLE TEAM STATS ###
def bat_vs_team_info(batsman,team):
    if ddf[(ddf['batter'] == batsman) & (ddf['bowling_team'] == team)].shape[0] == 0:
        multi = '''Check the *player* name and *team* name  
                - Ther could be possibly one of these three reasons for the error  
                1. He played for the same team you have selected  
                2. He never batted against that team  
                3. When he was playing in IPL, that team did not exist  
        '''
        st.image('erro.gif')
        st.markdown(multi)
    else:
        bmdf = ddf.groupby(['batter','bowling_team']).get_group((batsman,team))

        total_batsman_innings = bmdf['match_id'].nunique()
        balls_faced = bmdf['batter'].shape[0]
        total_batsman_runs = int(bmdf['batsman_runs'].sum())
        if batsman not in list(bmdf['player_dismissed'].value_counts().index):
            batsman_average = total_batsman_runs / total_batsman_innings
        else:
            batsman_average = round(total_batsman_runs/bmdf['player_dismissed'].value_counts()[batsman],2)    
        batsman_strike_rate = round(total_batsman_runs*100/bmdf.shape[0],2)
        batsman_highest_score = bmdf.groupby('match_id')['batsman_runs'].sum().max()
        ducks = (bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() == 0).sum()
        batsman_100 = (bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() >= 100).sum()
        batsman_50 = ((bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() >= 50).sum()) - (bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() >= 100).sum()
        boundries_4 = bmdf[bmdf['batsman_runs'] == 4].shape[0]
        boundries_6 = bmdf[bmdf['batsman_runs'] == 6].shape[0]

        temp = bmdf.groupby('match_id').agg({"ball": ["count"], "batsman_runs": ["sum"]}).reset_index()
        zeros_list = list(temp[(temp['ball']['count'] == 1) & (temp['batsman_runs']['sum'] == 0)]['match_id'].values)
        golden_ducks = bmdf.set_index('match_id').loc[zeros_list].shape[0]

        st.dataframe((pd.DataFrame(
                {'Innings': [total_batsman_innings],
                'Number of balls faced' : [balls_faced],
                'Total runs' : [total_batsman_runs],
                'Average': [batsman_average],
                'Strike rate': [batsman_strike_rate],
                'Highest score' : [batsman_highest_score],
                }
            )).transpose())
        st.dataframe((pd.DataFrame(
                {
                'Number of 100+ scores' : [batsman_100],
                'Number of 50+ scores' : [batsman_50],
                'Number of golden ducks' : [golden_ducks],
                'Number of ducks' : [ducks],
                "Number of 4's" : [boundries_4],
                "Number of 6's" : [boundries_6]
                }
            )).transpose())

        st.subheader('Dismissal Types')
        st.dataframe(pd.DataFrame(bmdf[bmdf['player_dismissed'] == batsman]['dismissal_kind'].value_counts()))
         
    
### Team Stats
def team_info(team):
    seasons = list(mdf['season'].unique())
    top_4_teams = mdf[mdf['match_type'] != 'League']
    final_teams = []
    sd={}
    for season in seasons:
        s = top_4_teams.groupby('season').get_group(season)
        s_teams = list(set(list(s['team1'].unique()) + list(s['team2'].unique())))
        final_teams = s_teams + final_teams
    for temp_team in batting_team_list:
        counts =final_teams.count(temp_team)
        sd[temp_team] = counts
    # groupby for batting team
    btdf = ddf.groupby('batting_team').get_group(team)
    top_3_batsman = (btdf.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False)[0:3]).reset_index()

    # groupby for bowling team
    bwdf = ddf.groupby('bowling_team').get_group(team)
    top_3_bowlers = (bwdf.groupby('bowler')['player_dismissed'].count().sort_values(ascending=False)[0:3]).reset_index()

    highest_successful_runchase = int(mdf[((mdf['team1'] == team)|(mdf['team2'] == team)) & (mdf['winner'] == team) & (mdf['result'] == 'wickets')&(mdf['method'].isna())]['target_runs'].max())
    lowest_total_defended = int(mdf[((mdf['team1'] == team)|(mdf['team2'] == team)) & (mdf['winner'] == team) & (mdf['result'] == 'runs')&(mdf['method'].isna())]['target_runs'].min())-1

    total_trophies = int((mdf[mdf['match_type']=='Final']['winner'] == team).sum())

    player_of_the_match = mdf[((mdf['team1'] == team) | (mdf['team2'] == team)) & (mdf['winner'] == team)]['player_of_match'].value_counts().reset_index()
    player_of_the_match.index = player_of_the_match.index + 1
    player_of_the_match = player_of_the_match[0:3]

    st.write('Top 3 batsman and bowlers from',selected_team)
    st.dataframe(pd.concat([top_3_batsman,top_3_bowlers], axis=1))
    st.write(selected_team," achievments")
    st.dataframe({
        'Stats':['Highest Successful Runchase','Lowest Total Defended','Total Trophies'],
        'Values':[highest_successful_runchase,lowest_total_defended,total_trophies]
    })
    st.write(selected_team,'has qualified',sd[selected_team],'times for playoffs')
    
### Team vs Team Stats
def team_vs_team_info(team1,team2):
    if team1 == team2:
        st.write('You have selected same teams')
    else:
        total_matches = mdf[((mdf['team1'] == team1) & (mdf['team2'] == team2)) | ((mdf['team1'] == team2) & (mdf['team2'] == team1))].shape[0]
        ttdf = mdf[(((mdf['team1'] == team1) & (mdf['team2'] == team2)) | ((mdf['team1'] == team2) & (mdf['team2'] == team1))) & ((mdf['result'] == 'wickets') | ((mdf['result'] == 'runs')))]
        wins = ttdf['winner'].value_counts().reset_index().rename(columns={'winner':'Winning Team'})
        wins.index = wins.index+1

        st.write('Number of matches played between',team1,'and',team2,'are',total_matches)
        st.dataframe(wins)

        if (mdf[((mdf['team1'] == team1) & (mdf['team2'] == team2)) | ((mdf['team1'] == team2) & (mdf['team2'] == team1))]['result'] == 'tie').sum() == 0:
            pass
        else:
            tttdf = mdf[(((mdf['team1'] == team1) & (mdf['team2'] == team2)) | ((mdf['team1'] == team2) & (mdf['team2'] == team1))) & ((mdf['result'] == 'tie'))]
            tie_wins = tttdf['winner'].value_counts().reset_index().rename(columns={'winner':'Winning Team'})
            tie_wins.index = tie_wins.index+1
            st.write('Number of Draw matches =',tttdf.shape[0])
            st.dataframe(tie_wins)

        if (mdf[((mdf['team1'] == team1) & (mdf['team2'] == team2)) | ((mdf['team1'] == team2) & (mdf['team2'] == team1))]['result'] == 'no result').sum() == 0:
            pass
        else:
            no_result_matches = mdf[((mdf['team1'] == team1) & (mdf['team2'] == team2) | (mdf['team1'] == team2) & (mdf['team2'] == team1)) & ((mdf['result'] == 'no result'))].shape[0]
            st.write('Total number of matches with no result =',no_result_matches)

        
        l = []
        l.append(team1)
        l.append(team2)
        OG_teams = ddf[((ddf['batting_team'] == team1) & (ddf['bowling_team'] == team2)) | ((ddf['batting_team'] == team2) & (ddf['bowling_team'] == team1))]

        
        for team in l:
            teams = OG_teams[OG_teams['bowling_team'] == team]

            
            batter = teams.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).reset_index().rename(columns={'batter':'batsman','batsman_runs':'Runs'})
            batter.index = batter.index + 1
            batter = batter[batter.index == 1]

            bowler = teams.groupby('bowler')['player_dismissed'].count().sort_values(ascending=False).reset_index().rename(columns={'player_dismissed':'Wickets'})
            bowler.index = bowler.index + 1
            bowler = bowler[bowler.index == 1]
            st.write('Top scorer against',team)
            st.dataframe(batter)
            st.write('Top wicket taker for',team)
            st.dataframe(bowler)


#### above are functions and below they are called
st.sidebar.title('IPL Statistics')

option = st.sidebar.selectbox('Select type of statistics',['Batsman Stats','Batsman vs Team Stats','Team stats','Team vs Team Stats'])
if option == 'Batsman Stats':
    st.title('Batsman stats')
    selected_batsman = st.sidebar.selectbox('Select Batsman',batsman_list)
    btn1 = st.sidebar.button('Fetch Results')   
    if btn1:
        bat_info(selected_batsman)

elif option == 'Batsman vs Team Stats':
    st.title('Batsman vs Team Stats')
    selected_batsman = st.sidebar.selectbox('Select Batsman',batsman_list)
    selected_team = st.sidebar.selectbox('Select Team',bowling_team_list)
    btn2 = st.sidebar.button('Fetch Results')
    if btn2:
        bat_vs_team_info(selected_batsman,selected_team)
    
elif option == 'Team stats':
    st.title('Team stats')
    selected_team = st.sidebar.selectbox('Select Team',batting_team_list)
    btn3 = st.sidebar.button('Fetch Results')
    if btn3:
        team_info(selected_team)        
    

elif option == 'Team vs Team Stats':
    st.title('Team vs Team Stats')
    selected_team1 = st.sidebar.selectbox('Select Team1',batting_team_list)
    selected_team2 = st.sidebar.selectbox('Select Team2',batting_team_list)
    btn4 = st.sidebar.button('Fetch Results')
    if btn4:
        team_vs_team_info(selected_team1,selected_team2)