from PicoGameBoy import PicoGameBoy
from time import sleep, time
import random
import json

class ChessGame:
    def __init__(self):
        self.pgb = PicoGameBoy()
        
        # Colors
        self.WHITE = PicoGameBoy.color(255, 255, 255)
        self.BLACK = PicoGameBoy.color(0, 0, 0)
        self.DARK_SQUARE = PicoGameBoy.color(139, 69, 19)
        self.LIGHT_SQUARE = PicoGameBoy.color(255, 228, 181)
        self.HIGHLIGHT = PicoGameBoy.color(255, 255, 0)
        self.SELECT = PicoGameBoy.color(0, 255, 0)
        self.RED = PicoGameBoy.color(255, 0, 0)
        self.BLUE = PicoGameBoy.color(0, 0, 255)
        
        # Game states
        self.MENU = 0
        self.PLAYING = 1
        self.GAME_OVER = 2
        self.SETTINGS = 3
        self.game_state = self.MENU
        
        # Menu options
        self.menu_options = ['Play vs Human', 'Play vs AI', 'Load Game', 'Settings']
        self.menu_selection = 0
        
        # Board setup
        self.SQUARE_SIZE = 30
        self.PIECE_SIZE = 24
        self.board = self.initial_board()
        
        # Game state
        self.selected_piece = None
        self.current_player = 'white'
        self.cursor_x = 0
        self.cursor_y = 0
        self.valid_moves = []
        self.move_history = []
        self.check_status = False
        self.game_mode = 'human'
        self.castling_rights = {
            'white': {'kingside': True, 'queenside': True},
            'black': {'kingside': True, 'queenside': True}
        }
        self.en_passant_target = None
        
        # Timers
        self.white_time = 600
        self.black_time = 600
        self.last_move_time = time()
        
        # AI settings
        self.ai_difficulty = 2
        self.ai_thinking = False
        
        # Animation
        self.animation_frames = []
        self.animation_speed = 5
        
        # Sound settings
        self.sound_enabled = True
        
        # Create piece sprites
        self.create_piece_sprites()
        
    def initial_board(self):
        return [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]

    def create_piece_sprites(self):
        # Detailed piece designs (8x8 pixel art)
        piece_designs = {
            'K': [ # King
                [0,0,1,0,0,1,0,0],
                [0,0,1,1,1,1,0,0],
                [0,0,0,1,1,0,0,0],
                [0,1,1,1,1,1,1,0],
                [0,1,1,1,1,1,1,0],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1]
            ],
            'Q': [ # Queen
                [0,1,0,1,1,0,1,0],
                [1,0,1,0,0,1,0,1],
                [1,0,1,1,1,1,0,1],
                [0,1,1,1,1,1,1,0],
                [0,1,1,1,1,1,1,0],
                [0,1,1,1,1,1,1,0],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1]
            ],
            'R': [ # Rook
                [1,0,1,1,1,1,0,1],
                [1,1,1,1,1,1,1,1],
                [0,1,1,1,1,1,1,0],
                [0,1,1,1,1,1,1,0],
                [0,1,1,1,1,1,1,0],
                [0,1,1,1,1,1,1,0],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1]
            ],
            'B': [ # Bishop
                [0,0,0,1,1,0,0,0],
                [0,0,1,1,1,1,0,0],
                [0,0,1,1,1,1,0,0],
                [0,1,1,1,1,1,1,0],
                [0,0,1,1,1,1,0,0],
                [0,1,1,1,1,1,1,0],
                [0,1,1,1,1,1,1,0],
                [1,1,1,1,1,1,1,1]
            ],
            'N': [ # Knight
                [0,0,1,1,1,1,0,0],
                [0,1,1,1,1,1,1,0],
                [1,1,0,1,1,1,1,0],
                [1,0,0,1,1,1,1,0],
                [0,0,0,1,1,1,0,0],
                [0,0,1,1,1,1,0,0],
                [0,1,1,1,1,1,1,0],
                [1,1,1,1,1,1,1,1]
            ],
            'P': [ # Pawn
                [0,0,0,0,0,0,0,0],
                [0,0,0,1,1,0,0,0],
                [0,0,1,1,1,1,0,0],
                [0,0,0,1,1,0,0,0],
                [0,0,1,1,1,1,0,0],
                [0,0,1,1,1,1,0,0],
                [0,1,1,1,1,1,1,0],
                [1,1,1,1,1,1,1,1]
            ]
        }

        # Create sprites for both colors
        sprite_index = 0
        for piece_type in 'KQRBNP':
            # White pieces
            sprite = self.create_piece_sprite(piece_designs[piece_type], True)
            self.pgb.add_sprite(sprite, self.PIECE_SIZE, self.PIECE_SIZE)
            sprite_index += 1
            
            # Black pieces
            sprite = self.create_piece_sprite(piece_designs[piece_type], False)
            self.pgb.add_sprite(sprite, self.PIECE_SIZE, self.PIECE_SIZE)
            sprite_index += 1
    def create_piece_sprite(self, design, is_white):
        sprite = bytearray(self.PIECE_SIZE * self.PIECE_SIZE * 2)
        scale = self.PIECE_SIZE // 8
        piece_color = self.WHITE if is_white else self.BLACK
        
        # Fill sprite with transparent/empty color first
        for y in range(self.PIECE_SIZE):
            for x in range(self.PIECE_SIZE):
                pos = (y * self.PIECE_SIZE + x) * 2
                sprite[pos] = 0
                sprite[pos + 1] = 0
        
        # Draw piece with outline for black pieces
        for y in range(8):
            for x in range(8):
                if design[y][x]:
                    # For black pieces, add a white outline
                    if not is_white:
                        # Draw outline
                        for sy in range(max(0, y*scale-1), min(self.PIECE_SIZE, (y+1)*scale+1)):
                            for sx in range(max(0, x*scale-1), min(self.PIECE_SIZE, (x+1)*scale+1)):
                                pos = (sy * self.PIECE_SIZE + sx) * 2
                                sprite[pos] = self.WHITE & 0xFF
                                sprite[pos + 1] = (self.WHITE >> 8) & 0xFF
                    
                    # Draw main piece
                    for sy in range(y*scale, min(self.PIECE_SIZE, (y+1)*scale)):
                        for sx in range(x*scale, min(self.PIECE_SIZE, (x+1)*scale)):
                            pos = (sy * self.PIECE_SIZE + sx) * 2
                            sprite[pos] = piece_color & 0xFF
                            sprite[pos + 1] = (piece_color >> 8) & 0xFF
        
        return sprite
    
    def draw_menu(self):
        self.pgb.fill(self.BLACK)
        
        # Draw title
        self.pgb.center_text("CHESS", self.WHITE)
        
        # Draw menu options
        y_start = 80
        for i, option in enumerate(self.menu_options):
            color = self.HIGHLIGHT if i == self.menu_selection else self.WHITE
            self.pgb.text(option, 60, y_start + i * 20, color)
        
        # Draw instructions
        self.pgb.text("A: Select  B: Back", 60, 200, self.WHITE)
        
        self.pgb.show()

    def handle_menu(self):
        if self.pgb.button_up() and self.menu_selection > 0:
            self.menu_selection -= 1
            sleep(0.2)
        if self.pgb.button_down() and self.menu_selection < len(self.menu_options) - 1:
            self.menu_selection += 1
            sleep(0.2)
        
        if self.pgb.button_A():
            if self.menu_selection == 0:  # Play vs Human
                self.game_mode = 'human'
                self.game_state = self.PLAYING
            elif self.menu_selection == 1:  # Play vs AI
                self.game_mode = 'ai'
                self.game_state = self.PLAYING
            elif self.menu_selection == 2:  # Load Game
                if self.load_game():
                    self.game_state = self.PLAYING
            elif self.menu_selection == 3:  # Settings
                self.game_state = self.SETTINGS
            sleep(0.2)

    def draw_piece(self, piece, x, y):
        if piece == '  ':
            return
            
        # Get piece index
        piece_type = piece[1]
        is_white = piece[0] == 'w'
        
        # Map piece types to sprite indices
        type_to_index = {'K': 0, 'Q': 2, 'R': 4, 'B': 6, 'N': 8, 'P': 10}
        sprite_index = type_to_index[piece_type]
        if not is_white:
            sprite_index += 1
        
        # Calculate position
        pos_x = x * self.SQUARE_SIZE + (self.SQUARE_SIZE - self.PIECE_SIZE) // 2
        pos_y = y * self.SQUARE_SIZE + (self.SQUARE_SIZE - self.PIECE_SIZE) // 2
        
        # Draw sprite
        self.pgb.sprite(sprite_index, pos_x, pos_y)


    def get_piece_moves(self, x, y, check_check=True):
        piece = self.board[y][x]
        if piece == '  ':
            return []
            
        color = piece[0]
        piece_type = piece[1]
        moves = []
        
        # Pawn moves
        if piece_type == 'P':
            direction = -1 if color == 'w' else 1
            
            # Forward move
            if 0 <= y + direction < 8 and self.board[y + direction][x] == '  ':
                moves.append((x, y + direction))
                # Initial two-square move
                if ((color == 'w' and y == 6) or (color == 'b' and y == 1)) and \
                   self.board[y + 2*direction][x] == '  ':
                    moves.append((x, y + 2*direction))
            
            # Captures
            for dx in [-1, 1]:
                new_x = x + dx
                new_y = y + direction
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    # Normal capture
                    if self.board[new_y][new_x] != '  ' and \
                       self.board[new_y][new_x][0] != color:
                        moves.append((new_x, new_y))
                    # En passant
                    elif (new_x, new_y) == self.en_passant_target:
                        moves.append((new_x, new_y))
        
        # Knight moves
        elif piece_type == 'N':
            knight_moves = [(-2,-1), (-2,1), (-1,-2), (-1,2),
                          (1,-2), (1,2), (2,-1), (2,1)]
            for dx, dy in knight_moves:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if self.board[new_y][new_x] == '  ' or \
                       self.board[new_y][new_x][0] != color:
                        moves.append((new_x, new_y))
        
        # Bishop, Rook, and Queen moves
        elif piece_type in 'BRQ':
            directions = []
            if piece_type in 'BQ':  # Diagonal moves
                directions += [(-1,-1), (-1,1), (1,-1), (1,1)]
            if piece_type in 'RQ':  # Straight moves
                directions += [(-1,0), (1,0), (0,-1), (0,1)]
                
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                while 0 <= new_x < 8 and 0 <= new_y < 8:
                    if self.board[new_y][new_x] == '  ':
                        moves.append((new_x, new_y))
                    elif self.board[new_y][new_x][0] != color:
                        moves.append((new_x, new_y))
                        break
                    else:
                        break
                    new_x += dx
                    new_y += dy
        
        # King moves
        elif piece_type == 'K':
            # Normal moves
            king_moves = [(-1,-1), (-1,0), (-1,1), (0,-1),
                         (0,1), (1,-1), (1,0), (1,1)]
            for dx, dy in king_moves:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if self.board[new_y][new_x] == '  ' or \
                       self.board[new_y][new_x][0] != color:
                        moves.append((new_x, new_y))
            
            # Castling
            if check_check and not self.is_in_check(color):
                if self.castling_rights[color]['kingside']:
                    if self.board[y][5] == '  ' and self.board[y][6] == '  ':
                        if not self.is_square_attacked(5, y, color) and \
                           not self.is_square_attacked(6, y, color):
                            moves.append((6, y))
                
                if self.castling_rights[color]['queenside']:
                    if self.board[y][3] == '  ' and \
                       self.board[y][2] == '  ' and \
                       self.board[y][1] == '  ':
                        if not self.is_square_attacked(3, y, color) and \
                           not self.is_square_attacked(2, y, color):
                            moves.append((2, y))
        
        # Filter moves that would leave king in check
        if check_check:
            legal_moves = []
            for move in moves:
                if not self.would_be_in_check(x, y, move[0], move[1], color):
                    legal_moves.append(move)
            moves = legal_moves
            
        return moves

    def is_in_check(self, color):
        # Find king
        king_pos = None
        for y in range(8):
            for x in range(8):
                if self.board[y][x] == color + 'K':
                    king_pos = (x, y)
                    break
            if king_pos:
                break
        
        return self.is_square_attacked(king_pos[0], king_pos[1], color)

    def is_square_attacked(self, x, y, defending_color):
        for y1 in range(8):
            for x1 in range(8):
                piece = self.board[y1][x1]
                if piece != '  ' and piece[0] != defending_color:
                    moves = self.get_piece_moves(x1, y1, check_check=False)
                    if (x, y) in moves:
                        return True
        return False

    def would_be_in_check(self, from_x, from_y, to_x, to_y, color):
        # Make temporary move
        temp_piece = self.board[to_y][to_x]
        self.board[to_y][to_x] = self.board[from_y][from_x]
        self.board[from_y][from_x] = '  '
        
        # Check if king is in check
        in_check = self.is_in_check(color)
        
        # Undo move
        self.board[from_y][from_x] = self.board[to_y][to_x]
        self.board[to_y][to_x] = temp_piece
        
        return in_check

    def make_move(self, from_pos, to_pos):
        fx, fy = from_pos
        tx, ty = to_pos
        moving_piece = self.board[fy][fx]
        
        # Store move in history
        captured_piece = self.board[ty][tx]
        move_record = {
            'piece': moving_piece,
            'from': from_pos,
            'to': to_pos,
            'captured': captured_piece,
            'castling': None,
            'en_passant': None,
            'promotion': None
        }
        
        # Handle castling
        if moving_piece[1] == 'K' and abs(tx - fx) == 2:
            if tx > fx:  # Kingside
                self.board[ty][5] = self.board[ty][7]
                self.board[ty][7] = '  '
                move_record['castling'] = 'kingside'
            else:  # Queenside
                self.board[ty][3] = self.board[ty][0]
                self.board[ty][0] = '  '
                move_record['castling'] = 'queenside'
        
        # Handle en passant capture
        if moving_piece[1] == 'P' and (tx, ty) == self.en_passant_target:
            self.board[fy][tx] = '  '
            move_record['en_passant'] = True
        
        # Make the move
        self.board[ty][tx] = moving_piece
        self.board[fy][fx] = '  '
        
        # Handle pawn promotion
        if moving_piece[1] == 'P' and (ty == 0 or ty == 7):
            self.board[ty][tx] = moving_piece[0] + 'Q'  # Auto-promote to queen
            move_record['promotion'] = 'Q'
        
        # Update castling rights
        if moving_piece[1] == 'K':
            self.castling_rights[self.current_player]['kingside'] = False
            self.castling_rights[self.current_player]['queenside'] = False
        elif moving_piece[1] == 'R':
            if fx == 0:  # Queenside rook
                self.castling_rights[self.current_player]['queenside'] = False
            elif fx == 7:  # Kingside rook
                self.castling_rights[self.current_player]['kingside'] = False
        
        # Set en passant target
        if moving_piece[1] == 'P' and abs(ty - fy) == 2:
            self.en_passant_target = (tx, (ty + fy) // 2)
        else:
            self.en_passant_target = None
        
        # Add move to history
        self.move_history.append(move_record)
        
        # Play move sound
        if self.sound_enabled:
            if captured_piece != '  ':
                self.pgb.sound(880, 100)  # Higher pitch for captures
            else:
                self.pgb.sound(440, 100)  # Normal move sound
            sleep(0.1)
            self.pgb.sound(0)
        
        # Switch players
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        # Update timer
        current_time = time()
        if self.current_player == 'white':
            self.black_time -= current_time - self.last_move_time
        else:
            self.white_time -= current_time - self.last_move_time
        self.last_move_time = current_time

    def ai_make_move(self):
        self.ai_thinking = True
        best_move = None
        best_score = float('-inf')
        
        # Get all possible moves for AI
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece != '  ' and piece[0] == 'b':  # AI plays black
                    moves = self.get_piece_moves(x, y)
                    for move in moves:
                        score = self.evaluate_move(x, y, move[0], move[1], self.ai_difficulty)
                        if score > best_score:
                            best_score = score
                            best_move = ((x, y), move)
        
        if best_move:
            self.make_move(best_move[0], best_move[1])
        
        self.ai_thinking = False

    def evaluate_move(self, from_x, from_y, to_x, to_y, depth):
        if depth == 0:
            return self.evaluate_position()
        
        # Make temporary move
        temp_piece = self.board[to_y][to_x]
        self.board[to_y][to_x] = self.board[from_y][from_x]
        self.board[from_y][from_x] = '  '
        
        # Recursive evaluation
        best_score = float('-inf') if depth % 2 == 0 else float('inf')
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece != '  ':
                    if (depth % 2 == 0 and piece[0] == 'w') or \
                       (depth % 2 == 1 and piece[0] == 'b'):
                        moves = self.get_piece_moves(x, y)
                        for move in moves:
                            score = self.evaluate_move(x, y, move[0], move[1], depth - 1)
                            if depth % 2 == 0:
                                best_score = max(best_score, score)
                            else:
                                best_score = min(best_score, score)
        
        # Undo move
        self.board[from_y][from_x] = self.board[to_y][to_x]
        self.board[to_y][to_x] = temp_piece
        
        return best_score

    def evaluate_position(self):
        piece_values = {
            'P': 1,
            'N': 3,
            'B': 3,
            'R': 5,
            'Q': 9,
            'K': 0  # King's value not counted in material
        }
        
        score = 0
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece != '  ':
                    value = piece_values[piece[1]]
                    if piece[0] == 'w':
                        score -= value
                    else:
                        score += value
                        
                    # Position bonuses
                    if piece[1] == 'P':  # Pawns
                        if piece[0] == 'b':
                            score += (7 - y) * 0.1  # Advance black pawns
                        else:
                            score -= y * 0.1  # Advance white pawns
                    
                    if piece[1] in 'NB':  # Knights and Bishops
                        if piece[0] == 'b':
                            score += 0.1 if y < 6 else 0  # Develop pieces
                        else:
                            score -= 0.1 if y > 1 else 0
        
        return score

    def draw_board(self):
        # Draw squares
        for y in range(8):
            for x in range(8):
                color = self.LIGHT_SQUARE if (x + y) % 2 == 0 else self.DARK_SQUARE
                self.pgb.fill_rect(
                    x * self.SQUARE_SIZE,
                    y * self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                    color
                )
        
        # Draw pieces
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece != '  ':
                    self.draw_piece(piece, x, y)
        
        # Draw selection and valid moves
        if self.selected_piece:
            x, y = self.selected_piece
            self.pgb.rect(
                x * self.SQUARE_SIZE,
                y * self.SQUARE_SIZE,
                self.SQUARE_SIZE,
                self.SQUARE_SIZE,
                self.SELECT
            )
            
            for move in self.valid_moves:
                self.pgb.rect(
                    move[0] * self.SQUARE_SIZE,
                    move[1] * self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                    self.HIGHLIGHT
                )
        
        # Draw cursor
        self.pgb.rect(
            self.cursor_x * self.SQUARE_SIZE,
            self.cursor_y * self.SQUARE_SIZE,
            self.SQUARE_SIZE,
            self.SQUARE_SIZE,
            self.RED
        )
        
        # Draw timer and status
        self.draw_status()
        
        self.pgb.show()

    def draw_status(self):
        # Draw timers
        w_min = int(self.white_time // 60)
        w_sec = int(self.white_time % 60)
        b_min = int(self.black_time // 60)
        b_sec = int(self.black_time % 60)
        
        self.pgb.text(f"White: {w_min:02d}:{w_sec:02d}", 5, 5, self.WHITE)
        self.pgb.text(f"Black: {b_min:02d}:{b_sec:02d}", 5, 15, self.WHITE)
        
        # Draw current player
        color = self.WHITE if self.current_player == 'white' else self.BLACK
        self.pgb.text(f"Turn: {self.current_player}", 5, 25, color)
        
        # Draw check status
        if self.check_status:
            self.pgb.text("CHECK!", 5, 35, self.RED)
        
        # Draw AI thinking status
        if self.ai_thinking:
            self.pgb.text("AI thinking...", 5, 45, self.BLUE)

    def save_game(self):
        game_state = {
            'board': self.board,
            'current_player': self.current_player,
            'castling_rights': self.castling_rights,
            'en_passant_target': self.en_passant_target,
            'white_time': self.white_time,
            'black_time': self.black_time,
            'move_history': self.move_history
        }
        
        try:
            with open('chess_save.json', 'w') as f:
                json.dump(game_state, f)
            return True
        except:
            return False

    def load_game(self):
        try:
            with open('chess_save.json', 'r') as f:
                game_state = json.load(f)
                
            self.board = game_state['board']
            self.current_player = game_state['current_player']
            self.castling_rights = game_state['castling_rights']
            self.en_passant_target = game_state['en_passant_target']
            self.white_time = game_state['white_time']
            self.black_time = game_state['black_time']
            self.move_history = game_state['move_history']
            return True
        except:
            return False

    def handle_input(self):
        if self.pgb.button_left() and self.cursor_x > 0:
            self.cursor_x -= 1
            sleep(0.15)
        if self.pgb.button_right() and self.cursor_x < 7:
            self.cursor_x += 1
            sleep(0.15)
        if self.pgb.button_up() and self.cursor_y > 0:
            self.cursor_y -= 1
            sleep(0.15)
        if self.pgb.button_down() and self.cursor_y < 7:
            self.cursor_y += 1
            sleep(0.15)
        
        if self.pgb.button_A():
            if self.selected_piece is None:
                piece = self.board[self.cursor_y][self.cursor_x]
                if piece != '  ' and piece[0] == self.current_player[0]:
                    self.selected_piece = (self.cursor_x, self.cursor_y)
                    self.valid_moves = self.get_piece_moves(self.cursor_x, self.cursor_y)
                    if self.sound_enabled:
                        self.pgb.sound(660, 50)
                        sleep(0.05)
                        self.pgb.sound(0)
            else:
                if (self.cursor_x, self.cursor_y) in self.valid_moves:
                    self.make_move(self.selected_piece, (self.cursor_x, self.cursor_y))
                    self.selected_piece = None
                    self.valid_moves = []
                    
                    # Check for game end conditions
                    if self.is_checkmate():
                        self.game_state = self.GAME_OVER
                    elif self.is_stalemate():
                        self.game_state = self.GAME_OVER
                    elif self.game_mode == 'ai' and self.current_player == 'black':
                        self.ai_make_move()
            sleep(0.2)
        
        if self.pgb.button_B():
            self.selected_piece = None
            self.valid_moves = []
            if self.sound_enabled:
                self.pgb.sound(220, 50)
                sleep(0.05)
                self.pgb.sound(0)
            sleep(0.2)

    def is_checkmate(self):
        # Check if current player has any legal moves
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece != '  ' and piece[0] == self.current_player[0]:
                    moves = self.get_piece_moves(x, y)
                    if moves:
                        return False
        
        # If no legal moves and in check, it's checkmate
        return self.is_in_check(self.current_player[0])

    def is_stalemate(self):
        # Check if current player has any legal moves
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece != '  ' and piece[0] == self.current_player[0]:
                    moves = self.get_piece_moves(x, y)
                    if moves:
                        return False
        
        # If no legal moves and not in check, it's stalemate
        return not self.is_in_check(self.current_player[0])

    def show_game_over(self):
        self.pgb.fill(self.BLACK)
        
        if self.is_checkmate():
            winner = "White" if self.current_player == "black" else "Black"
            self.pgb.center_text(f"{winner} wins!", self.WHITE)
        else:
            self.pgb.center_text("Stalemate!", self.WHITE)
        
        self.pgb.text("Press A to restart", 70, 140, self.WHITE)
        self.pgb.text("Press B for menu", 70, 160, self.WHITE)
        
        self.pgb.show()
        
        while True:
            if self.pgb.button_A():
                self.__init__()
                return
            if self.pgb.button_B():
                self.__init__()
                self.game_state = self.MENU
                return
            sleep(0.1)

    def animate_move(self, from_pos, to_pos):
        fx, fy = from_pos
        tx, ty = to_pos
        steps = 5
        
        piece = self.board[fy][fx]
        self.board[fy][fx] = '  '
        
        for i in range(steps + 1):
            self.pgb.fill(self.BLACK)
            self.draw_board()
            
            # Draw moving piece
            x = fx + (tx - fx) * i / steps
            y = fy + (ty - fy) * i / steps
            
            piece_x = int(x * self.SQUARE_SIZE + (self.SQUARE_SIZE - self.PIECE_SIZE) // 2)
            piece_y = int(y * self.SQUARE_SIZE + (self.SQUARE_SIZE - self.PIECE_SIZE) // 2)
            
            self.draw_piece(piece, piece_x // self.SQUARE_SIZE, piece_y // self.SQUARE_SIZE)
            self.pgb.show()
            
            sleep(0.05)
        
        self.board[ty][tx] = piece

    def run(self):
        while True:
            if self.game_state == self.MENU:
                self.draw_menu()
                self.handle_menu()
            
            elif self.game_state == self.PLAYING:
                # Update timer
                current_time = time()
                if self.current_player == 'white':
                    self.white_time -= current_time - self.last_move_time
                else:
                    self.black_time -= current_time - self.last_move_time
                self.last_move_time = current_time
                
                # Check for time out
                if self.white_time <= 0 or self.black_time <= 0:
                    self.game_state = self.GAME_OVER
                
                self.pgb.fill(self.BLACK)
                self.draw_board()
                self.handle_input()
                
                # Check if king is in check
                self.check_status = self.is_in_check(self.current_player[0])
            
            elif self.game_state == self.GAME_OVER:
                self.show_game_over()
            
            sleep(0.016)  # Cap at ~60 FPS

if __name__ == "__main__":
    game = ChessGame()
    game.run()
