def remove_duplicates(input_file, output_file):
    lines_seen = set()  # Set to store unique lines
    unique_lines = []

    with open(input_file, "r") as infile:
        for line in infile:
            if line not in lines_seen and not " " in line:
                lines_seen.add(line)
                unique_lines.append(line.capitalize())

    unique_lines.sort()  # Sort the unique lines

    with open(output_file, "w") as outfile:
        for line in unique_lines:
            outfile.write(line)


if __name__ == "__main__":
    input_filename = "resources.txt"  # Change this to your input file
    output_filename = input_filename  # Change this to your desired output file

    remove_duplicates(input_filename, output_filename)
