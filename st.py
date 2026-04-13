import streamlit as st
import numpy as np
from npc import players, minimax, terminal_util

st.set_page_config(page_title="PvE Tic-Tac-Toe", page_icon="⚡")

st.markdown(
    """
    <style>
        /* Schriften importieren, um unser Design von der Website zu matchen */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Outfit:wght@500;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }
        
        .game-button button {
            font-size: 50px !important;
            width: 100px !important;
            height: 100px !important;
            margin: 5px !important;
            padding: 0px !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            background-color: rgba(30, 31, 35, 0.6) !important;
            transition: all 0.3s ease !important;
        }
        .game-button button:hover {
            border-color: rgba(255, 140, 120, 0.5) !important;
            background-color: rgba(45, 47, 53, 0.8) !important;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }
        
        .backlink {
            text-decoration: none;
            color: #ff8c78;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 2rem;
            transition: color 0.3s;
        }
        .backlink:hover {
            color: #ffad82;
            text-decoration: underline;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<a href="https://qwertzlich.github.io/mywebsite" target="_self" class="backlink">⬅️ Zurück zu meiner Website</a>', unsafe_allow_html=True)

st.title('Welcome to PvE Tic-Tac-Toe!')

st.write('This is a simple game of Tic-Tac-Toe where you play against an self written AI. The AI uses the minimax algorithm to determine the best move to make. You are player 1 and the AI is player 2. You go first!')

if 'board' not in st.session_state:
    board = np.zeros((3, 3), dtype = np.int32)
    st.session_state['board'] = board
if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False

if st.button('(Re)-Start Game', key = 'restart'):
    board = np.zeros((3, 3), dtype = np.int32)
    st.session_state['board'] = board
    st.session_state['game_over'] = False

terminal, utility = terminal_util(st.session_state['board'])
if terminal:
    if utility == 1:
        st.header('Congratulations! You won!')
    elif utility == -1:
        st.header('You lost! Better luck next time!')
    else:
        st.header('It\'s a draw!')

cols = st.columns(3)

for col in range(3):
    with cols[col]:
        for row in range(3):
            st.markdown('<div class="game-button">', unsafe_allow_html=True)
            if st.session_state['board'][row, col] == 1:
                st.button('X', key = f'button_{row}{col}', disabled=True, use_container_width=True)
            elif st.session_state['board'][row, col] == -1:
                st.button('O', key = f'button_{row}{col}', disabled=True, use_container_width=True)
            else:
                if st.button('', key = f'button_{row}{col}', use_container_width=True):
                    st.session_state['board'][row, col] = players(st.session_state['board'])
                    if not np.count_nonzero(st.session_state['board']) == 9:
                        r, c = minimax(st.session_state['board'])
                        st.session_state['board'][r, c] = players(st.session_state['board'])
                        st.rerun()
                    else:
                        st.session_state['game_over'] = True
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

if st.session_state['game_over']:
    st.write('The Game is over! Press the button above to restart the game.')

