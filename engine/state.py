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
    def __init__(self, color: Color, piece_type: PieceType, square: Square):
        self.color = color
        self.piece_type = piece_type
        self.square = square
        self.has_moved: bool = False


class GameState:
    def __init__(self):
        self.pieces = [
            Piece(Color.WHITE, PieceType.ROOK, Square(File.A, 1)),
            Piece(Color.WHITE, PieceType.KNIGHT, Square(File.B, 1)),
            Piece(Color.WHITE, PieceType.BISHOP, Square(File.C, 1)),
            Piece(Color.WHITE, PieceType.QUEEN, Square(File.D, 1)),
            Piece(Color.WHITE, PieceType.KING, Square(File.E, 1)),
            Piece(Color.WHITE, PieceType.BISHOP, Square(File.F, 1)),
            Piece(Color.WHITE, PieceType.KNIGHT, Square(File.G, 1)),
            Piece(Color.WHITE, PieceType.ROOK, Square(File.H, 1)),
            *[Piece(Color.WHITE, PieceType.PAWN, Square(file, 2)) for file in File],
            *[Piece(Color.BLACK, PieceType.PAWN, Square(file, 7)) for file in File],
            Piece(Color.BLACK, PieceType.ROOK, Square(File.A, 8)),
            Piece(Color.BLACK, PieceType.KNIGHT, Square(File.B, 8)),
            Piece(Color.BLACK, PieceType.BISHOP, Square(File.C, 8)),
            Piece(Color.BLACK, PieceType.QUEEN, Square(File.D, 8)),
            Piece(Color.BLACK, PieceType.KING, Square(File.E, 8)),
            Piece(Color.BLACK, PieceType.BISHOP, Square(File.F, 8)),
            Piece(Color.BLACK, PieceType.KNIGHT, Square(File.G, 8)),
            Piece(Color.BLACK, PieceType.ROOK, Square(File.H, 8)),
        ]

        self.board: dict[Square, Piece] = {piece.square: piece for piece in self.pieces}
        self.mover = Color.WHITE
        self.moves: list = []

    def is_move_legal(self, move: Move) -> bool:
        # is it the right player's turn?
        # can piece move like that
        # is piece blocking or in between
        # will mover's king enter (or stay in) check (handles pins)
        # make move
        # is color in check
        # unmake last move
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
        # switch on piece type
        # king
        # adjacent squares within bounds of board
        # queen
        # all other squares in rank
        # all other squares in file
        # diagonals
        # but stop on block
        # rook
        # bishop
        # knight
        # pawn

        # potential helper generating lines of possible squares (no block yet)
        # iterate through offsets
        # for offset generate line out from piece (not including piece square)
        # end on OOB
        # with list of squares iterate and stop on piece (means a block, last one)

        # ? generate_diagonals, generate_horizontals_verticals call below?
        # ^ both applying an offset, so we can have 1 main helper generate_line_from_offset(square, offset tuple, optional length 1 limit)
        # maybe blocking test isn't part of that?
        # blocking filter truncates list of squares on first with piece (inclusive for enemy, exclusive for yours)

        # maybe can do king, knight, pawn also as lines, but with limit length 1, same blocking logic should work

    def get_piece_movable_squares(self, piece) -> list[Square]:
        # includes attacked squares
        # only different from get_piece_attacked_squares for PAWNS
        pass
