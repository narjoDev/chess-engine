from enum import Enum


class Color(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"


class PieceType(Enum):
    KING = "KING"
    QUEEN = "QUEEN"
    ROOK = "ROOK"
    BISHOP = "BISHOP"
    KNIGHT = "KNIGHT"
    PAWN = "PAWN"


class File(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"


class Square:
    def __init__(self, file: File, rank: int):
        assert rank >= 1 and rank <= 8
        self.file = file
        self.rank = rank


class Piece:
    def __init__(self, color, piece_type):
        self.color: Color = color
        self.piece_type: PieceType = piece_type
        self.has_moved: bool = False


class GameState:
    def __init__(self):
        self.board: dict[tuple[str, int], Piece] = {
            ("a", 1): Piece(Color.WHITE, PieceType.ROOK),
            ("b", 1): Piece(Color.WHITE, PieceType.KNIGHT),
            ("c", 1): Piece(Color.WHITE, PieceType.BISHOP),
            ("d", 1): Piece(Color.WHITE, PieceType.QUEEN),
            ("e", 1): Piece(Color.WHITE, PieceType.KING),
            ("f", 1): Piece(Color.WHITE, PieceType.BISHOP),
            ("g", 1): Piece(Color.WHITE, PieceType.KNIGHT),
            ("h", 1): Piece(Color.WHITE, PieceType.ROOK),
            **{(file, 2): Piece(Color.WHITE, PieceType.PAWN) for file in "abcdefgh"},
            **{(file, 7): Piece(Color.BLACK, PieceType.PAWN) for file in "abcdefgh"},
            ("a", 8): Piece(Color.BLACK, PieceType.ROOK),
            ("b", 8): Piece(Color.BLACK, PieceType.KNIGHT),
            ("c", 8): Piece(Color.BLACK, PieceType.BISHOP),
            ("d", 8): Piece(Color.BLACK, PieceType.QUEEN),
            ("e", 8): Piece(Color.BLACK, PieceType.KING),
            ("f", 8): Piece(Color.BLACK, PieceType.BISHOP),
            ("g", 8): Piece(Color.BLACK, PieceType.KNIGHT),
            ("h", 8): Piece(Color.BLACK, PieceType.ROOK),
        }

    def is_move_legal(self, move) -> bool:
        # can piece move like that
        # is piece blocking or in between
        # will mover's king enter check (handles pins)
        pass

    def is_color_in_check(self, color: Color) -> bool:
        pass

    def is_color_in_checkmate(self, color: Color) -> bool:
        pass

    def get_piece_attacked_squares(self, piece) -> list[Square]:
        # does not filter attacked squares (ignores other pieces)
        pass

    def get_piece_movable_squares(self, piece) -> list[Square]:
        # includes attacked squares
        # only different from get_piece_attacked_squares for PAWNS
        pass
