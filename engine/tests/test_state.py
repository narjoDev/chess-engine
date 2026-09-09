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
    ],
)
def test_get_piece_attacked_squares(test_params: TestParams):

    game_state = GameState(
        pieces=[test_params.input_piece_to_evaluate] + test_params.other_input_pieces
    )
    squares = game_state.get_piece_attacked_squares(test_params.input_piece_to_evaluate)
    assert set(squares) == test_params._expected_moves
