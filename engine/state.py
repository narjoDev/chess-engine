from enum import Enum
from dataclasses import dataclass


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


@dataclass
class Move:
    start: Square
    end: Square


class Piece:
    def __init__(self, color, piece_type):
        self.color: Color = color
        self.piece_type: PieceType = piece_type
        self.has_moved: bool = False


class GameState:
    def __init__(self):
        self.board: dict[Square, Piece] = {
            Square(File.A, 1): Piece(Color.WHITE, PieceType.ROOK),
            Square(File.B, 1): Piece(Color.WHITE, PieceType.KNIGHT),
            Square(File.C, 1): Piece(Color.WHITE, PieceType.BISHOP),
            Square(File.D, 1): Piece(Color.WHITE, PieceType.QUEEN),
            Square(File.E, 1): Piece(Color.WHITE, PieceType.KING),
            Square(File.F, 1): Piece(Color.WHITE, PieceType.BISHOP),
            Square(File.G, 1): Piece(Color.WHITE, PieceType.KNIGHT),
            Square(File.H, 1): Piece(Color.WHITE, PieceType.ROOK),
            **{
                Square(file, 2): Piece(Color.WHITE, PieceType.PAWN)
                for file in list(File)
            },
            **{
                Square(file, 7): Piece(Color.BLACK, PieceType.PAWN)
                for file in list(File)
            },
            Square(File.A, 8): Piece(Color.BLACK, PieceType.ROOK),
            Square(File.B, 8): Piece(Color.BLACK, PieceType.KNIGHT),
            Square(File.C, 8): Piece(Color.BLACK, PieceType.BISHOP),
            Square(File.D, 8): Piece(Color.BLACK, PieceType.QUEEN),
            Square(File.E, 8): Piece(Color.BLACK, PieceType.KING),
            Square(File.F, 8): Piece(Color.BLACK, PieceType.BISHOP),
            Square(File.G, 8): Piece(Color.BLACK, PieceType.KNIGHT),
            Square(File.H, 8): Piece(Color.BLACK, PieceType.ROOK),
        }
        self.mover = Color.WHITE
        self.moves: list = []

    def is_move_legal(self, move: Move) -> bool:
        # is it the right player's turn?
        # can piece move like that
        # is piece blocking or in between
        # will mover's king enter check (handles pins)
        pass

    def get_legal_moves(self) -> list[Move]:
        pass

    def is_color_in_check(self, color: Color) -> bool:
        # get king square
        # for each enemy piece
        # get attacked squares
        # if king square in attacked squares return true
        # end loop
        # return false
        pass

    def is_color_in_checkmate(self, color: Color) -> bool:
        # in check true
        # and legal moves empty
        pass

    def make_move(self, move: Move) -> bool:
        pass

    def unmake_last_move(self) -> bool:
        pass

    def get_piece_attacked_squares(self, piece) -> list[Square]:
        # takes into account:
        # blocks? yes
        # piece being pinned? no
        # includes both captures and empty squares
        pass

    def get_piece_movable_squares(self, piece) -> list[Square]:
        # includes attacked squares
        # only different from get_piece_attacked_squares for PAWNS
        pass
