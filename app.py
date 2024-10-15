import pandas as pd
import numpy as np
import streamlit as st
import pickle



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
players_list = list(set(batsman_list + bowler_list))
team_list = list(set(batting_team_list + bowling_team_list))

only_batters = set(batsman_list).difference(bowler_list)
only_bowlers = set(bowler_list).difference(batsman_list)

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

first_season = int(mdf['season'].min())
latest_season = int(mdf['season'].max())

# Changed Venue names where one stadium was addressed with different names
mdf['venue'].replace(['Arun Jaitley Stadium','Feroz Shah Kotla'],'Arun Jaitley Stadium, Delhi',inplace=True)
mdf['venue'].replace(['Wankhede Stadium'],'Wankhede Stadium, Mumbai',inplace=True)
mdf['venue'].replace(['Eden Gardens'],'Eden Gardens, Kolkata',inplace=True)
mdf['venue'].replace(['M Chinnaswamy Stadium','M.Chinnaswamy Stadium'],'M Chinnaswamy Stadium, Bengaluru',inplace=True)
mdf['venue'].replace(['MA Chidambaram Stadium','MA Chidambaram Stadium, Chepauk'],'MA Chidambaram Stadium, Chepauk, Chennai',inplace=True)
mdf['venue'].replace(['Rajiv Gandhi International Stadium','Rajiv Gandhi International Stadium, Uppal'],'Rajiv Gandhi International Stadium, Uppal, Hyderabad',inplace=True)
mdf['venue'].replace(['Sardar Patel Stadium, Motera'],'Narendra Modi Stadium, Ahmedabad',inplace=True)
mdf['venue'].replace(['Punjab Cricket Association Stadium, Mohali','Punjab Cricket Association IS Bindra Stadium, Mohali','Punjab Cricket Association IS Bindra Stadium'],'Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh',inplace=True)
mdf['venue'].replace(['Sawai Mansingh Stadium'],'Sawai Mansingh Stadium, Jaipur',inplace=True)
mdf['venue'].replace(['Sheikh Zayed Stadium'],'Zayed Cricket Stadium, Abu Dhabi',inplace=True)
mdf['venue'].replace(['Dr DY Patil Sports Academy'],'Dr DY Patil Sports Academy, Mumbai',inplace=True)
mdf['venue'].replace(['Brabourne Stadium'],'Brabourne Stadium, Mumbai',inplace=True)
mdf['venue'].replace(['Maharashtra Cricket Association Stadium'],'Maharashtra Cricket Association Stadium, Pune',inplace=True)
mdf['venue'].replace(['Himachal Pradesh Cricket Association Stadium'],'Himachal Pradesh Cricket Association Stadium, Dharamsala',inplace=True)
mdf['venue'].replace(['Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium'],'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam',inplace=True)

venue_list = list(mdf['venue'].unique())

### BATSMAN CAREER DETAILS ###
def bat_info(batsman):
    if batsman in only_bowlers:
        st.markdown(batsman+''' Has never faced a single delivery in his entire IPL career''')
        st.text("")
    else:
        a = batsman +"'s Batting IPL Statistics"
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
        batsman_100 = (bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() >= 100).sum()
        batsman_50 = ((bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() >= 50).sum()) - (bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() >= 100).sum()
        boundries_4 = bmdf[bmdf['batsman_runs'] == 4].shape[0]
        boundries_6 = bmdf[bmdf['batsman_runs'] == 6].shape[0]

        temp = bmdf.groupby('match_id').agg({"ball": ["count"], "batsman_runs": ["sum"]}).reset_index()
        zeros_list = list(temp[(temp['ball']['count'] == 1) & (temp['batsman_runs']['sum'] == 0)]['match_id'].values)
        ducks = (bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() == 0).sum() - bmdf.set_index('match_id').loc[zeros_list].shape[0]
        golden_ducks = bmdf.set_index('match_id').loc[zeros_list].shape[0]

        catches_taken = ddf[(ddf['fielder'] == batsman) & (ddf['dismissal_kind'] == 'caught')].shape[0]
        number_of_runouts = ddf[(ddf['fielder'] == batsman) & (ddf['dismissal_kind'] == 'run out')].shape[0]

        col1, col2, col3 =  st.columns(3)
        with col1:

            st.dataframe((pd.DataFrame(
                    {'Innings': [total_batsman_innings],
                    'Number of balls faced' : [balls_faced],
                    'Total runs' : [total_batsman_runs],
                    'Average': [batsman_average],
                    'Strike rate': [batsman_strike_rate],
                    'Highest score' : [batsman_highest_score],
                    }
                )).transpose())
        with col2:

            st.dataframe((pd.DataFrame(
                    {
                    'Number of 100+ scores' : [batsman_100],
                    'Number of 50+ scores' : [batsman_50],
                    'Number of ducks' : [ducks],
                    'Number of golden ducks' : [golden_ducks],
                    "Number of 4's" : [boundries_4],
                    "Number of 6's" : [boundries_6]
                    }
                )).transpose())
        with col3:
            st.dataframe(pd.DataFrame(bmdf[bmdf['player_dismissed'] == batsman]['dismissal_kind'].value_counts()))


### BATSMAN VS A SINGLE TEAM STATS ###
def bat_vs_team_info(batsman,team):
    if batsman in only_bowlers:
        st.markdown(batsman+''' Has never faced a single delivery in his entire IPL career''')
    else:   
        if ddf[(ddf['batter'] == batsman) & (ddf['bowling_team'] == team)].shape[0] == 0:
            multi = '''Nothing to display as part of batting statistics because of one of the following reasons  
                    1. '''+batsman+''' played for '''+team+''' or  
                    2. '''+batsman+''' never batted against '''+team+''' or  
                    3. When '''+batsman+''' was playing, '''+team+''' did not exist and vice versa or  
                    4. When '''+batsman+''' was playing, '''+team+''' was not a part of the tournament
            '''
            st.markdown(multi)
        else:
            a = batsman +"'s IPL Statistics against "+ team
            st.subheader(a)
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
            ducks = (bmdf.groupby('match_id')['batsman_runs'].sum().sort_values() == 0).sum() - bmdf.set_index('match_id').loc[zeros_list].shape[0]
            golden_ducks = bmdf.set_index('match_id').loc[zeros_list].shape[0]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.dataframe((pd.DataFrame(
                        {'Innings': [total_batsman_innings],
                        'Number of balls faced' : [balls_faced],
                        'Total runs' : [total_batsman_runs],
                        'Average': [batsman_average],
                        'Strike rate': [batsman_strike_rate],
                        'Highest score' : [batsman_highest_score],
                        }
                    )).transpose())
            with col2:
                st.dataframe((pd.DataFrame(
                        {
                        'Number of 100+ scores' : [batsman_100],
                        'Number of 50+ scores' : [batsman_50],
                        'Number of ducks' : [ducks],
                        'Number of golden ducks' : [golden_ducks],
                        "Number of 4's" : [boundries_4],
                        "Number of 6's" : [boundries_6]
                        }
                    )).transpose())

            with col3:
                st.dataframe(pd.DataFrame(bmdf[bmdf['player_dismissed'] == batsman]['dismissal_kind'].value_counts()))
         
### BOWLER CAREER DETAILS ###
def ball_info(bowler):
    
    if ddf[ddf['bowler'] == bowler].shape[0] != 0:
        a = bowler+"'s Bowling IPL Statistics"
        st.subheader(a)

        # nsdf is a data frame of innings which has only matches that are non super over
        # bnsdf is a dataframe of a single bowler
        nsdf = ddf[(ddf['inning'] == 1)|(ddf['inning'] == 2)]
        bnsdf = nsdf.groupby('bowler').get_group(bowler)

        matches = bnsdf['match_id'].nunique()
        wickets = bnsdf[(bnsdf['dismissal_kind'] != 'run out') & (bnsdf['dismissal_kind'] != 'retired hurt') & (bnsdf['dismissal_kind'] != 'obstructing the field') & (bnsdf['dismissal_kind'] != 'retired out')]['is_wicket'].sum()
        balls = (bnsdf[((bnsdf['extras_type'] != 'wides') & (bnsdf['extras_type'] != 'noballs'))]['ball'].count())
        overs = (balls//6)+(float(balls%6)/10)
        runs = bnsdf[(bnsdf['extras_type'] != 'legbyes') & (bnsdf['extras_type'] != 'byes')]['total_runs'].sum()
        if wickets == 0:
            average = runs/matches
            strike_rate = '-'
        else:
            average = runs/wickets
            strike_rate = round((balls/wickets),2)
        if balls//6 == 0:
            economy = runs*6
        else:
            economy = runs/overs
        number_of_4w = (bnsdf[bnsdf['dismissal_kind']!= 'run out'].groupby('match_id')['is_wicket'].sum() == 4).sum()
        number_of_5W = (bnsdf[bnsdf['dismissal_kind']!= 'run out'].groupby('match_id')['is_wicket'].sum() == 5).sum()


        # code for best figures in IPL
        temp = bnsdf[bnsdf['dismissal_kind']!= 'run out'].groupby('match_id')['is_wicket'].sum().sort_values(ascending=False).reset_index()
        x = []
        for i in temp[temp['is_wicket'] == temp['is_wicket'].max()]['match_id'].values:
            x.append(i)
        y = {}
        for i in x:
            m_runs = bnsdf[(bnsdf['match_id'] == i) & (bnsdf['extras_type'] != 'legbyes') & (bnsdf['extras_type'] != 'byes')]['total_runs'].sum()
            team = bnsdf[bnsdf['match_id'] == i]['batting_team'].unique()[0]
            y[i] = [m_runs,team]
        y = pd.DataFrame(y).transpose()

        best_wicket = bnsdf[bnsdf['dismissal_kind']!= 'run out'].groupby('match_id')['is_wicket'].sum().max()
        best_match_id = y[0][y[0] == y[0].min()].index[0]
        min_runs = bnsdf[(bnsdf['match_id'] == best_match_id) & (bnsdf['extras_type'] != 'legbyes') & (bnsdf['extras_type'] != 'byes')]['total_runs'].sum()
        best = (str(best_wicket)+'/'+str(min_runs))
        oponent_team = bnsdf[bnsdf['match_id'] == best_match_id]['batting_team'].unique()[0]
        pp_wickets = ddf[(ddf['bowler'] == bowler) & (ddf['over']<6) & (ddf['dismissal_kind'] != 'run out') & (ddf['dismissal_kind'] != 'retired hurt') & (ddf['dismissal_kind'] != 'obstructing the field') & (ddf['dismissal_kind'] != 'retired out')]['is_wicket'].sum()

        # Code for kind of dismissals
        filter_1 = ['caught','bowled','lbw','caught and bowled','stumped','hit wicket',None]
        a = bnsdf[(bnsdf['dismissal_kind'].isin(filter_1))]['dismissal_kind'].value_counts().reset_index()
        a.index = a.index +1

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe((pd.DataFrame(
                {
                'innings' : [matches],
                'wickets' : [wickets],
                'balls' : [balls],
                'overs' : [overs],
                'runs' : [runs]
                })))
        with col2:
            st.dataframe((pd.DataFrame(
                {
                'average' : [round(average,2)],
                'economy' : [round(economy,2)],
                'strike rate' : [strike_rate],
                '4 Wicket' : [number_of_4w],
                '5 Wicket' : [number_of_5W],
                'PP wickets' : [pp_wickets]
                })))

        col3, col4 = st.columns(2)
        with col3:
            st.write('Best figures in IPL')
            st.dataframe({
                'best': best,
                'oponent team' : oponent_team
            })
        with col4:
            st.write('Dismissal kind')
            st.dataframe(a)
    else:
        st.markdown('''Nothing to display as part of bowling statistics because  
                    '''+bowler+''' never bowled in IPL
        ''')
        
### BALL VS TEAM STATS
def ball_vs_team_info(bowler,team):
    # nsdf is a data frame of innings which has only matches that are non super over
    # bnsdf is a dataframe of a single bowler
    if bowler in only_batters:
        st.markdown(bowler+''' has never bowled a single bowl in his entire career''')
    else:
        nsdf = ddf[((ddf['inning'] == 1)|(ddf['inning'] == 2)) & (ddf['batting_team'] == team)]
        if nsdf[nsdf['bowler'] == bowler].shape[0] == 0:
            st.markdown('''Nothing to display as part of bowling statistics because of one of the following reasons   
                        1. '''+bowler+''' never bowled against '''+team+''' or  
                        2. '''+bowler+''' only played for '''+team+''' or  
                        3. when '''+bowler+''' was playing '''+team+''' not part of the tournament or  
                        4. when '''+bowler+''' was playing '''+team+''' did not exist and vice versa
                    ''')
        else:
            bnsdf = nsdf.groupby('bowler').get_group(bowler)

            matches = bnsdf['match_id'].nunique()
            wickets = bnsdf[(bnsdf['dismissal_kind'] != 'run out') & (bnsdf['dismissal_kind'] != 'retired hurt') & (bnsdf['dismissal_kind'] != 'obstructing the field') & (bnsdf['dismissal_kind'] != 'retired out')]['is_wicket'].sum()
            balls = (bnsdf[((bnsdf['extras_type'] != 'wides') & (bnsdf['extras_type'] != 'noballs'))]['ball'].count())
            overs = (balls//6)+(float(balls%6)/10)
            runs = bnsdf[(bnsdf['extras_type'] != 'legbyes') & (bnsdf['extras_type'] != 'byes')]['total_runs'].sum()
            if wickets == 0:
                average = runs/matches
                strike_rate = '-'
            else:
                average = runs/wickets
                strike_rate = round((balls/wickets),2)
            if balls//6 == 0:
                economy = runs*6
            else:
                economy = runs/overs
                number_of_4w = (bnsdf[bnsdf['dismissal_kind']!= 'run out'].groupby('match_id')['is_wicket'].sum() == 4).sum()
                number_of_5W = (bnsdf[bnsdf['dismissal_kind']!= 'run out'].groupby('match_id')['is_wicket'].sum() == 5).sum()


            # code for best figures in IPL against a team
            temp = bnsdf[bnsdf['dismissal_kind']!= 'run out'].groupby('match_id')['is_wicket'].sum().sort_values(ascending=False).reset_index()
            x = []
            for i in temp[temp['is_wicket'] == temp['is_wicket'].max()]['match_id'].values:
                x.append(i)
            y = {}
            for i in x:
                m_runs = bnsdf[(bnsdf['match_id'] == i) & (bnsdf['extras_type'] != 'legbyes') & (bnsdf['extras_type'] != 'byes')]['total_runs'].sum()
                team = bnsdf[bnsdf['match_id'] == i]['batting_team'].unique()[0]
                y[i] = [m_runs,team]
            y = pd.DataFrame(y).transpose()

            best_wicket = bnsdf[bnsdf['dismissal_kind']!= 'run out'].groupby('match_id')['is_wicket'].sum().max()
            best_match_id = y[0][y[0] == y[0].min()].index[0]
            min_runs = bnsdf[(bnsdf['match_id'] == best_match_id) & (bnsdf['extras_type'] != 'legbyes') & (bnsdf['extras_type'] != 'byes')]['total_runs'].sum()
            best = (str(best_wicket)+'/'+str(min_runs))
            pp_wickets = ddf[(ddf['batting_team'] == team) & (ddf['bowler'] == bowler) & (ddf['over']<6) & (ddf['dismissal_kind'] != 'run out') & (ddf['dismissal_kind'] != 'retired hurt') & (ddf['dismissal_kind'] != 'obstructing the field') & (ddf['dismissal_kind'] != 'retired out')]['is_wicket'].sum()

            # Code for kind of dismissals
            filter_1 = ['caught','bowled','lbw','caught and bowled','stumped','hit wicket',None]
            a = bnsdf[(bnsdf['dismissal_kind'].isin(filter_1))]['dismissal_kind'].value_counts().reset_index()
            a.index = a.index +1


            col1, col2 = st.columns(2)
            with col1:
                st.dataframe((pd.DataFrame(
                    {
                    'innings' : [matches],
                    'wickets' : [wickets],
                    'balls' : [balls],
                    'overs' : [overs],
                    'runs' : [runs]
                    })))
            with col2:
                st.dataframe((pd.DataFrame(
                    {
                    'average' : [round(average,2)],
                    'economy' : [round(economy,2)],
                    'strike rate' : [strike_rate],
                    '4 Wicket' : [number_of_4w],
                    '5 Wicket' : [number_of_5W],
                    'PP wickets' : [pp_wickets]
                    })))

            col3, col4 = st.columns(2)             
            with col3:
                st.write('Dismissal kind')
                st.dataframe(a)
            with col4:
                st.dataframe((pd.DataFrame(
                    {
                    'Best figures' : [best]
                    })))    


### TEAM STATS ###
def team_info(team):
    a = team+"'s IPL Statistics"
    st.subheader(a)
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

    col1, col2 = st.columns(2)
    with col1:
        st.write('Top 3 batsman and bowlers from',selected_team)
        st.dataframe(pd.concat([top_3_batsman,top_3_bowlers], axis=1))
    with col2:
        st.write(selected_team," achievments")
        st.dataframe({
            'Stats':['Highest Successful Runchase','Lowest Total Defended','Total Trophies'],
            'Values':[highest_successful_runchase,lowest_total_defended,total_trophies]
        })
    st.write(selected_team,'has qualified',sd[selected_team],'times for playoffs')
    
### TEAM VS TEAM STATS ###
def team_vs_team_info(team1,team2):
    if team1 == team2:
        st.write('You have selected same teams')
    elif mdf[((mdf['team1'] == team1) & (mdf['team2'] == team2)) | ((mdf['team1'] == team2) & (mdf['team2'] == team1))].shape[0] == 0:
        st.markdown('''unfortunately '''+team1+''' and '''+team2+''' have played 0 matches becasue of one one of the following reasons   
                    1. The time period in which '''+team1+''' was playing, '''+team2+''' was not even formed and vice versa  
                    2. The time period in which '''+team1+''' was playing, '''+team2+''' had stopped playing and vice versa  
                    3. The time period in which '''+team1+''' was playing, '''+team2+''' might got suspended from playing the IPL and vice versa
                    ''')
    else:
        total_matches = mdf[((mdf['team1'] == team1) & (mdf['team2'] == team2)) | ((mdf['team1'] == team2) & (mdf['team2'] == team1))].shape[0]
        ttdf = mdf[(((mdf['team1'] == team1) & (mdf['team2'] == team2)) | ((mdf['team1'] == team2) & (mdf['team2'] == team1))) & ((mdf['result'] == 'wickets') | ((mdf['result'] == 'runs')))]
        wins = ttdf['winner'].value_counts().reset_index().rename(columns={'winner':'Winning Team'})
        wins.index = wins.index+1

        col1, col2 = st.columns(2)
        with col1:
            st.write('Total Matches are',total_matches)
            st.dataframe(wins)
        with col2:
            if (mdf[((mdf['team1'] == team1) & (mdf['team2'] == team2)) | ((mdf['team1'] == team2) & (mdf['team2'] == team1))]['result'] == 'tie').sum() == 0:
                pass
            else:
                tttdf = mdf[(((mdf['team1'] == team1) & (mdf['team2'] == team2)) | ((mdf['team1'] == team2) & (mdf['team2'] == team1))) & ((mdf['result'] == 'tie'))]
                tie_wins = tttdf['winner'].value_counts().reset_index().rename(columns={'winner':'Winning Team'})
                tie_wins.index = tie_wins.index+1
                st.write('Number of Draw matches =',tttdf.shape[0])
                st.dataframe(tie_wins)
        st.text("")
        st.text("")
        if (mdf[((mdf['team1'] == team1) & (mdf['team2'] == team2)) | ((mdf['team1'] == team2) & (mdf['team2'] == team1))]['result'] == 'no result').sum() == 0:
            pass
        else:
            no_result_matches = mdf[((mdf['team1'] == team1) & (mdf['team2'] == team2) | (mdf['team1'] == team2) & (mdf['team2'] == team1)) & ((mdf['result'] == 'no result'))].shape[0]
            st.write('Total number of matches with no result =',no_result_matches)

        st.text("")
        st.text("")
        st.text("")
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
            col3, col4 = st.columns(2)
            with col3:
                st.write('Top scorer against',team)
                st.dataframe(batter)
            with col4:
                st.write('Top wicket taker for',team)
                st.dataframe(bowler)

#### Page Configuration
st.set_page_config(page_title="IPL Analysis", page_icon="🏏",layout="wide")
st.sidebar.title('IPL Insights & Predictions')

import base64

# Function to load and encode the local image
def load_image(image_file):
    with open(image_file, "rb") as image:
        return base64.b64encode(image.read()).decode()

# Load the local image
background_image = load_image("background.jpg")  # Replace with your actual image file name

# Inject CSS for the background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url(data:image/jpeg;base64,{background_image});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;  
        color: white;    
    }}
    </style>
    """,
    unsafe_allow_html=True
)

#### Above functions are used here
option = st.sidebar.selectbox('Main menu',['IPL Statistics','IPL winning Prediction'])
if option == 'IPL Statistics':
    option1 = st.sidebar.selectbox('Select type of statistics',['Player Stats','Player vs Team Stats','Team stats','Team vs Team Stats','Win Predictor'])
    if option1 == 'Player Stats':
        st.title('Player stats')
        selected_player = st.sidebar.selectbox('Select player',players_list)
        selected_Option = st.sidebar.selectbox('Select Type of Stats',['Batting Stats','Bowling Stats','Both'])
        btn1= st.sidebar.button('Fetch Results')   
        if btn1:
            if selected_Option == 'Batting Stats':
                bat_info(selected_player)
            elif selected_Option == 'Bowling Stats':
                ball_info(selected_player)
            else:
                bat_info(selected_player)
                ball_info(selected_player)

    elif option1 == 'Player vs Team Stats':
        st.title('Player vs Team Stats')
        selected_player = st.sidebar.selectbox('Select Player',players_list)
        selected_team = st.sidebar.selectbox('Select Team',team_list)
        selected_Option = st.sidebar.selectbox('Select Type of Stats',['Batting Stats','Bowling Stats','Both'])
        btn2 = st.sidebar.button('Fetch Results')
        if btn2:
            if selected_Option == 'Batting Stats':
                bat_vs_team_info(selected_player,selected_team)
            elif selected_Option == 'Bowling Stats':
                ball_vs_team_info(selected_player,selected_team)
            else:
                bat_vs_team_info(selected_player,selected_team)
                ball_vs_team_info(selected_player,selected_team)

    elif option1 == 'Team stats':
        st.title('Team stats')
        selected_team = st.sidebar.selectbox('Select Team',team_list)
        btn3 = st.sidebar.button('Fetch Results')
        if btn3:
            team_info(selected_team)        
        

    elif option1 == 'Team vs Team Stats':
        st.title('Team vs Team Stats')
        selected_team1 = st.sidebar.selectbox('Select Team1',team_list)
        selected_team2 = st.sidebar.selectbox('Select Team2',team_list)
        btn4 = st.sidebar.button('Fetch Results')
        if btn4:
            team_vs_team_info(selected_team1,selected_team2)
elif option == 'IPL winning Prediction':
    st.title('IPL Winning Prediction')
    pipe = pickle.load(open('pipe.pkl','rb'))
    col1, col2 = st.columns(2)
    with col1:
        batting_team = st.selectbox('Select batting team',sorted(team_list))
    with col2:
        bowling_team = st.selectbox('Select bowling team',sorted(team_list))
    venue = st.selectbox('Select venue',sorted(venue_list))
    target_runs = st.number_input('Target',max_value = 1200, min_value = 1)
    col3,col4,col5 = st.columns(3)
    with col3:
        Score = st.number_input('Score',max_value = 1200, min_value =0)
    with col4:
        Overs = st.number_input('Overs Completed',max_value = 20, min_value = 1)
    with col5:
        wickets_lost = st.number_input('Wickets Lost', max_value = 10, min_value = 0)
    if st.button('Predict Percentages'):
        if batting_team == bowling_team:
            st.write("You have selected same teams")
        elif (Overs == 0):
            st.write("Check the inputs")
        elif (wickets_lost == 10) | (Overs == 20):
            if (target_runs > Score):
                st.write(bowling_team," Won the match")
            elif(target_runs < Score):
                st.write(batting_team," Won the match")
            else:
                st.write("Its a tie")
        else:
            runs_left = target_runs - Score
            balls_left = 120 - (Overs*6)
            wickets_left = 10 - wickets_lost
            current_run_rate = Score/Overs
            required_run_rate = (runs_left*6)/balls_left 
            input_df = pd.DataFrame({
                    'batting_team':[batting_team],'bowling_team':[bowling_team],'venue':[venue],'runs_left':[runs_left],
                    'balls_left':[balls_left],'wickets_left':[wickets_left],'target_runs':[target_runs],'current_run_rate':[current_run_rate],
                    'required_run_rate':[required_run_rate]
            })
            result = pipe.predict_proba(input_df)
            loss_percentage = round(result[0][0],2)*100
            win_percentage = round(result[0][1],2)*100
            if win_percentage >=90:
                st.write("Given the current conditions,",batting_team," has an impressive ",win_percentage,"%","chance of winning the game")
                st.write("and as less as ",loss_percentage,"%","chance of loosing the game.")
            elif (win_percentage >= 70) & (win_percentage <= 89) :
                st.write(batting_team,"is in a strong position with a solid ",win_percentage,"%"," chance of taking the win! The game is theirs to lose!")
                st.write("Though there's still a ",loss_percentage,"%","chance of defeat.")
            elif (win_percentage >= 50) & (win_percentage <= 69):
                st.write("It's a close match, but",batting_team,"holds a promising ",win_percentage,"%","chance of securing the win")
                st.write("and",loss_percentage,"%"," risk of losing. It's still anyone's game!")
            elif (win_percentage >=30) & (win_percentage <= 49):
                st.write(batting_team," is up against the odds with a",win_percentage,"%"," chance of winning")
                st.write("and a ",loss_percentage,"%", "chance of losing, but a comeback is still possible if they push hard!")
            elif (win_percentage >=10) & (win_percentage <= 29):
                st.write(batting_team," is in a challenging position with just a ",win_percentage,"%"," chance of victory") 
                st.write("and a",loss_percentage,"%"," chance of defeat. It’s a long shot, but we have seen players pull off a miracle!")
            else:
                st.write(batting_team," has a only",win_percentage,"%"," chance of winning the game")
                st.write("and as high as ",loss_percentage,"%"," chance of loosing the game")
