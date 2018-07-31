def rename_cols(input_df):
    input_df.rename(columns = {3: 'Visiting Team', 6: 'Home Team', 9: 'Runs Visitor', 10: 'Runs Home'}, inplace=True)
    return input_df


def add_new_cols(input_df):
    input_df['Home Win'] = (input_df['Runs Home'] > input_df['Runs Visitor'])
    input_df['Visitor Win'] = (input_df['Runs Visitor'] > input_df['Runs Home'])
    return input_df


def proc_home_team_data(input_df):

    # Group by home team
    home_group = input_df.groupby(input_df['Home Team'])

    # Compute stats: Number of games, runs scored, runs conceded, wins, run differential
    home_df = home_group[['Runs Visitor', 'Runs Home', 'Home Win']].apply(sum)
    home_df['Home Games'] = home_group['Home Win'].count()
    home_df.rename(columns = {'Runs Visitor': 'Runs by Visitor', 'Runs Home': 'Runs at Home', 'Home Win': 'Wins at Home'}, inplace=True)
    home_df['RD at Home'] = home_df['Runs at Home'] - home_df['Runs by Visitor']
    home_df.index.rename('Team', inplace=True)
    home_df.reset_index(inplace=True)

    return home_df



def proc_visiting_team_data(input_df):

    # Group by visiting team
    visit_group = input_df.groupby(input_df['Visiting Team'])

    # Compute stats: Number of games, runs scored, runs conceded, wins, run differential
    visit_df = visit_group[['Runs Visitor', 'Runs Home', 'Visitor Win']].apply(sum)
    visit_df['Road Games'] = visit_group['Visitor Win'].count()
    visit_df.rename(columns = {'Runs Visitor': 'Runs as Visitor', 'Runs Home': 'Runs by Home', 
                                 'Visitor Win': 'Wins as Visitor'}, inplace=True)
    visit_df['RD as Visitor'] = visit_df['Runs as Visitor'] - visit_df['Runs by Home']
    visit_df.index.rename('Team', inplace=True)
    visit_df.reset_index(inplace=True)

    return visit_df




def merge_data_frames(home_df, visit_df):
    # Compute explanatory and response variables
    overall_df = home_df.merge(visit_df, how='outer', left_on='Team', right_on='Team')
    overall_df['RD'] = overall_df['RD at Home'] + overall_df['RD as Visitor']
    overall_df['Win Pct'] = (overall_df['Wins at Home'] + overall_df['Wins as Visitor']) / (overall_df['Home Games'] + overall_df['Road Games'])

    # Return dataframe with explanatory and response variables
    return overall_df



def extract_linear_reg_inputs(input_df):
    # Rename columns
    input_df = rename_cols(input_df)

    # Add new columns
    input_df = add_new_cols(input_df)

    # Group and process data by home team
    home_df = proc_home_team_data(input_df)

    # Group and process data by visiting team
    visit_df = proc_visiting_team_data(input_df)

    # Merge home and visitor dataframes
    overall_df = merge_data_frames(home_df, visit_df)

    return overall_df