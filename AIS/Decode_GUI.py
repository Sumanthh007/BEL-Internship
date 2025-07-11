import tkinter as tk
from tkinter import messagebox

def nmea_to_binary(payload):
    # AIS encoding table, each character is mapped to its 6-bit binary representation
    six_bit_ascii = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, ':': 10, ';': 11, '<': 12, '=': 13, '>': 14, '?': 15,
        '@': 16, 'A': 17, 'B': 18, 'C': 19, 'D': 20, 'E': 21, 'F': 22, 'G': 23,
        'H': 24, 'I': 25, 'J': 26, 'K': 27, 'L': 28, 'M': 29, 'N': 30, 'O': 31,
        'P': 32, 'Q': 33, 'R': 34, 'S': 35, 'T': 36, 'U': 37, 'V': 38, 'W': 39,
        '`': 40, 'a': 41, 'b': 42, 'c': 43, 'd': 44, 'e': 45, 'f': 46, 'g': 47,
        'h': 48, 'i': 49, 'j': 50, 'k': 51, 'l': 52, 'm': 53, 'n': 54, 'o': 55,
        'p': 56, 'q': 57, 'r': 58, 's': 59, 't': 60, 'u': 61, 'v': 62, 'w': 63
    }

    binary_str = ''
    for char in payload:
        value = six_bit_ascii[char]
        binary_str += f'{value:06b}'  # Convert to 6-bit binary

    return binary_str

def decode_ais_position_report(binary_str):
    # Extracting fields based on AIS message type 1, 2, or 3 (position reports)
    message_type = int(binary_str[0:6], 2)
    repeat_indicator = int(binary_str[6:8], 2)
    mmsi = int(binary_str[8:38], 2)
    navigational_status = int(binary_str[38:42], 2)
    rate_of_turn = int(binary_str[42:50], 2)
    speed_over_ground = int(binary_str[50:60], 2) / 10
    position_accuracy = int(binary_str[60:61], 2)

    longitude = int(binary_str[61:89], 2)
    latitude = int(binary_str[89:116], 2)
     # Longitude is encoded in the range -180 to 180 degrees
    if longitude & (1 << 27):  # Check if the sign bit (bit 27) is set
        longitude -= (1 << 28)  # Adjust for negative values
    longitude = longitude / 600000  # Convert from 1/600000 degree to degrees
    
    # Latitude is encoded in the range -90 to 90 degrees
    if latitude & (1 << 26):  # Check if the sign bit (bit 26) is set
        latitude -= (1 << 27)  # Adjust for negative values
    latitude = latitude / 600000  # Convert from 1/600000 degree to degrees

    course_over_ground = int(binary_str[116:128], 2) / 10
    true_heading = int(binary_str[128:137], 2)
    timestamp = int(binary_str[137:143], 2)

    # Return a dictionary of decoded fields
    return {
        'message_type': message_type,
        'repeat_indicator': repeat_indicator,
        'mmsi': mmsi,
        'navigational_status': navigational_status,
        'rate_of_turn': rate_of_turn,
        'speed_over_ground': speed_over_ground,
        'position_accuracy': position_accuracy,
        'longitude': longitude,
        'latitude': latitude,
        'course_over_ground': course_over_ground,
        'true_heading': true_heading,
        'timestamp': timestamp
    }

def decode_nmea():
    nmea_message = nmea_entry.get()

    try:
        # Extracting the payload from the NMEA message
        payload = nmea_message.split(',')[5]
        
        # Convert payload to binary
        binary_payload = nmea_to_binary(payload)

        # Decode the binary AIS message
        decoded_message = decode_ais_position_report(binary_payload)

        # Display the decoded message
        result_text.delete(1.0, tk.END)
        for key, value in decoded_message.items():
            result_text.insert(tk.END, f'{key}: {value}\n')

    except Exception as e:
        messagebox.showerror("Error", f"Failed to decode NMEA message: {e}")

# Create the main window
root = tk.Tk()
root.title("AIS Decoder")

# Create input fields and buttons
nmea_label = tk.Label(root, text="Enter NMEA Message:")
nmea_label.pack()

nmea_entry = tk.Entry(root, width=50)
nmea_entry.pack()

decode_button = tk.Button(root, text="Decode", command=decode_nmea)
decode_button.pack()

result_text = tk.Text(root, height=15, width=60)
result_text.pack()

# Run the main loop
root.mainloop()
