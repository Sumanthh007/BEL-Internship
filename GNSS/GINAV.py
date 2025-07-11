def parse_ginav_sentence(sentence):
    if not sentence.startswith("$GINAV"):
        raise ValueError("Not a GINAV NMEA sentence")
    
    # Remove the prefix and the checksum
    data_part = sentence[7:sentence.find('*')]  # Exclude '$GINAV,' and before '*'
    checksum_provided = sentence.split('*')[1].strip()  # Extract checksum part

    # Calculate checksum
    checksum_calculated = 0
    for char in data_part:
        checksum_calculated ^= ord(char)
    
    # Convert checksum to hexadecimal
    checksum_calculated_hex = format(checksum_calculated, '02X')
    
    # Split the sentence into fields
    fields = data_part.split(',')
    
    # Check if fields length matches expected length
    if len(fields) < 12:
        raise ValueError("Incomplete GINAV sentence")
    
    # Extract fields
    fix_quality = fields[0]
    year = fields[1]
    latitude = fields[2]
    lat_direction = fields[3]
    longitude = fields[4]
    lon_direction = fields[5]
    num_satellites = fields[6]
    hdop = fields[7]
    altitude = fields[8]
    altitude_units = fields[9]
    geoidal_separation = fields[10]
    geoidal_units = fields[11]
    
    # Print extracted data
    print(f"Fix Quality: {fix_quality}")
    print(f"Year: {year}")
    print(f"Latitude: {latitude} {lat_direction}")
    print(f"Longitude: {longitude} {lon_direction}")
    print(f"Number of Satellites: {num_satellites}")
    print(f"Horizontal Dilution of Precision (HDOP): {hdop}")
    print(f"Altitude: {altitude} {altitude_units}")
    print(f"Geoidal Separation: {geoidal_separation} {geoidal_units}")
    
    # Validate checksum
    if checksum_provided == checksum_calculated_hex:
        print("Checksum validation passed.")
    else:
        print(f"Checksum validation failed. Calculated: {checksum_calculated_hex}, Provided: {checksum_provided}")

# Example sentence
nmea_sentence = "$GINAV,1,2024,19.0760,N,72.8777,E,15,1.0,7.5,M,-34.0,M,,*7C\r\n"
parse_ginav_sentence(nmea_sentence)
