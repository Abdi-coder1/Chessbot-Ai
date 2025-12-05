
class Maneuver:
    """
    This Maneuver class represent a choice that a plyer or Ai can make on the board,
    That entails both moving and executing special rules like enpassant and castling.
    It is a pure data structure that gets updated by players, and is used by the
    chess_engine tp update both the Board and pieces.
    """
    def __init__(self):
        """
        Since the Maneuver object represent a move, it should contain,
        all the possible things that could happen during a move,
        Except for check_mate,
        """
        self.human_type = ['empty', 'selected', 'moved']  # Differentiation  for Human players
        self.state = {
            'color': None,                               # black or white?  type = str
            'piece': None,                               # what piece object have been moved?, contains an actual object
            'start_pos': ['y', 'x'],                     # list of starting condition for that piece, [int,int]
            'end_pos': ['y', 'x'],                       # list of ending condition for that piece, [int,int]
            'castling': {'bool': False, 'side': None, 'color': None},  # was a castling perform, if so, of what kind? str!
            'capture': {'bool': False,                                 # was a capture performed? contains a piece!
                        'piece': None},
            'updated': False,                                         # has it been changed?
             'human_type': self.human_type[0]                         # What state is the maneuver in by humans ? str
        }
