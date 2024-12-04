import os
import math

# Configuration Variables
max_distance = 2000000  # Max pen distance before splitting, in millimeters
pen_down_command = "S0"  # Example pen down command
pen_up_command = "S20"   # Example pen up command
gcode_file = "rock_key.gcode"  # Replace with your G-code file path
return_to_home_on_pen_change = True  # Set to True to return to home for pen changes, False to stay in place
home_position = (0, 0)  # Define home position as (X, Y)

def parse_gcode(file_path, max_distance, pen_down_command, pen_up_command, return_to_home, home_position):
    # Read the G-code file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Initialize variables
    output_files = []
    current_file_lines = []
    header_lines = []
    cumulative_distance = 0
    last_position = None  # (x, y)
    pen_is_down = False
    file_index = 1
    units = "mm"  # Default to millimeters

    # Extract header lines (G21, G90, and G1 F####)
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("G21") or stripped.startswith("G90") or stripped.startswith("G1 F"):
            header_lines.append(line)
        # Stop extracting header when commands begin
        if stripped.startswith("G1") and "F" not in stripped:
            break

    def save_current_file():
        nonlocal current_file_lines, file_index, last_position, pen_is_down
        # Create the new filename with the order number at the end
        output_path = f"{os.path.splitext(file_path)[0]}_{file_index}.gcode"
        
        # Add header lines to the file
        with open(output_path, 'w') as output_file:
            output_file.writelines(header_lines)
            # Add commands to return to home if enabled
            if return_to_home and last_position is not None:
                # Raise pen
                output_file.write(f"{pen_up_command}\n")
                # Move to home
                output_file.write(f"G1 X{home_position[0]} Y{home_position[1]}\n")
            # Write the rest of the file
            output_file.writelines(current_file_lines)
        
        output_files.append(output_path)
        file_index += 1
        current_file_lines = []

    def add_starting_commands():
        nonlocal current_file_lines, last_position, pen_is_down
        # Add commands to resume from home if enabled
        if return_to_home and last_position is not None:
            # Move to last position
            current_file_lines.append(f"G1 X{last_position[0]} Y{last_position[1]}\n")
            # Lower pen if it was down
            if pen_is_down:
                current_file_lines.append(f"{pen_down_command}\n")

    for line in lines:
        stripped = line.strip()
        
        # Detect units
        if stripped.startswith('G20'):
            units = "inches"
            current_file_lines.append(line)
            continue
        elif stripped.startswith('G21'):
            units = "mm"
            current_file_lines.append(line)
            continue

        # Check for pen down and pen up commands
        if stripped.startswith(pen_down_command):
            pen_is_down = True
            current_file_lines.append(line)
            continue
        elif stripped.startswith(pen_up_command):
            pen_is_down = False
            current_file_lines.append(line)
            continue

        # Process pen down movements only
        if pen_is_down and stripped.startswith('G1'):
            # Parse the G1 line to extract coordinates
            x, y = None, None
            for part in stripped.split():
                if part.startswith('X'):
                    x = float(part[1:])
                elif part.startswith('Y'):
                    y = float(part[1:])
            
            if x is not None and y is not None:
                if last_position is not None:
                    # Calculate distance between points
                    distance = math.sqrt((x - last_position[0])**2 + (y - last_position[1])**2)
                    
                    # Convert to consistent units if needed
                    if units == "inches":
                        distance *= 25.4  # Convert inches to mm
                    
                    cumulative_distance += distance

                    # If the max distance is exceeded, save the current file and start a new one
                    if cumulative_distance > max_distance:
                        save_current_file()
                        add_starting_commands()
                        cumulative_distance = 0
                
                last_position = (x, y)

        # Add the line to the current file
        current_file_lines.append(line)

    # Save the final file
    if current_file_lines:
        save_current_file()

    return output_files

if __name__ == "__main__":
    split_files = parse_gcode(
        gcode_file, 
        max_distance, 
        pen_down_command, 
        pen_up_command, 
        return_to_home_on_pen_change, 
        home_position
    )
    print(f"Split G-code files created in order: {split_files}")
