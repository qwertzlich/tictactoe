import streamlit as st
import numpy as np
from npc import players, minimax, terminal_util

st.set_page_config(page_title="PvE Tic-Tac-Toe", page_icon="⚡")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Outfit:wght@500;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }
        
        /* -------------------------------------------------------------
           GRID BUTTONS (TicTacToe Boxes, kind="secondary")
           ------------------------------------------------------------- */
        div[data-testid="stButton"]:has(button[kind="secondary"]),
        button[kind="secondary"] {
            height: 70px !important;
            min-height: 70px !important;
            max-height: 70px !important;
            box-sizing: border-box !important;
            margin: 0 !important;
        }
        button[kind="secondary"] {
            font-size: 35px !important;
            line-height: 1 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border-radius: 16px !important;
            border: none !important;
            transition: all 0.3s ease !important;
            padding: 0 !important;
        }

        /* Status: UNCLICKED (Orange Gradient, Dummy-X invisible) */
        button[kind="secondary"]:not(:disabled) {
            background: linear-gradient(135deg, #ff8c78 0%, #ffad82 100%) !important;
            box-shadow: 0 4px 10px rgba(255, 140, 120, 0.2);
        }
        button[kind="secondary"]:not(:disabled),
        button[kind="secondary"]:not(:disabled) * {
            color: transparent !important;
        }
        button[kind="secondary"]:not(:disabled):hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(255, 140, 120, 0.4) !important;
        }

        /* Status: CLICKED (Dark Background, white Text for X/O) */
        button[kind="secondary"]:disabled {
            background: rgba(30, 31, 35, 0.6) !important;
            border: 2px solid rgba(255, 255, 255, 0.06) !important;
        }
        button[kind="secondary"]:disabled,
        button[kind="secondary"]:disabled * {
            color: #fcfcfc !important;
            opacity: 1 !important; 
        }

        /* -------------------------------------------------------------
           RESTART BUTTON (kind="primary")
           ------------------------------------------------------------- */
        button[kind="primary"] {
            background: linear-gradient(135deg, #ff8c78 0%, #ffad82 100%) !important;
            color: #111 !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            transition: all 0.3s ease !important;
            padding: 0.8rem 1.6rem !important;
        }
        button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(255, 140, 120, 0.4) !important;
            color: #111 !important;
        }
        button[kind="primary"] * {
            color: #111 !important;
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

if st.button('(Re)-Start Game', key='restart', type='primary', use_container_width=True):
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
            if st.session_state['board'][row, col] == 1:
                st.button('X', key = f'button_{row}{col}', disabled=True, use_container_width=True)
            elif st.session_state['board'][row, col] == -1:
                st.button('O', key = f'button_{row}{col}', disabled=True, use_container_width=True)
            else:
                if st.button('X\u200b', key = f'button_{row}{col}', use_container_width=True):
                    st.session_state['board'][row, col] = players(st.session_state['board'])
                    if not np.count_nonzero(st.session_state['board']) == 9:
                        r, c = minimax(st.session_state['board'])
                        st.session_state['board'][r, c] = players(st.session_state['board'])
                        st.rerun()
                    else:
                        st.session_state['game_over'] = True
                        st.rerun()

if st.session_state['game_over']:
    st.write('The Game is over! Press the button above to restart the game.')

