players = [
    # Name, Role, BatAvg, SR, 30s, Inns, Econ, BowlSR, Wkts/Match, Dismissals, Matches
    ["Rohit Sharma", "RHB", 23.65, 142.22, 13, 44, 0, 0, 0, 0, 44],
    ["Tilak Varma", "LHB", 39.86, 145.54, 17, 22, 0, 0, 0, 0, 22],
    ["Suryakumar Yadav", "RHB", 39.19, 166.68, 15, 24, None, None, None, None, 24],
    ["Bevon Jacobs", "RHB", 30.66, 180.29, 1, 6, None, None, None, None, 6],
    ["Ryan Rickelton", "LHB,WK", 42.25, 156.12, 7, 17, None, None, None, 12, 17],
    ["Hardik Pandya", "RHB,AR,RHB", 26.14, 136.54, 10, 45, 9.1, 24.95, 0.5, None, 45],
    ["Mitchell Santner", "LHB,AR,OS", 7.6, 109, 0, 12, 6.7, 26.67, 0.75, None, 12],
    ["Karn Sharma", "LS", 7, 120.27, 0, 21, 8.39, 19.23, 1, None, 21],
    ["Trent Boult", "LHP,P", 14, 104.94, 0, 42, 8.34, 20.44, 1.07, None, 42],
    ["Jasprit Bumrah", "RHP,P", 9.33, 87.34, 0, 41, 7.05, 18.71, 1.36, None, 41],
    ["Deepak Chahar", "RHB,P", 1, 144, 0, 33, 8.14, 19.23, 1, None, 33],
    ["will jack", "RHB,OS", 32.86, 175.57, 1, 8, 11.11, 27, 0.25, 0, 8],
    ["Arjun Tendulkar", "LHB,P", 13, 144.44, 0, 4, 9.36, 19.67, 0.75, None, 4],
    ["naman dhir", "RHB", 23.33, 177.22, 2, 7, 0, 0, 0, None, 7],
    ['Reece Topley','LHP,P',0,0,0,1,7,20,1,None,1],
    ['Raj Angad B','LHB,RHP,AR',5.5,78.57,0,2,0,0,0,None,2]]


def calculate_score(player):                          
    name, role = player[0], player[1]
    batavg = player[2] or 0
    sr = player[3] or 0
    thirties = player[4] or 0
    inns = player[5] or 1
    econ = player[6] or 15
    bowl_sr = player[7] or 25
    wkts = player[8] or 0
    dismissals = player[9] or 0
    matches = player[10] or 1

    if "WK" in role:
        bat_score = 0.4 * batavg / 50 + 0.4 * sr / 150 + 0.2 * thirties / inns
        keep_score = dismissals / matches
        return 0.7 * bat_score + 0.3 * keep_score

    elif "AR" in role:
        bat_score = 0.4 * batavg / 50 + 0.4 * sr / 150 + 0.2 * thirties / inns
        bowl_score = 0.3 * (6/econ) + 0.4 * (25/bowl_sr) + 0.3 * (wkts/3)
        return 0.5 * bat_score + 0.5 * bowl_score

    elif "P" in role or "OS" in role or "LS" in role:
        return 0.3 * (6/econ) + 0.4 * (25/bowl_sr) + 0.3 * (wkts/3)

    else:
        return 0.4 * batavg / 50 + 0.4 * sr / 150 + 0.2 * thirties / inns


for player in players:
    score = calculate_score(player)
    print(f"{player[0]:<20} | Role: {player[1]:<12} | Success Score: {score:.3f}")

#______________________________________________________________________________________


from itertools import combinations
success_scores = [0.628,0.862,0.883,0.759,0.797,0.633,0.535,0.835,0.812,0.926,0.841,0.557,0.776,0.520,0.857,0.387]
LHB   = [1,4]
RHB   = [0,2,3]
Pacers = [8,9,10,12,14]
LeftPacers = [8,15]
OffSpinAR = [6]
LegSpinners = [7]
WK = [4]
ARP = [5,11,15]
Foreign = [3,4,6,8,11,14]
def is_valid(team):
    if sum(1 for i in team if i in Foreign) > 4: return False
    if sum(1 for i in team if i in Pacers) > 3: return False
    if sum(1 for i in team if i in LeftPacers) < 1: return False
    if sum(1 for i in team if i in OffSpinAR) < 1: return False
    if sum(1 for i in team if i in LegSpinners) < 1: return False
    if sum(1 for i in team if i in WK) < 1: return False
    if sum(1 for i in team if i in LHB) < 2: return False
    if sum(1 for i in team if i in RHB) < 2: return False
    if sum(1 for i in team if i in ARP) < 1: return False
    return True
best_score = -1
best_team = []

for team in combinations(range(16), 11):
    if is_valid(team):
        score = sum(success_scores[i] for i in team)
        if score > best_score:
            best_score = score
            best_team = team
print("Best Team (0-indexed player numbers):", best_team)
print('Where')
for i in range(16):
    print(players[i][0],':',i)
