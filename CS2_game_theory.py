import nashpy as nash
import numpy as np
import matplotlib.pyplot as plt
import random
import mplcursors

# Initial conditions:

complete_options_list = [
                        [0.50, 0.35, 0.20, 0.05],
                        [0.65, 0.50, 0.40, 0.15],
                        [0.80, 0.60, 0.50, 0.25],
                        [0.95, 0.85, 0.75, 0.50]
                        ]

win_rewards = [2, 1.5, 1, 1]
loss_rewards = [1.5, 0.5, -0.5, -2]

def gen_opts(eco1, eco2):
    """
    Generates a submatrix of complete_options_list with number of rows equal to eco1 and number of columns equal to eco2, 
    thus giving the game matrix for the given stage of the game based on both players eco.

    Parameters
    ----------
    eco1 : int or float
        The economy of player 1 at this stage of the game.
    eco2 : int or float
        The economy of player 2 at this stage of the game.

    Returns
    -------
    np.array
        A 2D numpy array representing the game matrix for the current stage of the game.

    """
    avaliable_outcomes = []
    for i in range(0, min(4, int(eco1))):
        sublist = []
        for j in range(0, min(4, int(eco2))):
            sublist.append(complete_options_list[i][j])
        avaliable_outcomes.append(sublist)
    return np.array(avaliable_outcomes)

def two_player_game(player1_strat, player2_strat, starting_points=(0, 0), starting_money=(1, 1), max_money=15, 
                    first_to_or_set_number="first to",  play_to=13, n=5, loss_bonuses=True, start_loss_bonus=0):
    """
    Plays a game with a given number of rounds or until a player reaches a certain number of points with two strategies against each other 
    and returns their money over time and points over time.

    Parameters
    ----------
    player1_strat : function
        The strategy function for player 1.
    player2_strat : function
        The strategy function for player 2.
    starting_points : tuple, optional
        The starting points for player 1 and player 2, by default (0, 0).
    starting_money : tuple, optional
        The starting money for player 1 and player 2, by default (1, 1).
    max_money : int or float, optional
        The maximum money a player can have, by default 15.
    first_to_or_set_number : str, optional
        If "first to", the game ends when a player reaches the play_to points. 
        If "set number", the game ends after play_to rounds.
        By default "first to".
    play_to : int or float, optional
        The number of points to play to or the number of rounds to play, by default 13.
    n : int, optional
        A chosen value for strategies such as eco_first_n_rounds, by default 5.
    loss_bonuses : bool, optional
        If True, players receive a loss bonus after losing a round, by default True.
    start_loss_bonus : int, optional
        The starting loss bonus for both players, by default 0.

    Returns
    -------
    tuple
        A tuple containing two lists; points_over_time and money_over_time.
        points_over_time : list
            A list of lists, where each inner list contains the points of player 1 and player 2 at each round.
        money_over_time : list
            A list of lists, where each inner list contains the money of player 1 and player 2 at each round.

    """
    money = [starting_money[0], starting_money[1]]
    points = [starting_points[0], starting_points[1]]
    points_over_time = [[starting_points[0],starting_points[1]]]
    money_over_time = [[starting_money[0],starting_money[1]]]
    round_number = 0
    losses_bonus1, losses_bonus2 = start_loss_bonus, start_loss_bonus
    two_player_game.player1choices = []
    two_player_game.player2choices = []

    if first_to_or_set_number == "first to":
        while max(points[0],points[1]) < play_to:
            game_matrix = gen_opts(money[0], money[1])
            strat1 = player1_strat(round_number, money[0], money[1], game_matrix, 0, n, losses_bonus1, losses_bonus2, first_half=accurate_cs_game.first_half)
            strat2 = player2_strat(round_number, money[1], money[0], game_matrix, 1, n, losses_bonus1, losses_bonus2, first_half=accurate_cs_game.first_half)
            loss_rewards1 = [1.5 + (0.5 * losses_bonus1), 0.5 + (0.5 * losses_bonus1), -0.5 + (0.5 * losses_bonus1), -2 + (0.5 * losses_bonus1)]
            loss_rewards2 = [1.5 + (0.5 * losses_bonus2), 0.5 + (0.5 * losses_bonus2), -0.5 + (0.5 * losses_bonus2), -2 + (0.5 * losses_bonus2)]

            rand_value = random.random()
            j = 0
            for i in range(0, len(strat1)):
                j += strat1[i]
                if rand_value < j:
                    p1_choice = i
                    break
            rand_value = random.random()
            j = 0
            for i in range(0, len(strat2)):
                j += strat2[i]
                if rand_value < j:
                    p2_choice = i
                    break
            two_player_game.player1choices.append(p1_choice)
            two_player_game.player2choices.append(p2_choice)
            roll=random.random()
            if game_matrix[p1_choice][p2_choice] > roll:
                money[0] += win_rewards[p1_choice]
                points[0] += 1
                if loss_bonuses == True:
                    if losses_bonus2 < 4:
                        losses_bonus2 += 1
                    if losses_bonus1 > 0:
                        losses_bonus1 -= 1
                money[1] += loss_rewards2[p2_choice]
                loser=2
            else:
                money[1] += win_rewards[p2_choice]
                points[1] += 1
                if loss_bonuses == True:
                    if losses_bonus1 < 4:
                        losses_bonus1 += 1
                    if losses_bonus2 > 0:
                        losses_bonus2 -= 1
                money[0] += loss_rewards1[p1_choice]
                loser=1
            
            money[0] = min(money[0],max_money)
            money[1] = min(money[1],max_money)
            #print("game matrix:\n"+str(game_matrix)+"\np1 strat: "+str(p1_choice+1)+"\np2 strat: "+str(p2_choice+1)+"\n roll: "+str(roll))
            #print(round_number)
            #print("player "+str(loser)+" loses and recieves a loss bonus of "+str([losses_bonus1,losses_bonus2][loser-1]))
            #print("player "+str((loser%2)+1)+" wins and maintains a loss bonus of "+str([losses_bonus2,losses_bonus1][(loser-1)]))
            #print(losses_bonus1,losses_bonus2)
            #print(points_over_time)
            points_over_time.append([points[0], points[1]])
            money_over_time.append([money[0],money[1]])
            round_number += 1

    else:
        while round_number < play_to:
            game_matrix = gen_opts(money[0], money[1])
            strat1 = player1_strat(round_number, money[0], money[1], game_matrix, 0, n, losses_bonus1, losses_bonus2, first_half=accurate_cs_game.first_half)
            strat2 = player2_strat(round_number, money[1], money[0], game_matrix, 1, n, losses_bonus1, losses_bonus2, first_half=accurate_cs_game.first_half)
            loss_rewards1 = [1.5 + (0.5 * losses_bonus1), 0.5 + (0.5 * losses_bonus1), -0.5 + (0.5 * losses_bonus1), -2 + (0.5 * losses_bonus1)]
            loss_rewards2 = [1.5 + (0.5 * losses_bonus2), 0.5 + (0.5 * losses_bonus2), -0.5 + (0.5 * losses_bonus2), -2 + (0.5 * losses_bonus2)]
            
            rand_value = random.random()
            j = 0
            for i in range(0, len(strat1)):
                j += strat1[i]
                if rand_value < j:
                    p1_choice = i
                    break
            rand_value = random.random()
            j = 0
            for i in range(0, len(strat2)):
                j += strat2[i]
                if rand_value < j:
                    p2_choice = i
                    break
            two_player_game.player1choices.append(p1_choice)
            two_player_game.player2choices.append(p2_choice)
            roll=random.random()
            if game_matrix[p1_choice][p2_choice] > roll:
                money[0] += win_rewards[p1_choice]
                points[0] += 1
                if loss_bonuses == True:
                    if losses_bonus2 < 4:
                        losses_bonus2 += 1
                    if losses_bonus1 > 0:
                        losses_bonus1 -= 1
                money[1] += loss_rewards2[p2_choice]
                loser=2
            else:
                money[1] += win_rewards[p2_choice]
                points[1] += 1
                if loss_bonuses == True:
                    if losses_bonus1 < 4:
                        losses_bonus1 += 1
                    if losses_bonus2 > 0:
                        losses_bonus2 -= 1
                money[0] += loss_rewards1[p1_choice]
                loser=1
            
            money[0] = min(money[0],max_money)
            money[1] = min(money[1],max_money)
            #print("game matrix:\n"+str(game_matrix)+"\np1 strat: "+str(p1_choice+1)+"\np2 strat: "+str(p2_choice+1)+"\n roll: "+str(roll))
            #print("player "+str(loser)+" loses and recieves a loss bonus of "+str([losses_bonus1,losses_bonus2][loser-1]))
            #print("player "+str((loser%2)+1)+" wins and maintains a loss bonus of "+str([losses_bonus2,losses_bonus1][(loser-1)]))
            #print(losses_bonus1,losses_bonus2)
            #print(points_over_time)
            points_over_time.append([points[0], points[1]])
            money_over_time.append([money[0],money[1]])
            round_number += 1

    return points_over_time.copy(), money_over_time.copy()

def extensive_form_game_into_normal_form_2_rounds(eco_player1, eco_player2, loss_reward_mult_player1, loss_reward_mult_player2):
    """
    Explanation...
    """
    outcome_game_win_matrix = []
    outcome_game_loss_matrix = []
    starting_game_matrix = gen_opts(eco1=eco_player1, eco2=eco_player2).tolist()
    for i in range(len(starting_game_matrix)):              #row player choice
        for j in range(len(starting_game_matrix[i])):       #column player choice
            win_current_player1eco = eco_player1 + win_rewards[i]
            loss_current_player2eco = eco_player2 + loss_reward_mult_player2 * 0.5 + loss_rewards[j]
            loss_current_player1eco = eco_player1 + loss_reward_mult_player1 * 0.5 + loss_rewards[i]
            win_current_player2eco = eco_player2 + win_rewards[j]
            p1_win_matrix = (np.multiply(gen_opts(win_current_player1eco, loss_current_player2eco), starting_game_matrix[i][j]) + starting_game_matrix[i][j]).tolist()
            p1_loss_matrix = (np.multiply(gen_opts(loss_current_player1eco, win_current_player2eco), (1 - starting_game_matrix[i][j])) + starting_game_matrix[i][j]).tolist()     #how to add a set number to every element in a matrix / nested list
            outcome_game_win_matrix.append(p1_win_matrix)
            outcome_game_loss_matrix.append(p1_loss_matrix)

    ecowin = []
    lilwin = []
    halfwin = []
    fullwin = []
    for i in range(len(outcome_game_win_matrix)):
        if i // len(starting_game_matrix[0]) == 0:
            ecowin.append(outcome_game_win_matrix[i])
        if i // len(starting_game_matrix[0]) == 1:
            lilwin.append(outcome_game_win_matrix[i])
        if i // len(starting_game_matrix[0]) == 2:
            halfwin.append(outcome_game_win_matrix[i])
        if i // len(starting_game_matrix[0]) == 3:
            fullwin.append(outcome_game_win_matrix[i])

    eco_row_sum_win = []
    lil_row_sum_win = []
    half_row_sum_win = []
    full_row_sum_win = []
    for i in ecowin:
        for j in i:
            eco_row_sum_win.append((sum(j) / len(j)))
    for i in lilwin:
        for j in i:
            lil_row_sum_win.append((sum(j) / len(j)))
    for i in halfwin:
        for j in i:
            half_row_sum_win.append((sum(j) / len(j)))
    for i in fullwin:
        for j in i:
            full_row_sum_win.append((sum(j) / len(j)))

    ecoloss = []
    lilloss = []
    halfloss = []
    fullloss = []
    for i in range(len(outcome_game_loss_matrix)):
        if i // len(starting_game_matrix[0]) == 0:
            ecoloss.append(outcome_game_loss_matrix[i])
        if i // len(starting_game_matrix[0]) == 1:
            lilloss.append(outcome_game_loss_matrix[i])
        if i // len(starting_game_matrix[0]) == 2:
            halfloss.append(outcome_game_loss_matrix[i])
        if i // len(starting_game_matrix[0]) == 3:
            fullloss.append(outcome_game_loss_matrix[i])

    eco_row_sum_loss = []
    lil_row_sum_loss = []
    half_row_sum_loss = []
    full_row_sum_loss = []
    for i in ecoloss:
        for j in i:
            eco_row_sum_loss.append((sum(j) / len(j)))
    for i in lilloss:
        for j in i:
            lil_row_sum_loss.append((sum(j) / len(j)))
    for i in halfloss:
        for j in i:
            half_row_sum_loss.append((sum(j) / len(j)))
    for i in fullloss:
        for j in i:
            full_row_sum_loss.append((sum(j) / len(j)))
    
    maximum_row_sums = []
    if len(eco_row_sum_win) != 0: 
        maximum_row_sums.append(max(eco_row_sum_win) + max(eco_row_sum_loss))
    if len(lil_row_sum_win) != 0:
        maximum_row_sums.append(max(lil_row_sum_win) + max(lil_row_sum_loss))
    if len(half_row_sum_win) != 0:
        maximum_row_sums.append(max(half_row_sum_win) + max(half_row_sum_loss))
    if len(full_row_sum_win) != 0:
        maximum_row_sums.append(max(full_row_sum_win) + max(full_row_sum_loss))
    if len(maximum_row_sums) == 0:
        return None
    index_of_max = maximum_row_sums.index(max(maximum_row_sums))
    return index_of_max

### THE STRAT ZONE ###

def support_enumerator_strat(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    Pick first equilibria it finds, dunno if this should be a stratergy...
    """
    support_enumerator_strat.stratname = "support enumerated"
    equilibria = nash.Game(game_matrix).support_enumeration()
    eq = next(equilibria)
    strat = list(eq)
    #print(f"player {player0_or_1} has strat:{strat[player0_or_1]} giving odds {complete_options_list[list(strat[player0_or_1]).index(1)]}")
    return strat[player0_or_1]

def short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    A strategy which picks the best option avaliable for winning the current round.

    Parameters
    ----------
    hmmm if we get rid of support ennumeration this would be hella smaller like half the size (just the docstring)

    """
    short_term.stratname = "short term"
    return [0] * min(int(eco) - 1, 3) + [1]

def eco_til_4_strat(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    A strategy which saves until its eco is greater than or equal to 4.
    """
    eco_til_4_strat.stratname = "eco til 4"
    strat = [0, 0, 0, 1]
    if eco < 4:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    return strat

def eco_til_n_eco(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    A strategy which saves until its eco is greater than or equal to a given n.
    """
    eco_til_n_eco.stratname = "eco til n eco"
    strat = [0] * min(int(eco) - 1, 3) + [1]
    if eco < n:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    return strat

def eco_first_n_rounds(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=5, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    A strategy which saves for the first n rounds, then just plays short_term.
    """
    eco_first_n_rounds.stratname = "eco first " + str(n) + " rounds"
    strat = [0] * min(int(eco) - 1, 3) + [1]
    if round_number < n:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    return strat
    
def eco_first_n_rounds_and_stay_above_m_eco(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=5, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    ecos for the first n rounds
    afterwhich it plays short_term but ecos if eco falls below m
    """
    m=4
    eco_first_n_rounds_and_stay_above_m_eco.stratname = "eco first " + str(n) + " and stay above " + str(m) + " eco"
    strat = [0] * min(int(eco) - 1, 3) + [1]
    if round_number <= n or eco < m:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    return strat

def random_strat(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    pick a random option with equal likelyhood
    """
    random_strat.stratname = "random"
    return [1 / min(int(eco), 4)] * min(int(eco), 4)

def eco_til_death(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    always ecos
    """
    eco_til_death.stratname = "champ"
    return [1] + [0] * min(int(eco) - 1, 3)

def bi4nxt(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    ecos till it can fullbuy
    if it can fulbuy nextround picking a stronger option than ecoing, it will do so
    """
    bi4nxt.stratname = "buy for next"
    strat = [0, 0, 0, 1]
    if eco == 3.5:
        strat = [0] + [1] * min((int(eco) - 2), 2)
    if eco < 3.5:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    if eco > 3.5:
        strat = [0, 0, 0, 1]
    return strat

def never_half(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    plays short_term, but littlebuys instead of halfbuys
    """
    never_half.stratname = "never half"
    if eco < 3 or eco > 4:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    else:
        strat = [0, 1, 0]
    return strat

def eco_first_n_rounds_then_lil_then_short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=5, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    ecos n rounds, then little buys FOR 1 ROUND, then just plays short term
    """
    eco_first_n_rounds_then_lil_then_short_term.stratname = "eco first " + str(n) + " then 1 lilbuy then short term"
    if round_number < n:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    if round_number == n:
        if eco < 2:
            strat = [1]
        if 2 <= eco < 3:
            strat = [0, 1]
        if 3 <= eco < 4:
            strat = [0, 1, 0]
        if eco >= 4:
            strat = [0, 1, 0, 0]
    if round_number > n:
        strat = min(int(eco) - 1, 3) * [0] + [1]
    return strat

def eco_first_n_rounds_then_half_then_short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=5, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    ecos n rounds, then half buys FOR 1 ROUND, then just plays short term
    """
    eco_first_n_rounds_then_half_then_short_term.stratname = "eco first " + str(n) + " then 1 halfbuy then short term"
    if round_number < n:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    if round_number == n:
        if eco < 2:
            strat = [1]
        if 2 <= eco < 3:
            strat = [1, 0]
        if 3 <= eco < 4:
            strat = [0, 0, 1]
        if eco >= 4:
            strat = [0, 0, 1, 0]
    if round_number > n:
        strat = min(int(eco) - 1, 3) * [0] + [1]
    return strat

def eco_if_down_on_money(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=5, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    eco when less money than opponent
    """
    eco_if_down_on_money.stratname = "eco when down on money"
    if eco < op_eco:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    else:
        strat = min(int(eco) - 1, 3) * [0] + [1]
    return strat

def bi4nxt_2_rounds(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=5, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    Finds the best option for including the next 3 rounds based on expected wins and eco.
    """
    bi4nxt_2_rounds.stratname = "buy for next 2 rounds"
    strat = [0] * min(int(eco), 4)
    index_of_choice = extensive_form_game_into_normal_form_2_rounds(eco, op_eco, losses_bonus1, losses_bonus2)
    strat[index_of_choice] = 1
    return strat

def support_enumerator_strat2(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    Pick first equilibria it finds, dunno if this should be a stratergy...
    """
    support_enumerator_strat2.stratname = "support enumerated 2"
    equilibria = nash.Game(game_matrix).support_enumeration()
    eq = next(equilibria)
    strat = list(eq)
    if round_number == 13:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    if round_number == 12 and first_half == True:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    #print(f"player {player0_or_1} has strat:{strat[player0_or_1]} giving odds {complete_options_list[list(strat[player0_or_1]).index(1)]}")
    return strat[player0_or_1]

def eco_til_4_strat2(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    A strategy which saves until its eco is greater than or equal to 4.
    """
    eco_til_4_strat2.stratname = "eco til 4 pt.2"
    strat = [0, 0, 0, 1]
    if eco < 4:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    if round_number == 13:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    if round_number == 12 and first_half == True:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    return strat

def eco_til_n_eco2(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=5, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    A strategy which saves until its eco is greater than or equal to a given n.
    """
    eco_til_n_eco2.stratname = "eco til n eco 2"
    strat = [0] * min(int(eco) - 1, 3) + [1]
    if eco < n:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    if round_number == 13:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    if round_number == 12 and first_half == True:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    return strat

def eco_first_n_rounds2(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=5, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    A strategy which saves for the first n rounds, then just plays short_term.
    """
    eco_first_n_rounds2.stratname = "eco first " + str(n) + " rounds 2"
    strat = [0] * min(int(eco) - 1, 3) + [1]
    if round_number < n:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    if round_number == 13:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    if round_number == 12 and first_half == True:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    return strat
    
def eco_first_n_rounds_and_stay_above_m_eco2(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=5, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    ecos for the first n rounds
    afterwhich it plays short_term but ecos if eco falls below m
    """
    m=4
    eco_first_n_rounds_and_stay_above_m_eco2.stratname = "eco first " + str(n) + " and stay above " + str(m) + " eco 2"
    strat = [0] * min(int(eco) - 1, 3) + [1]
    if round_number <= n or eco < m:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    if round_number == 13:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    if round_number == 12 and first_half == True:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    return strat

def bi4nxt2(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    ecos till it can fullbuy
    if it can fulbuy nextround picking a stronger option than ecoing, it will do so
    """
    bi4nxt2.stratname = "buy for next 2"
    strat = [0, 0, 0, 1]
    if eco == 3.5:
        strat = [0] + [1] * min((int(eco) - 2), 2)
    if eco < 3.5:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    if eco > 3.5:
        strat = [0, 0, 0, 1]
    if round_number == 13:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    if round_number == 12 and first_half == True:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    return strat

def never_half2(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    plays short_term, but littlebuys instead of halfbuys
    """
    never_half2.stratname = "never half 2"
    if eco < 3 or eco > 4:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0, first_half=False)
    else:
        strat = [0, 1, 0]
    if round_number == 13:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    if round_number == 12 and first_half == True:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    return strat

def eco_if_down_on_money2(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=5, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    eco when less money than opponent
    """
    eco_if_down_on_money2.stratname = "eco when down on money 2"
    if eco < op_eco:
        strat = [1] + [0] * min(int(eco) - 1, 3)
    else:
        strat = min(int(eco) - 1, 3) * [0] + [1]
    if round_number == 13:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    if round_number == 12 and first_half == True:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    return strat

def bi4nxt_2_rounds2(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=5, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    Finds the best option for including the next 3 rounds based on expected wins and eco.
    """
    bi4nxt_2_rounds2.stratname = "buy for next 2 rounds pt.2"
    strat = [0] * min(int(eco), 4)
    index_of_choice = extensive_form_game_into_normal_form_2_rounds(eco, op_eco, losses_bonus1, losses_bonus2)
    strat[index_of_choice] = 1
    if round_number == 13:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    if round_number == 12 and first_half == True:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    return strat

def eco_til_death2(round_number, eco, op_eco, game_matrix, player0_or_1=0, n=0, losses_bonus1=0, losses_bonus2=0, first_half=False):
    """
    always ecos
    """
    eco_til_death2.stratname = "champ 2"
    strat = [1] + [0] * min(int(eco) - 1, 3)
    if round_number == 13:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    if round_number == 12 and first_half == True:
        strat = short_term(round_number, eco, op_eco, game_matrix, player0_or_1=0)
    return strat

### now leaving THE STRAT ZONE ###

def accurate_cs_game(strat1, strat2, n=5, loss_bonuses=True):
    """
    A function to create an accurate game of counterstrike.

    Parameters
    ----------
    strat1 : function
        The strategy function for player 1.
    strat2 : function
        The strategy function for player 2.
    n : int, optional
        A chosen value for strategies such as eco_first_n_rounds, by default 5.
    loss_bonuses : bool, optional
        If True, players receive a loss bonus after losing a round, by default True.

    Returns
    -------
    tuple
        A tuple containing two lists; points_over_time and money_over_time.
        points_over_time : list
            A list of lists, where each inner list contains the points of player 1 and player 2 at each round.
        money_over_time : list
            A list of lists, where each inner list contains the money of player 1 and player 2 at each round.

    """
    accurate_cs_game.player1choices = []
    accurate_cs_game.player2choices = []
    accurate_cs_game.first_half = True
    points_over_time, money_over_time = two_player_game(player1_strat=strat1, player2_strat=strat2, starting_points=(0, 0), max_money=16, 
                                                        first_to_or_set_number="set number", play_to=12, n=n, loss_bonuses=loss_bonuses)
    accurate_cs_game.player1choices.append(two_player_game.player1choices)
    accurate_cs_game.player2choices.append(two_player_game.player2choices)
    next_half_points_over_time, next_half_money_over_time = two_player_game(player1_strat=strat1, player2_strat=strat2, 
                                                                            starting_points=(0, 0),starting_money=(1, 1), max_money=16, 
                                                                            first_to_or_set_number="set number", play_to=13, n=n, 
                                                                            loss_bonuses=loss_bonuses)
    accurate_cs_game.player1choices.append(two_player_game.player1choices)
    accurate_cs_game.player2choices.append(two_player_game.player2choices)
    for i in next_half_points_over_time:
        points_over_time.append([points_over_time[12][0] + i[0], points_over_time[12][1] + i[1]])
    for i in next_half_money_over_time:
        money_over_time.append(i)
    for i in range(0, len(points_over_time)):
        if max(points_over_time[i]) >= 13:
            del points_over_time[i + 1:]
            del money_over_time[i + 1:]
            break
    return points_over_time, money_over_time

def unpack_points_over_time_and_money_over_time(game_outcome, money_outcome):
    """
    A function to take game_outcome and money_outcome and from that return each teams scores and money at all rounds.

    Parameters
    ----------
    game_outcome : list
        A list of lists, where each inner list contains the points of player 1 and player 2 at each round.
    money_outcome : list
        A list of lists, where each inner list contains the money of player 1 and player 2 at each round.
    
    Returns
    -------
    tuple
        A tuple containing four lists; team1score, team2score, team1money and team2money.
        team1score : list
            A list of the scores over rounds of player 1.
        team2score : list
            A list of the scores over rounds of player 2.
        team1money : list
            A list of the money over rounds of player 1.
        team2money : list
            A list of the money over rounds of player 2.

    """
    team1score=[]
    team2score=[]
    team1money=[]
    team2money=[]
    for i in game_outcome:
        team1score.append(i[0])
        team2score.append(i[1])

    for i in money_outcome:
        team1money.append(i[0])
        team2money.append(i[1])
    return team1score, team2score, team1money, team2money

def graph_it_out(team1score, team2score, team1money, team2money, strat1, strat2, first_to=13, max_money=15):
    """
    A function to graph out a comparison of money and points for each team from the given lists.

    Parameters
    ----------
    team1score : list
        A list of the scores over rounds of player 1.
    team2score : list
        A list of the scores over rounds of player 2.
    team1money : list
        A list of the money over rounds of player 1.
    team2money : list
        A list of the money over rounds of player 2.
    strat1 : function
        The strategy function for player 1.
    strat2 : function
        The strategy function for player 2.
    first_to : int or float, optional
        The number of round wins a player needs to win the game, by default 13.
    max_money : int or float, optional
        The maximum amount of money that a player can have at any given round, by default 15.

    Returns
    -------
    None. 
        Displays the graph to compare the points over time and money over time for each team.

    """
    fig, (ax1, ax2) = plt.subplots(2)
    ax_2a = ax1.twinx()
    ax_2b = ax2.twinx()
    ax1.set_title("Team 1: " + strat1.stratname)
    ax2.set_title("Team 2: " + strat2.stratname)
    ax1.set_ylabel("wins")
    ax2.set_xlabel("round")
    ax2.set_ylabel("wins")
    ax_2a.set_ylabel("eco")
    ax_2b.set_ylabel("eco")
    ax1.step(range(0,len(team1score)),team1score, linewidth=5)
    ax2.step(range(0,len(team2score)),team2score, linewidth=5,color="red")
    ax_2a.step(range(0,len(team1score)), team1money, linewidth=2.5,color="green")
    ax_2b.step(range(0,len(team2score)), team2money, linewidth=2.5,color="forestgreen")
    ax1.set(ylim=(0, first_to))
    ax2.set(ylim=(0, first_to))
    ax_2a.set(ylim=(1, max_money))
    ax_2b.set(ylim=(1, max_money))

    plt.show()

def find_possible_strategies(play_to=13, repetitions=10_000, accurate_game=False, n=5):
    """
    A function to use the random strategy repeatedly to find what the possible strategies are in a full normal game.
    
    Parameters
    ----------
    play_to : int or float, optional
        The required number of round wins for a player to win a game, by default 13.
    repetitions : int, optional
        number of games to be tried to find possible strategies, by default 10,000.
    accurate_game : bool, optional
        A boolean deciding whether the game format is accurate game (True) or simply first to some number of wins, by default False.
    n : int, optional
        A chosen value for strategies such as eco_first_n_rounds, by default 5.

    Returns
    -------
    int
        The length of the list of all found strategies.

    """
    strat1 = random_strat
    strat2 = random_strat
    possible_strategies = []
    for i in range(repetitions):
        print(str(100 * i / repetitions) + " percent complete")
        if accurate_game == False:
            current_points_over_time, current_money_over_time = two_player_game(player1_strat=strat1, player2_strat=strat2, max_money=16, 
                                                                                first_to_or_set_number="first to", play_to=play_to, 
                                                                                loss_bonuses=True, n=n)
            if two_player_game.player1choices not in possible_strategies:
                possible_strategies.append(two_player_game.player1choices)
            if two_player_game.player2choices not in possible_strategies:
                possible_strategies.append(two_player_game.player2choices)
        else:
            current_points_over_time, current_money_over_time = accurate_cs_game(strat1=strat1, strat2=strat2, n=n, loss_bonuses=True)
            if accurate_cs_game.player1choices not in possible_strategies:
                possible_strategies.append(accurate_cs_game.player1chocies)
            if accurate_cs_game.player2choices not in possible_strategies:
                possible_strategies.append(accurate_cs_game.player2chocies)
    return len(possible_strategies)

def play_m_games(strat1, strat2, n=5, m=100, play_to=13, accurate_game=False):
    """
    A function to play m full games of two given strategies against each other.

    Parameters
    ----------
    strat1 : function
        The strategy function for player 1.
    strat2 : function
        The strategy function for player 2.
    n : int, optional
        A chosen value for strategies such as eco_first_n_rounds, by default 5.
    m : int, optional
        The number of games played between the strategies, by default 100.
    play_to : int or float, optional
        The required number of round wins for a player to win a game, by default 13.
    accurate_game : bool, optional
        A boolean deciding whether the game format is accurate game (True) or simply first to some number of wins, by default False

    Returns
    -------
    list
        A list of the two players final scores after the m games.

    """
    scores = [0, 0]
    for i in range(0, m):
        if accurate_game == False:
            gamescore = two_player_game(player1_strat=strat1, player2_strat=strat2, n=n, play_to=play_to)[0][-1]
            winner = gamescore.index(max(gamescore))
        else:
            gamescore = accurate_cs_game(strat1=strat1, strat2=strat2, n=n, loss_bonuses=True)[0][-1]
            winner = gamescore.index(max(gamescore))
        scores[winner] += 1
    return scores

def compare_eco_first_n_with_other_strategies_for_different_n(eco_first_n_selection=eco_first_n_rounds, other_strategy=short_term, 
                                                              play_to=13, number_of_games=1_000, accurate_game=False):
    """
    A function to return winrates of eco first n against another strategy for varying values of n, from 0 to the play_to value.

    Parameters
    ----------
    eco_first_n_selection : function, optional
        The chosen strategy which depends on n, such as eco_first_n_rounds_then_lil_then_short_term, by default eco_first_n_rounds.
    other_strategy : function, optional
        The chosen strategy to play against the eco_first_n_selection strategy, by default short_term.
    play_to : int or float, optional
        The required number of round wins for a player to win a game, by default 13.
    number_of_games : int, optional
        The given number of games for the player 1 strategy to play against player 2 strategy, by default 1,000.
    accurate_game : bool, optional
        A boolean deciding whether the game format is accurate game (True) or simply first to some number of wins, by default False
    
    Returns
    -------
    tuple
        A tuple containing two lists; eco_first_n_winrates and other_strategy_winrates.
        eco_first_n_winrates : list
            A list of the win rates for eco_first_n strategy for values of n from 0 to play_to.
        other_strategy_winrates : list
            A list of the win rates for the other strategy for values of n from 0 to play_to.

    """
    eco_first_first_n_winrates = []
    other_strategy_winrates = []
    for n in range(0, play_to):
        eco_first_first_n_wins, other_strategy_wins = play_m_games(strat1=eco_first_n_selection, strat2=other_strategy, n=n, 
                                                                   m=number_of_games, play_to=play_to, accurate_game=accurate_game)
        eco_first_first_n_winrate = eco_first_first_n_wins / number_of_games
        other_strategy_winrate = other_strategy_wins / number_of_games
        eco_first_first_n_winrates.append(eco_first_first_n_winrate)
        other_strategy_winrates.append(other_strategy_winrate)
    return eco_first_first_n_winrates, other_strategy_winrates

def graph_eco_first_n_against_other_strategy(eco_first_n_selection=eco_first_n_rounds, other_strategy=short_term, play_to=13, 
                                             number_of_games=1_000, accurate_game=False):
    """
    A function to show interactions on a graph between eco first n against another strategy depending on the value of n.

    Parameters
    ----------
    eco_first_n_selection : function, optional
        The chosen strategy which depends on n, such as eco_first_n_rounds_then_lil_then_short_term, by default eco_first_n_rounds.
    other_strategy : function, optional
        The chosen strategy to play against the eco_first_n_selection strategy, by default short_term.
    play_to : int or float, optional
        The required number of round wins for a player to win a game, by default 13.
    number_of_games : int, optional
        The given number of games for the player 1 strategy to play against player 2 strategy, by default 1,000.
    accurate_game : bool, optional
        A boolean deciding whether the game format is accurate game (True) or simply first to some number of wins, by default False
    
    
    Returns
    -------
    None.
        Displays the graph comparing win rates for different values of n.

    """
    eco_first_n_winrates = compare_eco_first_n_with_other_strategies_for_different_n(eco_first_n_selection=eco_first_n_selection, 
                                                                                     other_strategy=other_strategy, play_to=play_to, 
                                                                                     number_of_games=number_of_games, 
                                                                                     accurate_game=accurate_game)[0]
    fig, ax = plt.subplots()
    ax.set_title(eco_first_n_selection.stratname + " vs " + other_strategy.stratname)
    ax.set_ylabel("winrate")
    ax.set_xlabel("n")
    ax.set(ylim=(0, 1))
    ax.set(xlim=(0, play_to))
    plt.plot(eco_first_n_winrates, 'r-x')

    plt.show()

def generate_interaction_matrix(strategies, n=5, sample_size=1_000, decimal_places=3, accurate_game=False):
    """
    Given a list of strategies this function plays sample_size number of games of each strategy against each other strategy to generate a 
    matrix which has the win rate of each strategy against each other. 
    
    Parameters
    ----------
    strategies : list
        A list of functions which are the strategies for our interaction matrix.
    n : int, optional
        A chosen value for strategies such as eco_first_n_rounds, by default 5.
    sample_size : int, optional
        A chosen number of games to simulate play to find win rates, by default 1,000.
    decimal_places : int, optional
        The chosen number of decimal places that the interaction matrix will return with, by default 3.
    accurate_game : bool, optional
        A boolean deciding whether the game format is accurate game (True) or simply first to some number of wins, by default False
    
    Returns
    -------
    list
        A list of lists representing our interaction matrix, can be put into a numpy array.

    """
    interaction_matrix = [[0 for i in range(len(strategies))] for j in range(len(strategies))]
    for i in range(0, len(strategies)):
        for j in range(i, len(strategies)):
            print("i: " + strategies[i].__name__, "j: " + strategies[j].__name__)
            if i == j:
                interaction_matrix[i][i] = 0.5
            else:
                results = play_m_games(strat1=strategies[i], strat2=strategies[j], n=n, m=sample_size, accurate_game=accurate_game)
                interaction_matrix[i][j] = round(results[0] * (1 / sample_size), decimal_places)
                interaction_matrix[j][i] = round(results[1] * (1 / sample_size), decimal_places)

    return interaction_matrix
            
def display_interaction_matrix(matrix, strategies):
    """
    A function to print the interaction matrix nicely.

    Parameters
    ----------
    matrix : list
        The given interaction matrix between all strategies we want to look at.
    strategies : list
        The list of all strategies which we have generated the interaction matrix for.
    
    Returns
    -------
    None.
        Prints the interaction matrix with labelled stratnames row by row.

    """
    for i in range(0, len(matrix)):
        print (f"{strategies[i].stratname:30} {matrix[i]}")

def replicator_dynamics(game_matrix, iterations=100, intervals=100):
    """
    Uses nashpy replicator dynamics with the interaction matrix to show which strategies survive over time.

    Parameters
    ----------
    game_matrix : list
        A list of lists representing our matrix with win rates for each strategy against each other strategy.
    iterations : int, optional
        The number of games that we consider looking at the replicator dynamics, by default 100. again ?????????????????????
    intervals : int, optional
        The space between each things???????????????????????????????????????????????????????????????????????????????????????

    Returns
    -------
    array
        The population distribution of all strategies over time.

    """
    timepoints = np.linspace(0, iterations, intervals)
    game = nash.Game(game_matrix)
    replicator_game = game.replicator_dynamics(y0=[1 / 19, 1 / 19, 1 / 19, 1 / 19, 1 / 19, 2 / 19, 2 / 19, 1 / 19, 1 / 19, 2 / 19, 1 / 19, 1 / 19, 2 / 19, 2 / 19, 1 / 19, 1 / 19, 1 / 19, 1 / 19], timepoints=timepoints)
    return replicator_game
    
def replicator_dynamics_graph(outcome_array, strat_names):
    """
    A function to plot the replicator dynamics graph.

    Parameters
    ----------
    outcome_array : array
        The population distribution of all strategies over time.
    strat_names : list
        A list of the strategy names to plot on the graph.
    
    Returns
    -------
    None.
        Displays the graph showing the replicator dynamics of strategies over time.

    """
    x = np.linspace(0, len(outcome_array), len(outcome_array))
    y_vals = outcome_array
    y_vals = list(map(list, zip(*outcome_array)))   #transposes outcome array
    fig, ax = plt.subplots()
    lines=[]
    for line_index in range(0,len(y_vals)):
        lines.append(ax.plot(x, y_vals[line_index], label=strat_names[line_index]))
    ax.legend(loc="upper right")
    ax.set_xlabel("games")
    ax.set_ylabel("population share")
    mplcursors.cursor(fig, hover=True)

    plt.show()
