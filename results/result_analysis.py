# Write a Pthon script that takes all files starting with output and ending with .txt in the current directory, and for each file, it reads the content and 
# #extracts the third column (Circuit Length) from each line (ignoring the header). 
# It then computes the average of these values for each file, the standard deviation, the minimum, and the median. In this process only consider rows having
# the second column (Best Fitness) greater or equal to 1.0. Finally, print for each file the number of rows having Best Fitness < 1.0


import os
import glob
import pandas as pd
import numpy as np
import statistics

def analyze_output_files():
    """
    Analyze all output*.txt files in the current directory.
    Extract circuit length statistics for rows with Best Fitness >= 1.0
    """

    # Find all files starting with "output" and ending with ".txt"
    files = glob.glob("output*.txt")

    if not files:
        print("No files matching 'output*.txt' found in the current directory.")
        return

    print("ðŸ“Š ANALYZING OUTPUT FILES")
    print("=" * 60)

    for filename in sorted(files):
        print(f"\nFile: {filename}")
        print("-" * 40)

        try:
            # Read the file
            with open(filename, 'r') as f:
                lines = f.readlines()

            if not lines:
                print("File is empty")
                continue

            # Parse the data
            data = []
            header_found = False

            for line_num, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue

                # Skip header line (assume first non-empty line is header)
                if not header_found:
                    header_found = True
                    print(f"Header: {line}")
                    continue

                # Split by whitespace or comma
                parts = line.replace(',', ' ').split()

                if len(parts) < 3:
                    print(f"Line {line_num + 1} has insufficient columns: {line}")
                    continue

                try:
                    # Extract columns: assume format is [col1, best_fitness, circuit_length, ...]
                    best_fitness = float(parts[1])
                    circuit_length = int(parts[2])
                    data.append((best_fitness, circuit_length))

                except (ValueError, IndexError) as e:
                    print(f"Line {line_num + 1} parsing error: {line} ({e})")
                    continue

            if not data:
                print("No valid data found")
                continue

            # Separate data based on fitness criteria
            perfect_solutions = [(bf, cl) for bf, cl in data if bf >= 1.0]
            imperfect_solutions = [(bf, cl) for bf, cl in data if bf < 1.0]

            print(f"Total rows processed: {len(data)}")
            print(f"Rows with Best Fitness >= 1.0: {len(perfect_solutions)}")
            print(f"Rows with Best Fitness < 1.0: {len(imperfect_solutions)}")

            if perfect_solutions:
                # Extract circuit lengths for perfect solutions
                circuit_lengths = [cl for bf, cl in perfect_solutions]

                # Calculate statistics
                avg_length = np.mean(circuit_lengths)
                std_length = np.std(circuit_lengths, ddof=1) if len(circuit_lengths) > 1 else 0.0
                min_length = min(circuit_lengths)
                median_length = statistics.median(circuit_lengths)
                max_length = max(circuit_lengths)

                print(f"\nCIRCUIT LENGTH STATISTICS (Best Fitness >= 1.0):")
                print(f"   Average:        {avg_length:.2f}")
                print(f"   Standard Dev:   {std_length:.2f}")
                print(f"   Minimum:        {min_length}")
                print(f"   Median:         {median_length}")
                print(f"   Maximum:        {max_length}")

                # Show distribution
                """
                unique_lengths = sorted(set(circuit_lengths))
                print(f"\nLength Distribution:")
                for length in unique_lengths:
                    count = circuit_lengths.count(length)
                    percentage = (count / len(circuit_lengths)) * 100
                    print(f"   Length {length}: {count} times ({percentage:.1f}%)")
                """
            else:
                print("\nNo perfect solutions (Best Fitness >= 1.0) found")

        except Exception as e:
            print(f"\nError processing {filename}: {e}")

    print(f"\nAnalysis complete!")

if __name__ == "__main__":
    analyze_output_files()