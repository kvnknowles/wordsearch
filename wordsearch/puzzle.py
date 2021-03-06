from array import array
from itertools import chain, islice, tee
from typing import Tuple, List, Iterator, TextIO

from wordsearch.grid import Coordinates, Vector, Grid, terminal, directions

def parse_line(line: str) -> List[str]:
  """Strip a line of its newline ending character and tokenize on comma separators"""
  return line.rstrip('\n').split(',')

def read_puzzle(lines: TextIO) -> Tuple[List[str], Grid]:
  """Parses a puzzle input file into the list of words and the character grid"""
  words = parse_line(lines.readline())
  characters = map(ord, chain(*map(parse_line, lines)))

  return words, Grid(array('I', characters))

def find_all(grid: Grid, letter: str) -> Iterator[Coordinates]:
  """Find the locations of each instance of a character in the grid"""
  for point, char in grid.items():
    if char == letter:
      yield point

def search_vectors(grid: Grid, position: Coordinates, distance: int) -> Iterator[Vector]:
  """Generate all candidate search vectors from a starting position on a grid"""
  for direction in directions():
    # Filter out vectors whose length would be too short to match the word (borders approaching an edge)
    if terminal(position, direction, distance) in grid:

      # Create the vector and limit the search distance to the length of the word
      yield islice(grid.vector(position, direction), distance)

def find_word(grid: Grid, word: str) -> Iterator[Coordinates]:
  """Finds a word by searching in all direction of a grid, returning the location of each letter"""
  first_letter = word[0]
  length = len(word)

  if length < 2:
    raise ValueError(f"Search word must be at least two characters long! Got '{word}'")

  for position in find_all(grid, first_letter):
    for search_vector in search_vectors(grid, position, length):
      # Save a copy of the search vector to return if it matches the word
      points, result = tee(search_vector)

      # Translate the point vector to the character at each coordinate location
      characters = map(lambda it: grid[it], points)

      # Compare each character of the word to the characters in the search vector, returning early if no match found
      if all(a == b for a, b in zip(word, characters)):
        return result

  raise ValueError(f"{word} not found in puzzle!")
