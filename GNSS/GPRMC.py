def parse_gprmc_sentence(sentence):
    if not sentence.startswith("$GPRMC"):
        raise ValueError("Not a GPRMC NMEA sentence")
    
    # Remove the prefix and the checksum
    data_part = sentence[7:].split('*')[0]  # Remove '$GPRMC,' and data after '*'
    checksum_provided = sentence.split('*')[1].strip().split('\r')[0]  # Extract checksum part

    # Split the sentence into fields
    fields = data_part.split(',')
    
    if len(fields) < 9:
        raise ValueError("Incomplete GPRMC sentence")
    
    # Extract fields
    time_utc = fields[0]
    status = fields[1]
    latitude = fields[2]
    lat_direction = fields[3]
    longitude = fields[4]
    lon_direction = fields[5]
    speed_knots = fields[6]
    course_degrees = fields[7]
    date = fields[8]
    mode_indicator = fields[9] if len(fields) > 9 else ''
    
    # Calculate checksum
    checksum_calculated = 0
    for char in sentence[1:sentence.find('*')]:  # Calculate checksum over the data part before '*'
        checksum_calculated ^= ord(char)
    
    # Convert checksum to hexadecimal
    checksum_calculated_hex = format(checksum_calculated, '02X')
    
    # Print extracted data
    print(f"Time (UTC): {time_utc}")
    print(f"Status: {status}")
    print(f"Latitude: {latitude} {lat_direction}")
    print(f"Longitude: {longitude} {lon_direction}")
    print(f"Speed over Ground (knots): {speed_knots}")
    print(f"Course over Ground (degrees): {course_degrees}")
    print(f"Date: {date}")
    print(f"Mode Indicator: {mode_indicator}")
    
    # Validate checksum
    if checksum_provided == checksum_calculated_hex:
        print("Checksum validation passed.")
    else:
        print(f"Checksum validation failed. Calculated: {checksum_calculated_hex}, Provided: {checksum_provided}")

# Example sentence
nmea_sentence = "$GPRMC,151227.3997,A,4723.5403567,N,00826.8867153,E,0.00000,81.6172,111022,,,R*4F\r\n"
parse_gprmc_sentence(nmea_sentence)
