import pytest

from engine.state import *


# TODO: parameterize for more pieces
# TODO: test pins
# TODO: test if piece is blocked
# TODO: `game_state` is initialized with default positions

# TODO: create the test with a very specific and simple board


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
            test_case_name="King basic",
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
            test_case_name="Rook with friendly piece in the way",
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
            test_case_name="Queen can move onto enemy position",
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
            # NOTE: the function being tested does NOT check threatened squares
            test_case_name="King cannot move into threatened squares",
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

    # TODO: move the pawn, check only move 1
    # TODO: test black not just white


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
