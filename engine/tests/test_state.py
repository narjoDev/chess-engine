import pytest

from engine.state import *

# TODO: test pins


@dataclass
class TestParams:
    __test__ = False  # Prevents pytest from trying to collect this class
    test_case_name: str
    input_piece_to_evaluate: Piece
    # does not include the above
    other_input_pieces: list[Piece]
    # `e3` will be converted to Square(File.E, 3)
    expected_moves: set[str]
    _expected_moves: set[Square] | None = None

    def __post_init__(self):
        self._expected_moves = {
            Square(File[sq[0].upper()], int(sq[1])) for sq in self.expected_moves
        }


@pytest.mark.parametrize(
    "test_params",
    [
        TestParams(
            test_case_name="King in open attacks surrounding squares",
            input_piece_to_evaluate=Piece(
                Color.WHITE, PieceType.KING, Square(File.E, 4)
            ),
            other_input_pieces=[],
            expected_moves={
                "e3",
                "e5",
                "d3",
                "d4",
                "d5",
                "f3",
                "f4",
                "f5",
            },
        ),
        TestParams(
            test_case_name="Rook is blocked by friendly piece",
            input_piece_to_evaluate=Piece(
                Color.WHITE, PieceType.ROOK, Square(File.E, 4)
            ),
            other_input_pieces=[Piece(Color.WHITE, PieceType.ROOK, Square(File.E, 5))],
            expected_moves={
                # e4 rook sees (1) entire 4th rank and (2) entire `e` file except where blocked by e5
                "a4",
                "b4",
                "c4",
                "d4",
                "e1",
                "e2",
                "e3",
                "f4",
                "g4",
                "h4",
            },
        ),
        TestParams(
            test_case_name="Knight in the corner doesn't go off the board",
            input_piece_to_evaluate=Piece(
                Color.WHITE, PieceType.KNIGHT, Square(File.A, 1)
            ),
            other_input_pieces=[],
            expected_moves={"b3", "c2"},
        ),
        TestParams(
            test_case_name="Queen can attack enemy occupied square",
            input_piece_to_evaluate=Piece(
                Color.WHITE, PieceType.QUEEN, Square(File.E, 4)
            ),
            other_input_pieces=[Piece(Color.BLACK, PieceType.PAWN, Square(File.E, 6))],
            expected_moves={
                # NOTE: you can visually inspect with render_expected_moves
                "a4",
                "a8",
                "b1",
                "b4",
                "b7",
                "c2",
                "c4",
                "c6",
                "d3",
                "d4",
                "d5",
                "e1",
                "e2",
                "e3",
                "e5",
                "e6",
                "f3",
                "f4",
                "f5",
                "g2",
                "g4",
                "g6",
                "h1",
                "h4",
                "h7",
            },
        ),
        TestParams(
            # NOTE: get_piece_attacked_squares does not filter out losing moves (e.g., moving into check)
            test_case_name="King attacked squares DOES include threatened squares",
            input_piece_to_evaluate=Piece(
                Color.WHITE, PieceType.KING, Square(File.E, 4)
            ),
            other_input_pieces=[Piece(Color.BLACK, PieceType.ROOK, Square(File.A, 5))],
            expected_moves={"d3", "d4", "d5", "e3", "e5", "f3", "f4", "f5"},
        ),
    ],
    ids=lambda test_params: test_params.test_case_name,
)
def test_get_piece_attacked_squares(test_params: TestParams):

    game_state = GameState(
        pieces=[test_params.input_piece_to_evaluate] + test_params.other_input_pieces
    )
    squares = game_state.get_piece_attacked_squares(test_params.input_piece_to_evaluate)
    assert set(squares) == test_params._expected_moves


# Tests that King is not in check by default
def test_is_color_in_check_false_by_default():

    game_state = GameState()
    assert not game_state.is_color_in_check(Color.WHITE)


# Tests that King in check from a piece
def test_is_color_in_check():

    game_state = GameState(
        pieces=[
            Piece(Color.WHITE, PieceType.KING, Square(File.E, 4)),
            Piece(Color.BLACK, PieceType.ROOK, Square(File.E, 5)),
        ]
    )
    assert game_state.is_color_in_check(Color.WHITE)


# Tests that `get_piece_movable_squares` has pawn moves and attacks
# whereas `get_piece_attackable_squares` has pawn attacks
def test_pawn_move_vs_attack():

    pawn = Piece(Color.WHITE, PieceType.PAWN, Square(File.E, 2))
    game_state = GameState(pieces=[pawn])

    move_attack = game_state.get_piece_movable_squares(pawn)

    expected_attack = {Square(File.D, 3), Square(File.F, 3)}
    expected_move = {Square(File.E, 3), Square(File.E, 4)}
    assert set(move_attack) == (expected_attack | expected_move)


def test_pawn_move_that_has_moved():

    pawn = Piece(Color.WHITE, PieceType.PAWN, Square(File.E, 2))
    game_state = GameState(pieces=[pawn])

    game_state.make_move(Move(Square(File.E, 2), Square(File.E, 3)))

    move_attack = game_state.get_piece_movable_squares(pawn)

    expected_attack = {Square(File.D, 4), Square(File.F, 4)}
    expected_move = {Square(File.E, 4)}
    assert set(move_attack) == (expected_attack | expected_move)


def test_pawn_move_black():

    pawn = Piece(Color.BLACK, PieceType.PAWN, Square(File.E, 7))
    game_state = GameState(pieces=[pawn])

    move_attack = game_state.get_piece_movable_squares(pawn)

    expected_attack = {Square(File.D, 6), Square(File.F, 6)}
    expected_move = {Square(File.E, 6), Square(File.E, 5)}
    assert set(move_attack) == (expected_attack | expected_move)


def test_pawn_is_blocked():

    white_pawn = Piece(Color.WHITE, PieceType.PAWN, Square(File.E, 2))
    black = Piece(Color.BLACK, PieceType.PAWN, Square(File.E, 3))
    game_state = GameState(pieces=[white_pawn, black])

    move_attack = game_state.get_piece_movable_squares(white_pawn)

    # movable squares includes empty threatened squares
    expected_attack = {Square(File.D, 3), Square(File.F, 3)}
    # movable squares excludes blocked forward move
    expected_move = set()
    assert set(move_attack) == (expected_attack | expected_move)


# # TODO en passant
# def test_pawn_en_passant():

#     white_pawn = Piece(Color.WHITE, PieceType.PAWN, Square(File.D, 2))
#     black_pawn = Piece(Color.BLACK, PieceType.PAWN, Square(File.C, 4))
#     game_state = GameState(pieces=[white_pawn, black_pawn])

#     # Test that en passant is an allowable move
#     # Test that en passant moves to the correct square and captures


# Tests positive and negative of:
#   (1) the start square contains a piece
#   (2) it is the moving player's turn
#   (3) end square is included in movable squares
#   (4) if the move captures, the captured piece is the opposite color
#   (5) the move does not place the mover in check (handles pins)
def test_is_move_legal_positive():
    white_queen = Piece(Color.WHITE, PieceType.QUEEN, Square(File.E, 2))
    black_queen = Piece(Color.BLACK, PieceType.QUEEN, Square(File.E, 3))
    game_state = GameState(pieces=[white_queen, black_queen])
    assert game_state.is_move_legal(Move(Square(File.E, 2), Square(File.E, 3)))


def test_is_move_legal_1_start_square_contains_a_piece():
    game_state = GameState()
    assert not game_state.is_move_legal(Move(Square(File.E, 4), Square(File.E, 5)))


def test_is_move_legal_2_is_it_the_moving_players_turn():
    # moving black but it's white's turn
    white_queen = Piece(Color.WHITE, PieceType.QUEEN, Square(File.E, 2))
    black_queen = Piece(Color.BLACK, PieceType.QUEEN, Square(File.E, 3))
    game_state = GameState(pieces=[white_queen, black_queen])
    assert not game_state.is_move_legal(Move(Square(File.E, 3), Square(File.E, 2)))


def test_is_move_legal_3_end_square_is_in_movable_squares():
    game_state = GameState()
    assert not game_state.is_move_legal(Move(Square(File.E, 2), Square(File.E, 5)))


def test_is_move_legal_4_captured_piece_is_opposing_color():
    game_state = GameState()
    # Bishop can't take own pawn
    assert not game_state.is_move_legal(Move(Square(File.F, 1), Square(File.E, 2)))


def test_is_move_legal_5_mover_is_pinned():

    # (enemy rook) - - - (my rook) (my king)
    black_rook = Piece(Color.BLACK, PieceType.ROOK, Square(File.D, 2))
    white_rook = Piece(Color.WHITE, PieceType.ROOK, Square(File.E, 2))
    white_king = Piece(Color.WHITE, PieceType.KING, Square(File.F, 2))
    game_state = GameState(pieces=[black_rook, white_rook, white_king])

    assert not game_state.is_move_legal(Move(Square(File.E, 2), Square(File.E, 3)))


def test_is_move_legal_5_mover_is_pinned_v2():

    # (white rook) (white king) => white rook can move
    white_rook = Piece(Color.WHITE, PieceType.ROOK, Square(File.E, 2))
    white_king = Piece(Color.WHITE, PieceType.KING, Square(File.F, 2))
    game_state = GameState(pieces=[white_rook, white_king])

    move_the_rook = Move(Square(File.E, 2), Square(File.E, 3))
    assert game_state.is_move_legal(move_the_rook)

    # now add a (black rook) like so:
    #   (black rook) (white rook) (white king) => white rook can't move out of the way
    black_rook = Piece(Color.BLACK, PieceType.ROOK, Square(File.D, 2))
    game_state = GameState(pieces=[black_rook, white_rook, white_king])

    assert not game_state.is_move_legal(move_the_rook)
    # white rook can still take black rook
    assert game_state.is_move_legal(Move(Square(File.E, 2), Square(File.D, 2)))


def test_is_move_legal_6_pawn_threatened_squares():

    white_pawn = Piece(Color.WHITE, PieceType.PAWN, Square(File.E, 2))
    black_blocker = Piece(Color.BLACK, PieceType.PAWN, Square(File.E, 3))
    black_threatened = Piece(Color.BLACK, PieceType.ROOK, Square(File.D, 3))
    game_state = GameState(pieces=[white_pawn, black_blocker, black_threatened])

    capture_rook_move = Move(Square(File.E, 2), Square(File.D, 3))
    assert game_state.is_move_legal(capture_rook_move)
    capture_empty_move = Move(Square(File.E, 2), Square(File.F, 3))
    assert not game_state.is_move_legal(capture_empty_move)


def test_unmake_last_move():
    white_pawn = Piece(Color.WHITE, PieceType.PAWN, Square(File.E, 2))
    black_pawn = Piece(Color.BLACK, PieceType.PAWN, Square(File.D, 3))
    game_state = GameState(pieces=[white_pawn, black_pawn])

    game_state.make_move(Move(Square(File.E, 2), Square(File.D, 3)))
    game_state.unmake_last_move()

    assert game_state.board.get(Square(File.E, 2)) == white_pawn
    assert game_state.board.get(Square(File.D, 3)) == black_pawn

    assert white_pawn in game_state.pieces
    assert black_pawn in game_state.pieces

    assert game_state.mover == Color.WHITE
    assert len(game_state.history) == 0


def test_is_move_legal_unmakes_move():
    white_pawn = Piece(Color.WHITE, PieceType.PAWN, Square(File.E, 2))
    black_pawn = Piece(Color.BLACK, PieceType.PAWN, Square(File.D, 3))
    game_state = GameState(pieces=[white_pawn, black_pawn])

    move = Move(Square(File.E, 2), Square(File.D, 3))
    assert game_state.is_move_legal(move)

    assert game_state.board.get(Square(File.E, 2)) == white_pawn
    assert game_state.board.get(Square(File.D, 3)) == black_pawn


# For debug visualization
def render_expected_moves(expected_moves: set[str]) -> str:
    rows = ["  a b c d e f g h"]

    for rank in range(8, 0, -1):
        cells = [
            "X" if f"{file.name.lower()}{rank}" in expected_moves else "."
            for file in File
        ]
        rows.append(f"{rank} {' '.join(cells)} {rank}")

    rows.append("  a b c d e f g h")
    return "\n".join(rows)
