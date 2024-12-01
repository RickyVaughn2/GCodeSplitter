# GCodeSplitter

**GCodeSplitter** is a lightweight and versatile tool designed to optimize G-code files for drawbots and similar CNC devices. It splits large G-code drawings into smaller, manageable segments based on user-defined limits, ensuring seamless pen changes and uninterrupted drawing operations.

---

## Features

- **Customizable Pen Limits**: Set a maximum drawing distance to avoid running out of ink mid-drawing.
- **Optional Pen Change Behavior**:
  - Stay in place for a manual pen change.
  - Automatically return to a configurable home position for easier pen replacement and resume drawing precisely where it left off.
- **Flexible Home Position**: Define the home coordinates to suit your workspace layout.
- **Support for Multiple Units**: Automatically detects and adjusts for millimeters (default) or inches in G-code files.
- **Sequential File Output**: Splits files into sequentially numbered segments (e.g., `drawing_1.gcode`, `drawing_2.gcode`), making it easy to execute in order.
- **Lightweight and Fast**: Process G-code files efficiently without unnecessary overhead.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/GCodeSplitter.git
   cd GCodeSplitter
   ```

2. Ensure you have Python 3.6 or higher installed.

3. Run the script directly:
   ```bash
   python GCodeSplitter.py
   ```

---

## Usage

1. Place your G-code file in the project directory.
2. Open the script and configure the following variables at the top:
   - **`max_distance`**: Maximum drawing distance (in millimeters) before splitting the file.
   - **`pen_down_command`**: G-code command that lowers the pen (e.g., `S0`).
   - **`pen_up_command`**: G-code command that raises the pen (e.g., `S20`).
   - **`return_to_home_on_pen_change`**: Set to `True` to return to a home position during pen changes, or `False` to remain in place.
   - **`home_position`**: The (X, Y) coordinates for the home position (default: `(0, 0)`).
3. Run the script:
   ```bash
   python GCodeSplitter.py
   ```
4. The program will output split files named sequentially (e.g., `rock_key_1.gcode`, `rock_key_2.gcode`, etc.).

---

## Example Configuration

```python
max_distance = 2000000  # Maximum pen distance in millimeters
pen_down_command = "S0"  # Command to lower the pen
pen_up_command = "S20"   # Command to raise the pen
gcode_file = "rock_key.gcode"  # Path to your G-code file
return_to_home_on_pen_change = True  # Set to True for home return, False to stay in place
home_position = (0, 0)  # Home position coordinates
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance GCodeSplitter.

---

## Contact

For questions, feedback, or suggestions, feel free to reach out to [your email or GitHub profile].
