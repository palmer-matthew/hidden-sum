from random import shuffle, choice

class GameView():
    pass

class Game():
    
    def __init__(self, players, total_rounds):
        self.pot = 0
        self.players = players
        self.total_rounds = total_rounds
        self.current_round = 0
        self.highest_bet = 0

    def shuffle_player_hands(self):
        for player in self.players:
            player.shuffle()

    def deal_player_hands(self):
        for player in self.players:
            player.deal()

    def reload_pot(self):
        self.pot = 0
    
    def add_to_pot(self, player_bet):
        self.pot += player_bet

    def betting_phase(self, initial=False):
        for player in self.players:
            if initial == True:
                player_bet = player.make_bet(action="call", highest_bet=1)
            elif not player.has_folded():
                player_bet = player.make_bet(highest_bet=self.highest_bet)
            self.highest_bet = max(player_bet, self.highest_bet)
            self.add_to_pot(player_bet)

    def reward_round_winner(self, winner_index):
        self.players[winner_index].add_rewards()

    def find_game_winner(self):
        winner_index = 0
        highest = 0
        for index, player in enumerate(self.players):
            player_chips = player.get_chips()
            if player_chips >= highest:
                winner_index = index
                highest = player_chips
        return winner_index

    def start(self):
        while self.is_game_over():
            self.play_round()
        self.end()

    def end(self):
        winner = self.players[self.find_game_winner()]
        return winner

    def is_game_over(self):
        return [not player.has_chips for player in self.players] or self.current_round >= self.total_rounds

    def play_round(self):

        self.current_round += 1

        self.betting_phase(initial=True)

        self.shuffle_player_hands()
        self.deal_player_hands()

        self.reload_pot()
        self.betting_phase()

        winner = self.showdown()
        self.reward_round_winner(winner)

    def showdown(self):
        # TODO: The function doesn't account for cases where they are ties for the highest sum
        highest_total = 0
        index_of_winner = 0
        for index, player in enumerate(self.players):
            if not player.has_folded():
                total = player.get_hand_sum()
                if total > highest_total:
                    highest_total = total
                    index_of_winner = index
        return index_of_winner

        
class Player():

    def __init__(self, username):
        self.username = username
        self.deck = PlayerDeck()
        self.chips = 20
        self.blind = 0
        self.folded = False

    def has_chips(self):
        return self.chips > 0
    
    def get_chips(self):
        return self.chips
    
    def get_hand(self, player_view=True):
        if player_view:
            return { "public": "?" , "hidden": self.deck.get_hidden_card() }
        return { "public": self.deck.get_public_card() , "hidden": "?"}
    
    def shuffle(self):
        self.deck.shuffle_hidden_cards()
        self.deck.shuffle_public_cards()

    def deal(self):
        self.deck.choose_hand()
    
    def make_bet(self, action=None, **kwargs):
        actions = ['fold', 'call', 'raise']

        if action is None:
            action = choice(actions)
        
        if action == 'fold':
            return self.fold()
        elif action == 'call':
            return self.call(kwargs["highest_bet"])
        elif action == 'raise':
            return self.raise_bet(choice(range(1,3)))
    
    def bet_made(self, bet):
        self.chips -= bet
        self.blind += bet
    
    def call(self, highest_bet):
        if highest_bet is None:
            return 0
        elif self.has_chips and highest_bet > self.chips:
            return 0
        self.bet_made(highest_bet)
        return highest_bet
        

    def fold(self):
        self.folded = True
        return 0

    def raise_bet(self, raised_bet):
        if raised_bet is None:
            return 0
        elif self.has_chips and raised_bet > self.chips:
            return 0
        self.bet_made(raised_bet)
        return raised_bet
    
    def has_folded(self):
        return self.folded
    
    def get_hand_sum(self):
        return self.deck.get_hidden_card + self.deck.get_public_card
    
    def add_rewards(self, round_rewards):
        self.chips += round_rewards
        


class PlayerDeck():
    def __init__(self):
        self.hidden_cards = [i for i in range(1, 11)]
        self.public_cards = [i for i in range(1, 11)]
        self.hidden_card_chosen = -1
        self.public_card_chosen = -1

    def shuffle_hidden_cards(self):
        shuffle(self.hidden_cards)
    
    def shuffle_public_cards(self):
        shuffle(self.public_cards)

    def reset_hand(self):
        self.hidden_card_chosen = -1
        self.public_card_chosen = -1
        # self.shuffle_hidden_cards()
        # self.shuffle_public_cards()
    
    def choose_hand(self):
        self.hidden_card_chosen = choice(self.hidden_card_chosen)
        self.public_card_chosen = choice(self.public_card_chosen)

    def get_public_card(self):
        return self.public_card_chosen
    
    def get_hidden_card(self):
        return self.hidden_card_chosen
    

if __name__ == "__main__":
    pass