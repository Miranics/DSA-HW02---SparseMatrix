"""
Sparse Matrix Calculator
------------------------
A program to perform operations on sparse matrices.

Author: Nanen Miracle Mbanaade
Last update: 2025-02-19 13:11
"""

from sparse_matrix import SparseMatrix
from typing import Optional, Tuple, List
import os
import sys
from datetime import datetime

# my sample matrix files! 📁
SAMPLE_FILES = [
    "../../sample_inputs/matrix1.txt",
    "../../sample_inputs/matrix2.txt",
    "../../sample_inputs/matrix3.txt"
]

# Where I save my results 💾
RESULTS_DIR = "../../results"

def ensure_results_directory():
    """Create results directory if it doesn't exist. 📁✨"""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"\nCreated results directory at {RESULTS_DIR}")

def print_menu() -> None:
    """Show what we can do! 🎯"""
    print("\n" + "=" * 40)
    print("🔢 Sparse Matrix Calculator 🔢")
    print("=" * 40)
    print("1. ➕ Add matrices")
    print("2. ➖ Subtract matrices")
    print("3. ✖️  Multiply matrices")
    print("4. 📊 Display matrix statistics")
    print("5. 👋 Exit")
    print("=" * 40)
    print("Enter your choice: ", end="")

def list_sample_files() -> None:
    """Show available matrix files. 📂"""
    print("\n📂 Available sample files:")
    for i, file_path in enumerate(SAMPLE_FILES, 1):
        status = "✅" if os.path.exists(file_path) else "❌"
        print(f"{i}. {status} {file_path}")
    print("\n💡 Tip: Enter 1-3 for sample files or type a full path")

def get_file_choice(prompt: str) -> str:
    """
    Get file choice from user - made super friendly! 😊
    
    Args:
        prompt (str): What to ask the user
        
    Returns:
        str: The chosen file path
    """
    while True:
        list_sample_files()
        print(f"\n{prompt}")
        choice = input("Your choice: ").strip()
        
        # Check if user picked a sample file
        if choice.isdigit() and 1 <= int(choice) <= len(SAMPLE_FILES):
            file_path = SAMPLE_FILES[int(choice) - 1]
        else:
            file_path = choice
            
        if os.path.isfile(file_path):
            return file_path
            
        print(f"\n❌ Oops! File '{file_path}' not found.")
        print("Please try again with a valid file number or path.")

def load_matrix(prompt: str) -> Optional[SparseMatrix]:
    """
    Load a matrix - with helpful error messages! 🎯
    
    Args:
        prompt (str): What to ask the user
        
    Returns:
        Optional[SparseMatrix]: The loaded matrix (or None if something went wrong)
    """
    try:
        file_path = get_file_choice(prompt)
        matrix = SparseMatrix(file_path)
        print(f"\n✅ Successfully loaded: {matrix}")
        return matrix
        
    except (ValueError, FileNotFoundError) as e:
        print(f"\n❌ Couldn't load matrix: {str(e)}")
        print("\n📝 The file should look like this:")
        print("rows=<number>")
        print("cols=<number>")
        print("(row, col, value)")
        return None
        
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled")
        return None
        
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        return None

def save_result(matrix: SparseMatrix, operation: str) -> bool:
    """
    Save our result - now in a nice results folder! 📁
    
    Args:
        matrix (SparseMatrix): Matrix to save
        operation (str): What we did (add/subtract/multiply)
        
    Returns:
        bool: True if save worked, False if something went wrong
    """
    try:
        # Making sure i have a results directory
        ensure_results_directory()
        
        # Create a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"result_{operation}_{timestamp}.txt"
        output_path = os.path.join(RESULTS_DIR, filename)
        
        # Save the file
        matrix.save_to_file(output_path)
        print(f"\n💾 Result saved to: {filename}")
        
        # Show some stats
        print("\n📊 Result Statistics:")
        display_matrix_statistics(matrix)
        return True
        
    except IOError as e:
        print(f"\n❌ Couldn't save result: {str(e)}")
        return False
        
    except Exception as e:
        print(f"\n💥 Unexpected error while saving: {str(e)}")
        return False

def display_matrix_statistics(matrix: SparseMatrix) -> None:
    """Show interesting facts about our matrix! 📊"""
    stats = matrix.get_statistics()
    print("\n📊 Matrix Statistics:")
    print(f"📏 Size: {stats['dimensions'][0]} x {stats['dimensions'][1]}")
    print(f"🔢 Non-zero elements: {stats['non_zero_elements']}")
    print(f"💯 Total elements: {stats['total_elements']}")
    print(f"📈 Density: {stats['density']:.4%}")
    if stats['min_value'] is not None:
        print(f"⬇️  Minimum value: {stats['min_value']}")
        print(f"⬆️  Maximum value: {stats['max_value']}")

def perform_operation(operation: str) -> Optional[SparseMatrix]:
    """
    Do the matrix math! ✨
    
    Args:
        operation (str): What we're doing (add/subtract/multiply)
        
    Returns:
        Optional[SparseMatrix]: The result (or None if something went wrong)
    """
    # Loading my  matrices
    print("\n🔍 Loading first matrix:")
    matrix1 = load_matrix("Pick the first matrix:")
    if matrix1 is None:
        return None
        
    print("\n🔍 Loading second matrix:")
    matrix2 = load_matrix("Pick the second matrix:")
    if matrix2 is None:
        return None
        
    try:
        # Show what i'm working with
        print(f"\n🎯 Operation: {operation}")
        print(f"📌 Matrix 1: {matrix1}")
        print(f"📌 Matrix 2: {matrix2}")
        
        #Now doing the math!
        if operation == "addition":
            if matrix1.rows != matrix2.rows or matrix1.cols != matrix2.cols:
                print(f"\n❌ Can't add these matrices - sizes don't match!")
                print(f"Matrix 1 is {matrix1.rows}x{matrix1.cols}")
                print(f"Matrix 2 is {matrix2.rows}x{matrix2.cols}")
                print("They need to be the same size for addition.")
                return None
            return matrix1.add(matrix2)
            
        elif operation == "subtraction":
            if matrix1.rows != matrix2.rows or matrix1.cols != matrix2.cols:
                print(f"\n❌ Can't subtract these matrices - sizes don't match!")
                print(f"Matrix 1 is {matrix1.rows}x{matrix1.cols}")
                print(f"Matrix 2 is {matrix2.rows}x{matrix2.cols}")
                print("They need to be the same size for subtraction.")
                return None
            return matrix1.subtract(matrix2)
            
        elif operation == "multiplication":
            if matrix1.cols != matrix2.rows:
                print(f"\n❌ Can't multiply these matrices - sizes don't work!")
                print(f"Matrix 1 is {matrix1.rows}x{matrix1.cols}")
                print(f"Matrix 2 is {matrix2.rows}x{matrix2.cols}")
                print("The columns of Matrix 1 must match the rows of Matrix 2.")
                return None
            return matrix1.multiply(matrix2)
            
    except ValueError as e:
        print(f"\n❌ Error during {operation}: {str(e)}")
    except Exception as e:
        print(f"\n💥 Unexpected error during {operation}: {str(e)}")
    
    return None

def main() -> None:
    """Let's get calculating! 🚀"""
    print("🎉 Welcome to Sparse Matrix Calculator! 🎉")
    print("Made with ❤️  by Miracle")
    print("Last updated: 2025-02-19 13:11:24")
    
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
                matrix = load_matrix("Pick a matrix to analyze:")
                if matrix:
                    display_matrix_statistics(matrix)
                    
            elif choice == '5':
                print("\n👋 Thanks for using Sparse Matrix Calculator!")
                print("Hope to see you again soon! ✨")
                break
                
            else:
                print("\n❌ Oops! Please enter a number between 1 and 5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using Sparse Matrix Calculator!")
            break
        except Exception as e:
            print(f"\n💥 Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()