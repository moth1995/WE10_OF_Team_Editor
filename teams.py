from editor.club import Club

def get_players_nations(of, team_id):
    players=[]
    for i in range (0, 23):
        players.append(int.from_bytes(of.data[nations_players_relink_offset + (i * 2) + (team_id * nations_players_relink_size) : nations_players_relink_offset + (i * 2) + 2  + (team_id * nations_players_relink_size)], byteorder='little'))
    return players

def get_players_clubs(of, team_id):
    team_id-=first_club_team_id
    players=[]
    for i in range (0, 32):
        players.append(int.from_bytes(of.data[clubs_players_relink_offset + (i * 2) + (team_id * clubs_players_relink_size) : clubs_players_relink_offset + (i * 2) + 2 + (team_id * clubs_players_relink_size)], byteorder='little'))
    return players

def get_players_ml(of):
    players=[]
    for i in range (0, 32):
        players.append(int.from_bytes(of.data[ml_players_relink_offset + (i * 2) : ml_players_relink_offset + (i * 2) + 2], byteorder='little'))
    return players

def get_formation(of, team_id):
    if first_nat_team_id <= team_id <= last_nat_team_id:
        formation_data = of.data[nations_formation_data_offset + (team_id * formation_data_size) : nations_formation_data_offset + formation_data_size + (team_id * formation_data_size) ]
    elif first_club_team_id <= team_id <= last_club_team_id:
        formation_data = of.data[clubs_formation_data_offset + ((team_id - first_club_team_id) * formation_data_size) : clubs_formation_data_offset + formation_data_size + ((team_id - first_club_team_id) * formation_data_size) ]
    return formation_data

def get_formation_generic(of, team_id):
    if first_nat_team_id <= team_id <= last_nat_team_id:
        formation_data = of.data[nations_formation_data_offset + (team_id * formation_data_size) + 3 : nations_formation_data_offset + formation_data_size + (team_id * formation_data_size) ]
    elif first_club_team_id <= team_id <= last_club_team_id:
        formation_data = of.data[clubs_formation_data_offset + ((team_id - first_club_team_id) * formation_data_size) + 3: clubs_formation_data_offset + formation_data_size + ((team_id - first_club_team_id) * formation_data_size) ]
    return formation_data

def set_formation(of, team_id, formation_data):
    if first_nat_team_id <= team_id <= last_nat_team_id:
        for i, byte in enumerate(formation_data):
            of.data[nations_formation_data_offset+(team_id*formation_data_size) + i] = byte
    elif first_club_team_id <= team_id <= last_club_team_id:
        for i, byte in enumerate(formation_data):
            of.data[clubs_formation_data_offset+((team_id - first_club_team_id)*formation_data_size) + i] = byte

def set_formation_generic(of, team_id, formation_data):
    if first_nat_team_id <= team_id <= last_nat_team_id:
        for i, byte in enumerate(formation_data):
            of.data[nations_formation_data_offset + 3 + (team_id*formation_data_size) + i] = byte
    elif first_club_team_id <= team_id <= last_club_team_id:
        for i, byte in enumerate(formation_data):
            of.data[clubs_formation_data_offset+ 3 + ((team_id - first_club_team_id)*formation_data_size) + i] = byte

first_nat_team_id = 0
last_nat_team_id = 63
first_club_team_id = 64
last_club_team_id = 202

nations_players_relink_offset = 664306
nations_players_relink_size = 46
clubs_players_relink_offset = 667710
clubs_players_relink_size = 64
nations_jersey_number_offset = 657932
nations_jersey_number_size = 23
clubs_jersey_number_offset = 659634
clubs_jersey_number_size = 32
clubs_names_offset = Club.start_address
clubs_names_size = Club.size
three_letter_clubs_name_offset = 773869
three_letter_clubs_name_size = 3
nations_formation_data_offset = 677056
clubs_formation_data_offset = 700352
formation_data_size = 364
nations_kits_data_offset = 762752
clubs_kits_data_offset = 785280
nations_kits_data_size = 352
clubs_kits_data_size = 544

ml_players_relink_offset = 676542
