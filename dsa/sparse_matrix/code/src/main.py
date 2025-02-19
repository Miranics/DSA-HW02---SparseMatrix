"""
Main program for Sparse Matrix operations.
Author: Miranics
Date: 2025-02-19 10:44:59
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
    Perform the specified matrix operation.
    
    Args:
        operation (str): Name of operation to perform
        
    Returns:
        Optional[SparseMatrix]: Result matrix or None if operation failed
    """
    # Load first matrix
    matrix1 = load_matrix("Enter path to first matrix file: ")
    if matrix1 is None:
        return None
        
    # Load second matrix
    matrix2 = load_matrix("Enter path to second matrix file: ")
    if matrix2 is None:
        return None
        
    try:
        # Perform requested operation
        if operation == "addition":
            return matrix1.add(matrix2)
        elif operation == "subtraction":
            return matrix1.subtract(matrix2)
        elif operation == "multiplication":
            return matrix1.multiply(matrix2)
    except ValueError as e:
        print(f"Error performing {operation}: {str(e)}")
    except Exception as e:
        print(f"Unexpected error during {operation}: {str(e)}")
    
    return None

def main() -> None:
    """Main program loop."""
    while True:
        try:
            print_menu()
            choice = input().strip()
            
            if choice == '1':
                result = perform_operation("addition")
                if result:
                    save_result(result, "addition")
                    
            elif choice == '2':
                result = perform_operation("subtraction")
                if result:
                    save_result(result, "subtraction")
                    
            elif choice == '3':
                result = perform_operation("multiplication")
                if result:
                    save_result(result, "multiplication")
                    
            elif choice == '4':
                matrix = load_matrix("Enter path to matrix file: ")
                if matrix:
                    display_matrix_statistics(matrix)
                    
            elif choice == '5':
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice! Please try again.")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()