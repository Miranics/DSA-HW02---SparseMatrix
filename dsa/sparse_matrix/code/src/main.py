"""
Sparse Matrix Calculator
Author: Miranics
Date: 2025-02-19 12:19:22
"""

from sparse_matrix import SparseMatrix
from typing import Optional, Tuple, List
import os
import sys

# Store the sample files for quick access
SAMPLE_FILES = {
    '1': "../../sample_inputs/matrix1.txt",
    '2': "../../sample_inputs/matrix2.txt",
    '3': "../../sample_inputs/matrix3.txt"
}

def print_menu() -> None:
    """Display menu options."""
    print("\nSparse Matrix Operations")
    print("1. Add matrices")
    print("2. Subtract matrices")
    print("3. Multiply matrices")
    print("4. Display matrix statistics")
    print("5. Exit")
    print("Enter your choice: ", end="")

def print_file_selection() -> None:
    """Display available matrix files."""
    print("\nAvailable matrix files:")
    for key, path in SAMPLE_FILES.items():
        print(f"{key}. {path}")
    print("Or enter full path for a different file")
    print("Your choice: ", end="")

def get_valid_filepath(prompt: str) -> str:
    """
    Get a valid file path from user input with quick selection options.
    
    Args:
        prompt (str): Message to display to user
        
    Returns:
        str: Valid file path
        
    Raises:
        KeyboardInterrupt: If user cancels input
    """
    while True:
        try:
            print(prompt)
            print_file_selection()
            user_input = input().strip()
            
            # Check if user selected a sample file
            if user_input in SAMPLE_FILES:
                file_path = SAMPLE_FILES[user_input]
            else:
                file_path = user_input

            if not file_path:
                print("Error: Please enter a file path or number.")
                continue
                
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
        matrix = SparseMatrix(file_path)
        print(f"Successfully loaded matrix: {matrix}")
        return matrix
        
    except (ValueError, FileNotFoundError) as e:
        print(f"Error loading matrix: {str(e)}")
        print("Please check that the file exists and has the correct format:")
        print("rows=<number>")
        print("cols=<number>")
        print("(row, col, value)")
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
        print(f"Matrix statistics:")
        display_matrix_statistics(matrix)
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
    print("\nLoading first matrix:")
    matrix1 = load_matrix("Select the first matrix file:")
    if matrix1 is None:
        return None
        
    # Load second matrix
    print("\nLoading second matrix:")
    matrix2 = load_matrix("Select the second matrix file:")
    if matrix2 is None:
        return None
        
    try:
        # Show matrix dimensions before operation
        print(f"\nOperation: {operation}")
        print(f"Matrix 1: {matrix1.rows}x{matrix1.cols}")
        print(f"Matrix 2: {matrix2.rows}x{matrix2.cols}")
        
        # Perform requested operation
        if operation == "addition":
            if matrix1.rows != matrix2.rows or matrix1.cols != matrix2.cols:
                print(f"Error: Matrices cannot be added because their dimensions don't match.")
                print(f"Matrix 1 is {matrix1.rows}x{matrix1.cols}")
                print(f"Matrix 2 is {matrix2.rows}x{matrix2.cols}")
                print("Both matrices must have the same dimensions for addition.")
                return None
            return matrix1.add(matrix2)
            
        elif operation == "subtraction":
            if matrix1.rows != matrix2.rows or matrix1.cols != matrix2.cols:
                print(f"Error: Matrices cannot be subtracted because their dimensions don't match.")
                print(f"Matrix 1 is {matrix1.rows}x{matrix1.cols}")
                print(f"Matrix 2 is {matrix2.rows}x{matrix2.cols}")
                print("Both matrices must have the same dimensions for subtraction.")
                return None
            return matrix1.subtract(matrix2)
            
        elif operation == "multiplication":
            if matrix1.cols != matrix2.rows:
                print(f"Error: Matrices cannot be multiplied because dimensions are incompatible.")
                print(f"Matrix 1 is {matrix1.rows}x{matrix1.cols}")
                print(f"Matrix 2 is {matrix2.rows}x{matrix2.cols}")
                print("The number of columns in Matrix 1 must equal the number of rows in Matrix 2.")
                return None
            return matrix1.multiply(matrix2)
            
    except ValueError as e:
        print(f"Error performing {operation}: {str(e)}")
    except Exception as e:
        print(f"Unexpected error during {operation}: {str(e)}")
    
    return None

def main() -> None:
    """Main program loop."""
    print("Sparse Matrix Calculator")
    print("Author: Miranics")
    print("Date: 2025-02-19 12:19:22")
    
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
                matrix = load_matrix("Select matrix file for statistics:")
                if matrix:
                    display_matrix_statistics(matrix)
                    
            elif choice == '5':
                print("Thank you for using Sparse Matrix Calculator!")
                break
                
            else:
                print("Invalid choice! Please enter a number between 1 and 5.")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()