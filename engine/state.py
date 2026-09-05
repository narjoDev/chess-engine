from enum import Enum
from dataclasses import dataclass
from typing import Optional


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

    def attack_direction(self, color: Color) -> set[tuple[int, int]]:
        # (file, rank) offset convention e.g. e4

        diagonals = {(-1, -1), (-1, 1), (1, -1), (1, 1)}
        horizontal_vertical = {(0, 1), (0, -1), (1, 0), (-1, 0)}

        if self == PieceType.ROOK:
            return horizontal_vertical
        elif self in {PieceType.KING, PieceType.QUEEN}:
            return horizontal_vertical | diagonals
        elif self == PieceType.BISHOP:
            return diagonals
        elif self == PieceType.KNIGHT:
            return {
                (-2, -1),
                (-2, 1),
                (2, -1),
                (2, 1),
                (1, 2),
                (1, -2),
                (-1, 2),
                (-1, -2),
            }
        elif self == PieceType.PAWN:
            if color == Color.WHITE:
                return {(-1, 1), (1, 1)}
            else:
                return {(-1, -1), (1, -1)}
        else:
            raise ValueError(f"Unknown enum {self}")

    def can_only_move_distance_1(self) -> bool:
        return self in {PieceType.KING, PieceType.KNIGHT, PieceType.PAWN}


class File(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7
    H = 8

    @classmethod
    def is_within_bounds(cls, value: int) -> bool:
        return value >= 1 and value <= 8


def is_rank_within_bounds(value: int) -> bool:
    return value >= 1 and value <= 8


@dataclass(frozen=True)
class Square:
    file: File
    rank: int

    def __post_init__(self):
        assert self.rank >= 1 and self.rank <= 8

    def offset(self, offset_file: int, offset_rank: int) -> Optional["Square"]:
        new_file_value: int = self.file.value + offset_file
        if not File.is_within_bounds(new_file_value):
            return None

        new_rank_value: int = self.rank + offset_rank
        if not is_rank_within_bounds(new_rank_value):
            return None

        return Square(File(new_file_value), new_rank_value)


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
        """Check if a move (start square, end square) is legal.
        Checks include:
            - the start square contains a piece
            - it is the moving player's turn
            - the piece can move in the direction specified
            - the piece is not blocked from the end square
            - if the move captures, the captured piece is the opposite color
            - the move does not place the mover in check (handles pins)
        """
        # is it the right player's turn?
        # can piece move like that
        # is piece blocking or in between
        # will mover's king enter (or stay in) check (handles pins)
        # make move
        # is color in check
        # unmake last move
        pass

    def get_legal_moves(self) -> list[Move]:
        """Get all legal moves for the current player."""
        # Call `get_piece_movable_squares` and filter using `is_move_legal`
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

    def get_piece_attacked_squares(self, piece: Piece) -> list[Square]:
        # takes into account:
        # blocks? yes
        # piece being pinned? no
        # includes both captures and empty squares

        # pawns: flip per color

        BOARD_DIM = 8

        attacked_squares = []

        # for my piece, visit every possible "direction"
        for direction in piece.piece_type.attack_direction(piece.color):
            direction_file, direction_rank = direction

            # for pieces that can move more than 1 distance, iterate until blocked
            if piece.piece_type.can_only_move_distance_1():
                distance_limit = 1
            else:
                distance_limit = BOARD_DIM

            for distance in range(distance_limit):
                offset_file = distance * direction_file
                offset_rank = distance * direction_rank

                candidate_square: Optional[Square] = piece.square.offset(
                    offset_file, offset_rank
                )
                # bounds check
                if not candidate_square:
                    break

                # square already occupied check
                if candidate_square in self.board:
                    existing_piece = self.board[candidate_square]
                    is_same_color = piece.color == existing_piece.color

                    if not is_same_color:
                        attacked_squares.append(candidate_square)
                    break

                # TODO any other checks?

                attacked_squares.append(candidate_square)

        return attacked_squares

    def get_piece_movable_squares(self, piece: Piece) -> list[Square]:
        # "movable" includes attacked squares
        # excludes squares with friendly pieces
        # does not take into account pins
        if piece.piece_type != PieceType.PAWN:
            return self.get_piece_attacked_squares(piece)

        # PAWN: offset always (0, 1) - if hasn't moved also (0, 2)
        pass
