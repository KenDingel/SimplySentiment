# Open the input file for reading
with open('Transcript.txt', 'r') as input_file:
    # Create a new file for writing
    with open('output.txt', 'w') as output_file:
        # Read each line in the input file
        for line in input_file:
            # Split the line by ':' and take the text after the last colon
            parts = line.rsplit(':', 1)
            if len(parts) >= 2:
                second_half = parts[1]
            else:
                second_half = ""
            
            # Write the second half to the output file
            output_file.write(second_half)
