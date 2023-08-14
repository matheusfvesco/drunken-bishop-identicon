import hashlib
from typing import Tuple
from xml.etree.ElementTree import Element, tostring
import base64

import numpy as np


class DrunkenBishopIdenticon:
    """Class for generating Drunken Bishop identicons.

    Attributes:
        slug (str): The input string used to generate the identicon.
        board_size (Tuple[int, int]): The size of the board used to generate the identicon.
        hash (str): The hash map generated from the input slug.
        board (np.ndarray): The board generated from the hash map.
        svg_string (str): The SVG string representation of the identicon.
    """

    def __init__(self, slug: str, bsize: int = 7, iter: int = 1) -> None:
        """Initializes a DrunkenBishopIdenticon object.

        Args:
            slug (str): The input string used to generate the identicon.
            bsize (int, optional): The size of the board. Defaults to 7.
            iter (int, optional): The number of iterations to run the drunken bishop algorithm. Defaults to 1.
        """
        self.slug = slug
        self.board_size = (bsize, bsize)
        self.hash = self.slug_to_hashmap(self.slug)
        self.board = self.gen_board(bsize, self.hash, iter)
        self.svg_string = self.svg()

    def gen_board(
        self,
        board_size: int,
        hash_map: str,
        num_iterations: int = 1,
        invert: bool = True,
    ) -> np.ndarray:
        """Generates a board using the drunken bishop algorithm.

        Args:
            board_size (int): The size of the board.
            hash_map (str): The hash map used to generate the board.
            num_iterations (int, optional): The number of iterations to run the algorithm. Defaults to 1.
            invert (bool, optional): Whether to invert the directions every other iteration. Defaults to True.

        Returns:
            np.ndarray: The generated board.
        """
        board = np.zeros((board_size, board_size), dtype=int)
        x, y = board_size // 2, board_size // 2
        for i in range(num_iterations):
            directions = hash_map[::-1] if invert and i % 2 == 1 else hash_map
            for direction in directions:
                if direction in "NW":
                    y = max(0, y - 1)
                if direction in "SE":
                    y = min(board_size - 1, y + 1)
                if direction in "NE":
                    x = max(0, x - 1)
                if direction in "SW":
                    x = min(board_size - 1, x + 1)
                board[x, y] += 1
        return board

    def slug_to_hashmap(self, slug: str) -> str:
        """Converts a slug to a hash map.

        Args:
            slug (str): The input slug.

        Returns:
            str: The generated hash map.
        """
        hash = hashlib.sha256(slug.encode()).hexdigest()
        hex_to_dir = {
            "0": "N",
            "1": "N",
            "2": "N",
            "3": "N",
            "4": "E",
            "5": "E",
            "6": "E",
            "7": "E",
            "8": "S",
            "9": "S",
            "a": "S",
            "b": "S",
            "c": "W",
            "d": "W",
            "e": "W",
            "f": "W",
        }
        return "".join([hex_to_dir[c] for c in hash])

    def svg(self, size: int = 300) -> str:
        """Generates an SVG string representation of the identicon.

        Args:
            size (int, optional): The size of the SVG image. Defaults to 300.

        Returns:
            str: The SVG string representation of the identicon.
        """
        normalized_board = (
            (self.board - self.board.min())
            / (self.board.max() - self.board.min())
            * 255
        )
        color = [
            int(hashlib.sha256(self.hash.encode()).hexdigest()[i : i + 2], 16)
            for i in range(0, 6, 2)
        ]
        image = np.zeros((*self.board.shape, 3), dtype=np.uint8)
        for i in range(3):
            image[:, :, i] = normalized_board * color[i] / 255
        return self.numpy_to_svg(image, size, size)

    @staticmethod
    def numpy_to_svg(arr: np.ndarray, width: int, height: int) -> str:
        """Converts a numpy array to an SVG image with the given width and height.

        Args:
            arr (np.ndarray): The input numpy array.
            width (int): The width of the SVG image.
            height (int): The height of the SVG image.

        Returns:
            str: The SVG string representation of the input numpy array.
        """
        svg = Element("svg", width=str(width), height=str(height))
        rect_width = width / arr.shape[1]
        rect_height = height / arr.shape[0]
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                color = arr[i, j]
                color = np.append(color, 255) if len(color) == 3 else color
                rect = Element(
                    "rect",
                    x=str(j * rect_width),
                    y=str(i * rect_height),
                    width=str(rect_width),
                    height=str(rect_height),
                    fill="rgba({},{},{},{})".format(*color),
                )
                svg.append(rect)
        return tostring(svg).decode("utf-8")
    
    def svg_base64(self,size: int = 300) -> str:
        """Returns the base64 encoding of the SVG image.

        Returns:
            str: The base64 encoding of the SVG image.
        """
        return base64.b64encode(self.svg(size).encode('utf-8')).decode('utf-8')
