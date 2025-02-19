"""
Sparse Matrix Implementation using Dictionary of Keys (DOK) format.
Author: Miranics
Date: 2025-02-19 10:29:38
Description: A memory-efficient implementation of sparse matrices that only stores non-zero elements.
"""

from typing import Dict, Tuple, List, Union
import os

class SparseMatrix:
    """
    A memory-efficient implementation of a sparse matrix using dictionary of keys (DOK) format.
    
    This implementation stores only non-zero elements in a dictionary where the key is a tuple
    of (row, col) and the value is the non-zero element. This approach is memory efficient
    for matrices with many zero elements.

    Attributes:
        rows (int): Number of rows in the matrix
        cols (int): Number of columns in the matrix
        elements (Dict[Tuple[int, int], int]): Dictionary storing non-zero elements
    """
    
    def __init__(self, matrix_file_path: str = None, num_rows: int = 0, num_cols: int = 0):
        """
        Initialize sparse matrix either from file or with given dimensions.
        
        Args:
            matrix_file_path (str, optional): Path to input file containing matrix data
            num_rows (int, optional): Number of rows if creating empty matrix
            num_cols (int, optional): Number of columns if creating empty matrix
            
        Raises:
            ValueError: If file format is invalid or dimensions are negative
        """
        self.elements: Dict[Tuple[int, int], int] = {}
        
        if matrix_file_path:
            self._load_from_file(matrix_file_path)
        else:
            if num_rows < 0 or num_cols < 0:
                raise ValueError("Matrix dimensions cannot be negative")
            self.rows = num_rows
            self.cols = num_cols

    def _load_from_file(self, file_path: str) -> None:
        """
        Load matrix data from a file.
        
        The file format should be:
        rows=<number>
        cols=<number>
        (row, col, value)
        (row, col, value)
        ...
        
        Args:
            file_path (str): Path to the input file
            
        Raises:
            ValueError: If file format is invalid
            FileNotFoundError: If file doesn't exist
        """
        try:
            with open(file_path, 'r') as file:
                # Read and validate dimensions
                rows_line = file.readline().strip()
                cols_line = file.readline().strip()
                
                if not rows_line.startswith('rows=') or not cols_line.startswith('cols='):
                    raise ValueError("Input file has wrong format: Missing rows/cols headers")
                
                try:
                    self.rows = int(rows_line[5:])
                    self.cols = int(cols_line[5:])
                    if self.rows < 0 or self.cols < 0:
                        raise ValueError("Matrix dimensions cannot be negative")
                except ValueError:
                    raise ValueError("Invalid dimensions in input file")
                
                # Read matrix elements
                for line_num, line in enumerate(file, 3):  # Start counting from line 3
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError(f"Invalid element format at line {line_num}: {line}")
                    
                    try:
                        # Parse (row, col, value)
                        content = line[1:-1].replace(' ', '')  # Remove parentheses and spaces
                        row, col, value = map(int, content.split(','))
                        
                        # Validate indices
                        if not (0 <= row < self.rows and 0 <= col < self.cols):
                            raise ValueError(
                                f"Invalid indices at line {line_num}: ({row}, {col})"
                                f" - Must be within bounds [0,{self.rows-1}] x [0,{self.cols-1}]"
                            )
                        
                        self.set_element(row, col, value)
                    except ValueError as e:
                        raise ValueError(f"Invalid number format at line {line_num}: {line}")
                        
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not open file: {file_path}")

    def get_element(self, row: int, col: int) -> int:
        """
        Get element at specified position.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            int: Value at position (0 if position contains no entry)
            
        Raises:
            ValueError: If indices are out of bounds
        """
        self._validate_indices(row, col)
        return self.elements.get((row, col), 0)

    def set_element(self, row: int, col: int, value: int) -> None:
        """
        Set element at specified position.
        
        Args:
            row (int): Row index
            col (int): Column index
            value (int): Value to set
            
        Raises:
            ValueError: If indices are out of bounds
        """
        self._validate_indices(row, col)
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]

    def _validate_indices(self, row: int, col: int) -> None:
        """
        Validate if indices are within matrix bounds.
        
        Args:
            row (int): Row index to validate
            col (int): Column index to validate
            
        Raises:
            ValueError: If indices are out of bounds
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError(
                f"Invalid indices: ({row}, {col}) - "
                f"Must be within bounds [0,{self.rows-1}] x [0,{self.cols-1}]"
            )

    def add(self, other: 'SparseMatrix') -> 'SparseMatrix':
        """
        Add two sparse matrices.
        
        Args:
            other (SparseMatrix): Matrix to add
            
        Returns:
            SparseMatrix: Result of addition
            
        Raises:
            ValueError: If matrix dimensions don't match
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                f"Matrix dimensions must match for addition: "
                f"({self.rows}, {self.cols}) != ({other.rows}, {other.cols})"
            )
        
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        
        # Add elements from both matrices
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value)
        
        for (row, col), value in other.elements.items():
            current = result.get_element(row, col)
            result.set_element(row, col, current + value)
        
        return result

    def subtract(self, other: 'SparseMatrix') -> 'SparseMatrix':
        """
        Subtract two sparse matrices.
        
        Args:
            other (SparseMatrix): Matrix to subtract
            
        Returns:
            SparseMatrix: Result of subtraction
            
        Raises:
            ValueError: If matrix dimensions don't match
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                f"Matrix dimensions must match for subtraction: "
                f"({self.rows}, {self.cols}) != ({other.rows}, {other.cols})"
            )
        
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        
        # Add elements from first matrix
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value)
        
        # Subtract elements from second matrix
        for (row, col), value in other.elements.items():
            current = result.get_element(row, col)
            result.set_element(row, col, current - value)
        
        return result

    def multiply(self, other: 'SparseMatrix') -> 'SparseMatrix':
        """
        Multiply two sparse matrices.
        
        This implementation uses an efficient approach that only processes
        non-zero elements, making it especially efficient for sparse matrices.
        
        Args:
            other (SparseMatrix): Matrix to multiply with
            
        Returns:
            SparseMatrix: Result of multiplication
            
        Raises:
            ValueError: If matrix dimensions are incompatible
        """
        if self.cols != other.rows:
            raise ValueError(
                f"Invalid dimensions for multiplication: "
                f"Matrix 1 columns ({self.cols}) must equal Matrix 2 rows ({other.rows})"
            )
        
        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)
        
        # Group elements by row and column for efficient multiplication
        self_rows: Dict[int, Dict[int, int]] = {}
        other_cols: Dict[int, Dict[int, int]] = {}
        
        # Organize first matrix by rows
        for (row, col), value in self.elements.items():
            if row not in self_rows:
                self_rows[row] = {}
            self_rows[row][col] = value
        
        # Organize second matrix by columns
        for (row, col), value in other.elements.items():
            if col not in other_cols:
                other_cols[col] = {}
            other_cols[col][row] = value
        
        # Perform multiplication only for non-zero elements
        for i in self_rows:
            for j in other_cols:
                sum_value = 0
                for k in self_rows[i]:
                    if k in other_cols[j]:
                        sum_value += self_rows[i][k] * other_cols[j][k]
                if sum_value != 0:
                    result.set_element(i, j, sum_value)
        
        return result

    def save_to_file(self, file_path: str) -> None:
        """
        Save matrix to file in specified format.
        
        Args:
            file_path (str): Path where to save the matrix
            
        Raises:
            IOError: If file cannot be written
        """
        try:
            with open(file_path, 'w') as file:
                file.write(f"rows={self.rows}\n")
                file.write(f"cols={self.cols}\n")
                
                # Sort elements for consistent output
                sorted_elements = sorted(self.elements.items())
                for (row, col), value in sorted_elements:
                    file.write(f"({row}, {col}, {value})\n")
        except IOError as e:
            raise IOError(f"Error writing to file {file_path}: {str(e)}")

    def get_density(self) -> float:
        """
        Calculate the density of the matrix (proportion of non-zero elements).
        
        Returns:
            float: Density value between 0 and 1
        """
        total_elements = self.rows * self.cols
        if total_elements == 0:
            return 0.0
        return len(self.elements) / total_elements

    def get_statistics(self) -> dict:
        """
        Get statistical information about the matrix.
        
        Returns:
            dict: Dictionary containing matrix statistics
        """
        if not self.elements:
            return {
                "dimensions": (self.rows, self.cols),
                "non_zero_elements": 0,
                "density": 0.0,
                "min_value": None,
                "max_value": None,
                "total_elements": self.rows * self.cols
            }
        
        values = list(self.elements.values())
        return {
            "dimensions": (self.rows, self.cols),
            "non_zero_elements": len(self.elements),
            "density": self.get_density(),
            "min_value": min(values),
            "max_value": max(values),
            "total_elements": self.rows * self.cols
        }
