import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timezone

# TEAM REFERENCE

# LEAGUE TABLE
LEAGUE_TABLE_TEAM = "Leicester"
LEAGUE_TABLE_TITLE = "#Premier League Table"
LEAGUE_TABLE_SOURCE = "https://www.bbc.co.uk/sport/football/premier-league/table"
LEAGUE_TABLE_SHOW_TEAMS = 6 # Show this many teams
LEAGUE_TABLE_NUM_TEAMS = 20 # Total number of teams in the league.

def GetLeagueTableData(update_time):
    raw_data = pd.read_html(LEAGUE_TABLE_SOURCE)
    table = raw_data[0]

    if "Live" in table.columns:
        print("WARNING: Games are in progress. Table will be out of date very fast.")

    table.rename(columns = {'Unnamed: 0':'Pos', 'F':'Goals'}, inplace=True)
    table.rename(columns = {'Live':'Pos'}, inplace=True)

    table = table.drop(columns=['Unnamed: 1','Form','L','A'], axis=1)
    table = table.head(20)

    team_mask = table['Team'] == TEAM
    base_pos = np.flatnonzero(team_mask)
    if base_pos.size == 0:
        print("ERROR: There is no team named " + TEAM + " in the table.")
        exit()
    team_index = base_pos[0]
    #team_index = table.iloc[base_pos]

    starting_pos = team_index - int(LEAGUE_TABLE_SHOW_TEAMS / 2)
    min_starting_pos = 0
    max_starting_pos = LEAGUE_TABLE_NUM_TEAMS - LEAGUE_TABLE_SHOW_TEAMS
    starting_pos = min(max_starting_pos,max(min_starting_pos,starting_pos))

    table = table.iloc[range(starting_pos,starting_pos + LEAGUE_TABLE_SHOW_TEAMS)]

    table_result = table.to_markdown(index=False)
    
    source_string = "[Source](" + LEAGUE_TABLE_SOURCE + ")"
    return '\n\n'.join([LEAGUE_TABLE_TITLE,table_result,source_string,update_time])
    

current_time = datetime.now(timezone.utc)
timestamp = current_time.strftime("^Last ^updated ^at ^%H:%M:%S-%d-%b-%Y")
print(GetLeagueTableData(timestamp))
