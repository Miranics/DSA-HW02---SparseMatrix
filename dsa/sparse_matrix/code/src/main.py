"""
Main program for Sparse Matrix operations.
Author: Miranics
Date: 2025-02-19 10:29:38
"""

from sparse_matrix import SparseMatrix
from typing import Optional, Tuple
import os
import sys

def print_menu() -> None:
    """Display menu options."""
    print("\nSparse Matrix Operations")
    print("1. Add matrices")
    print("2. Subtract matrices")
    print("3. Multiply matrices")
    print("4. Display matrix statistics")
    print("5. Exit")
    print("Enter your choice: ", end="")

def get_valid_filepath(prompt: str) -> str:
    """
    Get a valid file path from user input.
    
    Args:
        prompt (str): Message to display to user
        
    Returns:
        str: Valid file path
        
    Raises:
        KeyboardInterrupt: If user cancels input
    """
    while True:
        try:
            file_path = input(prompt).strip()
            if os.path.isfile(file_path):
                return file_path
            print(f"Error: File '{file_path}' does not exist.")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"Error: {str(e)}")

def load_matrix(prompt: str) -> Optional[SparseMatrix]:
    """
    Load a matrix from a file with error handling.
    
    Args:
        prompt (str): Message to display to user
        
    Returns:
        Optional[SparseMatrix]: Loaded matrix or None if loading failed
    """
    try:
        file_path = get_valid_filepath(prompt)
        return SparseMatrix(file_path)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error loading matrix: {str(e)}")
        return None
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

def save_result(matrix: SparseMatrix, operation: str) -> bool:
    """
    Save matrix result to file with error handling.
    
    Args:
        matrix (SparseMatrix): Matrix to save
        operation (str): Operation name for filename
        
    Returns:
        bool: True if save was successful, False otherwise
    """
    try:
        output_path = f"result_{operation}.txt"
        matrix.save_to_file(output_path)
        print(f"Result saved to {output_path}")
        return True
    except IOError as e:
        print(f"Error saving result: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error while saving: {str(e)}")
        return False

def display_matrix_statistics(matrix: SparseMatrix) -> None:
    """
    Display statistical information about the matrix.
    
    Args:
        matrix (SparseMatrix): Matrix to analyze
    """
    stats = matrix.get_statistics()
    print("\nMatrix Statistics:")
    print(f"Dimensions: {stats['dimensions'][0]} x {stats['dimensions'][1]}")
    print(f"Non-zero elements: {stats['non_zero_elements']}")
    print(f"Total elements: {stats['total_elements']}")
    print(f"Density: {stats['density']:.4%}")
    if stats['min_value'] is not None:
        print(f"Minimum value: {stats['min_value']}")
        print(f"Maximum value: {stats['max_value']}")

def perform_operation(operation: str) -> Optional[SparseMatrix]:
    """
    Perform matrix operation based on given operation type.
    
    Args:
        operation (str): Type of operation to perform
        
    Returns:
        Optional[SparseMatrix]: Result matrix or None if operation failed
    """
    matrix1 = load_matrix("Enter path for first matrix: ")
    if matrix1 is None:
        return None
        
    matrix2 = load_matrix("Enter path for second matrix: ")
    if matrix2 is None:
        return None
        
    try:
        if operation == "add":
            return matrix1 + matrix2
        elif operation == "subtract":
            return matrix1 - matrix2
        elif operation == "multiply":
            return matrix1 * matrix2
        else:
            print(f"Unsupported operation: {operation}")
            return None
    except ValueError as e:
        print(f"Error performing operation: {str(e)}")
        return None