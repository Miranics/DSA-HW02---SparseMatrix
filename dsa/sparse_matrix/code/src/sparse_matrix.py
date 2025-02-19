"""
Sparse Matrix Implementation using Dictionary of Keys (DOK) format.
Author: Miranics
Date: 2025-02-19 11:08:23

This module implements a sparse matrix class that efficiently stores
only non-zero elements using a dictionary-based storage format.
"""

from typing import Dict, Tuple, List, Union
import os

class SparseMatrix:
    """
    A memory-efficient implementation of sparse matrices using dictionary of keys (DOK) format.
    
    This implementation stores only non-zero elements in a dictionary where the key is a tuple
    of (row, col) and the value is the non-zero element. This makes it memory efficient for
    matrices with many zero elements.
    
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
            
    def _process_header(self, rows_line: str, cols_line: str) -> Tuple[int, int]:
        """
        Process and validate the header lines of the matrix file.
        
        Args:
            rows_line (str): Line containing row information
            cols_line (str): Line containing column information
            
        Returns:
            Tuple[int, int]: Number of rows and columns
            
        Raises:
            ValueError: If header format is invalid
        """
        if not rows_line.startswith('rows=') or not cols_line.startswith('cols='):
            raise ValueError("Input file has wrong format: Missing rows/cols headers")
            
        try:
            rows = int(rows_line[5:])
            cols = int(cols_line[5:])
            
            if rows <= 0 or cols <= 0:
                raise ValueError(f"Invalid dimensions: {rows}x{cols} (must be positive)")
                
            return rows, cols
            
        except ValueError:
            raise ValueError("Invalid number format in headers")

    def _load_from_file(self, file_path: str) -> None:
        """
        Load matrix data from a file.
        
        Args:
            file_path (str): Path to the input file
            
        Raises:
            ValueError: If file format is invalid
            FileNotFoundError: If file doesn't exist
        """
        try:
            with open(file_path, 'r') as file:
                # Read headers
                rows_line = file.readline().strip()
                if not rows_line:
                    raise ValueError("File is empty")
                    
                cols_line = file.readline().strip()
                if not cols_line:
                    raise ValueError("Missing columns specification")
                
                # Process headers
                self.rows, self.cols = self._process_header(rows_line, cols_line)
                
                # Read matrix elements
                line_num = 2  # Start counting from line 3 (0-based index + 2 header lines)
                elements_loaded = 0
                invalid_elements = 0
                
                for line in file:
                    line_num += 1
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    
                    # Validate format
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError(
                            f"Invalid element format at line {line_num}: {line}\n"
                            f"Expected format: (row, col, value)"
                        )
                    
                    try:
                        # Parse (row, col, value)
                        content = line[1:-1].replace(' ', '')  # Remove parentheses and spaces
                        parts = content.split(',')
                        
                        if len(parts) != 3:
                            raise ValueError(
                                f"Invalid element format at line {line_num}: {line}\n"
                                f"Expected three comma-separated values: (row, col, value)"
                            )
                            
                        row, col, value = map(int, parts)
                        
                        # Skip elements that are out of bounds but warn user
                        if not (0 <= row < self.rows and 0 <= col < self.cols):
                            print(f"Warning: Skipping out-of-bounds element at line {line_num}: {line}")
                            invalid_elements += 1
                            continue
                            
                        self.set_element(row, col, value)
                        elements_loaded += 1
                            
                    except ValueError as e:
                        if str(e).startswith("Invalid element format"):
                            raise
                        raise ValueError(
                            f"Invalid number format at line {line_num}: {line}\n"
                            f"All values must be integers"
                        )
                
                print(f"Successfully loaded {elements_loaded} elements")
                if invalid_elements > 0:
                    print(f"Skipped {invalid_elements} invalid elements")
                        
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
                    
            print(f"Saved {len(self.elements)} elements to {file_path}")
            
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

    def __str__(self) -> str:
        """
        Get string representation of the matrix.
        
        Returns:
            str: String representation showing dimensions and number of non-zero elements
        """
        stats = self.get_statistics()
        return (
            f"SparseMatrix({self.rows}x{self.cols}) with "
            f"{len(self.elements)} non-zero elements "
            f"(density: {stats['density']:.2%})"
        )

    def __repr__(self) -> str:
        """
        Get detailed string representation of the matrix.
        
        Returns:
            str: Detailed string representation including dimensions and elements
        """
        return (
            f"SparseMatrix(rows={self.rows}, cols={self.cols}, "
            f"elements={dict(sorted(self.elements.items()))})"
        )