import streamlit as st
import random
import time

# --- Game Logic Classes ---
class Board:
    def __init__(self):
        self.cells = [str(i+1) for i in range(9)]

    def reset(self):
        self.cells = [str(i+1) for i in range(9)]

    def make_move(self, pos, mark):
        if self.cells[pos-1] not in ['X', 'O']:
            self.cells[pos-1] = mark
            return True
        return False

    def is_full(self):
        return all(cell in ['X', 'O'] for cell in self.cells)

    def display(self):
        board_display = ""
        for i in range(9):
            cell = self.cells[i]
            board_display += f" {cell} "
            if i % 3 != 2:
                board_display += "|"
            if i % 3 == 2 and i != 8:
                board_display += "\n-----------\n"
        return board_display

    def check_win(self, mark):
        b = self.cells
        wins = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        return any(b[i]==b[j]==b[k]==mark for i,j,k in wins)

    def empty_cells(self):
        return [i+1 for i, cell in enumerate(self.cells) if cell not in ['X', 'O']]

# --- Player Logic ---
class Player:
    def __init__(self, mark):
        self.mark = mark

    def get_move(self, board):
        pass

class HumanPlayer(Player):
    def get_move(self, board):
        return None  # Human selects via UI

class RandomComputer(Player):
    def get_move(self, board):
        return random.choice(board.empty_cells())

class SmartComputer(Player):
    def get_move(self, board):
        for move in board.empty_cells():
            board.cells[move-1] = self.mark
            if board.check_win(self.mark):
                board.cells[move-1] = str(move)  # Reset
                return move
            board.cells[move-1] = str(move)
        
        opponent = 'O' if self.mark == 'X' else 'X'
        for move in board.empty_cells():
            board.cells[move-1] = opponent
            if board.check_win(opponent):
                board.cells[move-1] = str(move)
                return move
            board.cells[move-1] = str(move)
        
        if 5 in board.empty_cells():
            return 5
        for corner in [1, 3, 7, 9]:
            if corner in board.empty_cells():
                return corner
        for edge in [2, 4, 6, 8]:
            if edge in board.empty_cells():
                return edge
        return random.choice(board.empty_cells())

# --- Streamlit UI & Game Flow ---
st.set_page_config("Tic Tac Toe")
st.title("🎮 Tic-Tac-Toe with AI Modes")

if "board" not in st.session_state:
    st.session_state.board = Board()
    st.session_state.player1 = None
    st.session_state.player2 = None
    st.session_state.current_player = None
    st.session_state.message = ""
    st.session_state.mark_map = {}
    st.session_state.human_turn = True

def setup_game(mode, mark):
    b = Board()
    st.session_state.board = b
    mark1 = mark.upper()
    mark2 = 'O' if mark1 == 'X' else 'X'
    st.session_state.mark_map = {"Player 1": mark1, "Player 2": mark2}

    if mode == "Human vs Human":
        p1 = HumanPlayer(mark1)
        p2 = HumanPlayer(mark2)
    elif mode == "Human vs Random Computer":
        p1 = HumanPlayer(mark1)
        p2 = RandomComputer(mark2)
    elif mode == "Human vs Smart Computer":
        p1 = HumanPlayer(mark1)
        p2 = SmartComputer(mark2)
    elif mode == "Random Computer vs Smart Computer":
        p1 = RandomComputer(mark1)
        p2 = SmartComputer(mark2)
    
    st.session_state.player1 = p1
    st.session_state.player2 = p2
    st.session_state.current_player = p1
    st.session_state.message = ""
    st.session_state.human_turn = isinstance(p1, HumanPlayer)

st.sidebar.header("Game Settings")
game_mode = st.sidebar.selectbox("Choose Game Mode", [
    "Human vs Human", "Human vs Random Computer", "Human vs Smart Computer", "Random Computer vs Smart Computer"
])
player1_mark = st.sidebar.radio("Player 1 Mark", ["X", "O"])
if st.sidebar.button("Start New Game"):
    setup_game(game_mode, player1_mark)

# --- Display Game Board ---
st.subheader("Game Board")
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        cell = st.session_state.board.cells[i]
        if cell not in ['X', 'O']:
            if st.session_state.human_turn and isinstance(st.session_state.current_player, HumanPlayer):
                if st.button(f"{cell}", key=f"btn{i}"):
                    move = int(cell)
                    if st.session_state.board.make_move(move, st.session_state.current_player.mark):
                        st.session_state.human_turn = False
        else:
            st.markdown(f"### {cell}")

# --- Game Logic Flow ---
def next_turn():
    b = st.session_state.board
    cp = st.session_state.current_player
    if not isinstance(cp, HumanPlayer):
        time.sleep(0.5)
        move = cp.get_move(b)
        b.make_move(move, cp.mark)
        st.session_state.human_turn = True

    if b.check_win(cp.mark):
        st.session_state.message = f"🏆 Player with mark '{cp.mark}' wins!"
        st.session_state.human_turn = False
    elif b.is_full():
        st.session_state.message = "🤝 It's a draw!"
        st.session_state.human_turn = False
    else:
        st.session_state.current_player = (
            st.session_state.player2 if cp == st.session_state.player1 else st.session_state.player1
        )
        st.session_state.human_turn = isinstance(st.session_state.current_player, HumanPlayer)

if not st.session_state.message:
    if not st.session_state.human_turn:
        next_turn()

# --- Game Status ---
st.subheader("Game Status")
st.markdown(st.session_state.board.display())
if st.session_state.message:
    st.success(st.session_state.message)

if st.button("🔄 Restart Game"):
    setup_game(game_mode, player1_mark)
