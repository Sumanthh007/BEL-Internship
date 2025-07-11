def sixbit_to_binary(payload):
    """Convert 6-bit AIS payload to binary."""
    sixbit_map = "0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW`abcdefghijklmnopqrstuvw"
    binary_string = ""
    
    for char in payload:
        index = sixbit_map.index(char)
        binary_string += format(index, '06b')
        
    return binary_string

def decode_position_report(binary_data):
    """Decode AIS position report (Types 1, 2, 3)."""
    mmsi = int(binary_data[8:38], 2)
    longitude = int(binary_data[61:89], 2) / 600000.0
    latitude = int(binary_data[89:116], 2) / 600000.0
    speed_over_ground = int(binary_data[50:60], 2) / 10.0
    course_over_ground = int(binary_data[116:128], 2) / 10.0
    true_heading = int(binary_data[128:137], 2)

    return {
        "message_type": int(binary_data[0:6], 2),
        "mmsi": mmsi,
        "longitude": longitude,
        "latitude": latitude,
        "speed_over_ground": speed_over_ground,
        "course_over_ground": course_over_ground,
        "true_heading": true_heading,
    }


def decode_static_voyage_data(binary_data):
    """Decode Static and Voyage Related Data (Type 5)."""
    try:
        # Ensure binary data is long enough (424 bits)
        if len(binary_data) < 424:
            raise ValueError(f"Binary data is too short: {len(binary_data)} bits (expected 424 bits)")
        
        # Decode MMSI (Maritime Mobile Service Identity)
        mmsi = int(binary_data[8:38], 2)
        
        # Decode IMO number (International Maritime Organization number)
        imo_number = int(binary_data[40:70], 2)
        
        # Decode Call Sign
        call_sign = "".join([chr(int(binary_data[i:i + 6], 2) + 64) for i in range(70, 112, 6)]).strip()
        
        # Decode Ship Name
        ship_name = "".join([chr(int(binary_data[i:i + 6], 2) + 64) for i in range(112, 232, 6)]).strip()
        
        # Decode Destination
        destination = "".join([chr(int(binary_data[i:i + 6], 2) + 64) for i in range(302, 422, 6)]).strip()

        # Return decoded information as a dictionary
        return {
            "message_type": int(binary_data[0:6], 2),
            "mmsi": mmsi,
            "imo_number": imo_number,
            "call_sign": call_sign,
            "ship_name": ship_name,
            "destination": destination,
        }
    except ValueError as ve:
        print(f"Error decoding static voyage data: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred while decoding: {e}")
        return None


def decode_base_station_report(binary_data):
    """Decode Base Station Report (Type 4)."""
    mmsi = int(binary_data[8:38], 2)
    utc_year = int(binary_data[38:52], 2)
    utc_month = int(binary_data[52:56], 2)
    utc_day = int(binary_data[56:61], 2)
    utc_hour = int(binary_data[61:66], 2)
    utc_minute = int(binary_data[66:72], 2)
    utc_second = int(binary_data[72:78], 2)
    longitude = int(binary_data[79:107], 2) / 600000.0
    latitude = int(binary_data[107:134], 2) / 600000.0

    return {
        "message_type": int(binary_data[0:6], 2),
        "mmsi": mmsi,
        "utc_time": f"{utc_year}-{utc_month:02d}-{utc_day:02d} {utc_hour:02d}:{utc_minute:02d}:{utc_second:02d}",
        "longitude": longitude,
        "latitude": latitude,
    }


def decode_binary_addressed(binary_data):
    """Decode Binary Addressed Message (Type 6)."""
    mmsi = int(binary_data[8:38], 2)
    seq_num = int(binary_data[38:40], 2)
    destination_mmsi = int(binary_data[40:70], 2)
    retransmit_flag = int(binary_data[70], 2)
    spare = int(binary_data[71:72], 2)
    application_id = int(binary_data[72:88], 2)

    return {
        "message_type": int(binary_data[0:6], 2),
        "mmsi": mmsi,
        "sequence_number": seq_num,
        "destination_mmsi": destination_mmsi,
        "retransmit_flag": retransmit_flag,
        "application_id": application_id
    }

def decode_binary_acknowledge(binary_data):
    """Decode Binary Acknowledge (Type 7)."""
    try:
        # AIS Type 7 message has a fixed length of 88 bits
        if len(binary_data) < 88:
            raise ValueError("Binary data is too short: expected at least 88 bits")

        # Extract MMSI and sequence numbers from the binary data
        mmsi_1 = int(binary_data[8:38], 2)
        sequence_number_1 = int(binary_data[40:48], 2)
        mmsi_2 = int(binary_data[48:78], 2)
        sequence_number_2 = int(binary_data[80:88], 2)

        return {
            "message_type": 7,
            "mmsi_1": mmsi_1,
            "sequence_number_1": sequence_number_1,
            "mmsi_2": mmsi_2,
            "sequence_number_2": sequence_number_2,
        }

    except Exception as e:
        print(f"Error decoding binary acknowledge: {e}")
        return None
    

def decode_binary_broadcast(binary_data):
    """Decode Binary Broadcast Message (Type 8)."""
    mmsi = int(binary_data[8:38], 2)
    application_id = int(binary_data[40:56], 2)

    return {
        "message_type": int(binary_data[0:6], 2),
        "mmsi": mmsi,
        "application_id": application_id
    }


def decode_sar_aircraft_position(binary_data):
    """Decode Standard SAR Aircraft Position Report (Type 9)."""
    mmsi = int(binary_data[8:38], 2)
    altitude = int(binary_data[38:50], 2)
    speed_over_ground = int(binary_data[50:60], 2) / 10.0
    longitude = int(binary_data[61:89], 2) / 600000.0
    latitude = int(binary_data[89:116], 2) / 600000.0
    course_over_ground = int(binary_data[116:128], 2) / 10.0
    true_heading = int(binary_data[128:137], 2)

    return {
        "message_type": int(binary_data[0:6], 2),
        "mmsi": mmsi,
        "altitude": altitude,
        "longitude": longitude,
        "latitude": latitude,
        "speed_over_ground": speed_over_ground,
        "course_over_ground": course_over_ground,
        "true_heading": true_heading,
    }


def decode_utc_date_inquiry(binary_data):
    """Decode UTC and Date Inquiry (Type 10)."""
    mmsi = int(binary_data[8:38], 2)

    return {
        "message_type": int(binary_data[0:6], 2),
        "mmsi": mmsi
    }


def decode_addressed_safety(binary_data):
    """Decode Addressed Safety-Related Message (Type 12)."""
    mmsi = int(binary_data[8:38], 2)
    seq_num = int(binary_data[38:40], 2)
    destination_mmsi = int(binary_data[40:70], 2)
    retransmit_flag = int(binary_data[70], 2)

    return {
        "message_type": int(binary_data[0:6], 2),
        "mmsi": mmsi,
        "sequence_number": seq_num,
        "destination_mmsi": destination_mmsi,
        "retransmit_flag": retransmit_flag
    }


def decode_interrogation(binary_data):
    """Decode Interrogation (Type 15)."""
    mmsi = int(binary_data[8:38], 2)
    interrogated_mmsi = int(binary_data[40:70], 2)

    return {
        "message_type": int(binary_data[0:6], 2),
        "mmsi": mmsi,
        "interrogated_mmsi": interrogated_mmsi
    }


def decode_static_data_report(binary_data):
    """Decode Static Data Report (Type 24)."""
    mmsi = int(binary_data[8:38], 2)
    part_number = int(binary_data[38:40], 2)

    if part_number == 0:
        vessel_name = "".join([chr(int(binary_data[i:i + 6], 2) + 64) for i in range(40, 160, 6)]).strip()
        return {
            "message_type": int(binary_data[0:6], 2),
            "mmsi": mmsi,
            "vessel_name": vessel_name
        }
    else:
        ship_type = int(binary_data[40:48], 2)
        vendor_id = "".join([chr(int(binary_data[i:i + 6], 2) + 64) for i in range(48, 90, 6)]).strip()
        return {
            "message_type": int(binary_data[0:6], 2),
            "mmsi": mmsi,
            "ship_type": ship_type,
            "vendor_id": vendor_id
        }

def decode_base_station_report_utc(binary_data):
    """Decode UTC and Date Response (Type 11)."""
    mmsi = int(binary_data[8:38], 2)
    utc_year = int(binary_data[38:52], 2)
    utc_month = int(binary_data[52:56], 2)
    utc_day = int(binary_data[56:61], 2)
    utc_hour = int(binary_data[61:66], 2)
    utc_minute = int(binary_data[66:72], 2)
    utc_second = int(binary_data[72:78], 2)
    longitude = int(binary_data[79:107], 2) / 600000.0
    latitude = int(binary_data[107:134], 2) / 600000.0

    return {
        "message_type": 11,
        "mmsi": mmsi,
        "utc_time": f"{utc_year}-{utc_month:02d}-{utc_day:02d} {utc_hour:02d}:{utc_minute:02d}:{utc_second:02d}",
        "longitude": longitude,
        "latitude": latitude,
    }


def decode_safety_broadcast(binary_data):
    """Decode Safety Broadcast Message (Type 14)."""
    mmsi = int(binary_data[8:38], 2)
    safety_text = "".join([chr(int(binary_data[i:i + 6], 2)) for i in range(40, len(binary_data), 6)]).strip()

    return {
        "message_type": 14,
        "mmsi": mmsi,
        "safety_text": safety_text
    }


def decode_acknowledge(binary_data):
    """Decode Binary Acknowledge Message (Type 13)."""
    mmsi = int(binary_data[8:38], 2)
    dest_mmsi1 = int(binary_data[40:70], 2)

    return {
        "message_type": 13,
        "mmsi": mmsi,
        "acknowledged_mmsi": dest_mmsi1
    }


def decode_assignment(binary_data):
    """Decode Assignment Mode Command (Type 16)."""
    mmsi = int(binary_data[8:38], 2)
    assigned_mmsi1 = int(binary_data[40:70], 2)

    return {
        "message_type": 16,
        "mmsi": mmsi,
        "assigned_mmsi_1": assigned_mmsi1
    }


def decode_dgnss_binary(binary_data):
    """Decode DGNSS Binary Broadcast (Type 17)."""
    mmsi = int(binary_data[8:38], 2)
    longitude = int(binary_data[40:61], 2) / 600
    latitude = int(binary_data[61:82], 2) / 600

    return {
        "message_type": 17,
        "mmsi": mmsi,
        "longitude": longitude,
        "latitude": latitude
    }


def decode_gps_correction(binary_data):
    """Decode GPS Correction Report (Type 18)."""
    mmsi = int(binary_data[8:38], 2)
    longitude = int(binary_data[61:89], 2) / 600000.0
    latitude = int(binary_data[89:116], 2) / 600000.0
    speed_over_ground = int(binary_data[50:60], 2) / 10.0
    course_over_ground = int(binary_data[116:128], 2) / 10.0
    true_heading = int(binary_data[128:137], 2)

    return {
        "message_type": 18,
        "mmsi": mmsi,
        "longitude": longitude,
        "latitude": latitude,
        "speed_over_ground": speed_over_ground,
        "course_over_ground": course_over_ground,
        "true_heading": true_heading,
    }


def decode_cpa_warning(binary_data):
    """Decode CPA Warning (Type 19)."""
    mmsi = int(binary_data[8:38], 2)
    longitude = int(binary_data[61:89], 2) / 600000.0
    latitude = int(binary_data[89:116], 2) / 600000.0
    speed_over_ground = int(binary_data[50:60], 2) / 10.0
    course_over_ground = int(binary_data[116:128], 2) / 10.0

    return {
        "message_type": 19,
        "mmsi": mmsi,
        "longitude": longitude,
        "latitude": latitude,
        "speed_over_ground": speed_over_ground,
        "course_over_ground": course_over_ground,
    }


def decode_utc_inquiry(binary_data):
    """Decode UTC and Date Inquiry (Type 20)."""
    mmsi = int(binary_data[8:38], 2)
    utc_year = int(binary_data[38:52], 2)
    utc_month = int(binary_data[52:56], 2)
    utc_day = int(binary_data[56:61], 2)

    return {
        "message_type": 20,
        "mmsi": mmsi,
        "utc_date": f"{utc_year}-{utc_month:02d}-{utc_day:02d}"
    }


def decode_static_vessel(binary_data):
    """Decode Static Vessel Data (Type 21)."""
    mmsi = int(binary_data[8:38], 2)
    vessel_name = "".join([chr(int(binary_data[i:i + 6], 2) + 64) for i in range(40, 160, 6)]).strip()

    return {
        "message_type": 21,
        "mmsi": mmsi,
        "vessel_name": vessel_name
    }


def decode_single_slot(binary_data):
    """Decode Single Slot Binary Message (Type 23)."""
    mmsi = int(binary_data[8:38], 2)

    return {
        "message_type": 23,
        "mmsi": mmsi
    }
def decode_static_data_report(binary_data):
    """Decode Static Data Report (Type 24)."""
    mmsi = int(binary_data[8:38], 2)
    part_number = int(binary_data[38:40], 2)
    if part_number == 0:
        vessel_name = "".join([chr(int(binary_data[i:i + 6], 2)) for i in range(40, 160, 6)]).strip()
        return {
            "message_type": 24,
            "mmsi": mmsi,
            "part_number": part_number,
            "vessel_name": vessel_name
        }
    else:
        ship_type = int(binary_data[40:48], 2)
        vendor_id = "".join([chr(int(binary_data[i:i + 6], 2)) for i in range(48, 90, 6)]).strip()
        callsign = "".join([chr(int(binary_data[i:i + 6], 2)) for i in range(90, 132, 6)]).strip()
        return {
            "message_type": 24,
            "mmsi": mmsi,
            "part_number": part_number,
            "ship_type": ship_type,
            "vendor_id": vendor_id,
            "callsign": callsign
        }

def decode_single_slot_binary(binary_data):
    """Decode Single Slot Binary Message (Type 25)."""
    mmsi = int(binary_data[8:38], 2)
    application_identifier = int(binary_data[40:56], 2)
    data_payload = binary_data[56:]

    return {
        "message_type": 25,
        "mmsi": mmsi,
        "application_identifier": application_identifier,
        "data_payload": data_payload
    }

def decode_multiple_slot_binary(binary_data):
    """Decode Multiple Slot Binary Message (Type 26)."""
    mmsi = int(binary_data[8:38], 2)
    application_identifier = int(binary_data[40:56], 2)
    data_payload = binary_data[56:]

    return {
        "message_type": 26,
        "mmsi": mmsi,
        "application_identifier": application_identifier,
        "data_payload": data_payload
    }

def decode_long_range(binary_data):
    """Decode Long Range AIS Broadcast Message (Type 27)."""
    mmsi = int(binary_data[8:38], 2)
    position_accuracy = int(binary_data[38:39], 2)
    raim_flag = int(binary_data[39:40], 2)
    longitude = int(binary_data[40:59], 2) / 600.0
    latitude = int(binary_data[59:78], 2) / 600.0
    speed_over_ground = int(binary_data[78:85], 2) / 10.0
    course_over_ground = int(binary_data[85:94], 2) / 10.0
    gnss_position_status = int(binary_data[94:95], 2)

    return {
        "message_type": 27,
        "mmsi": mmsi,
        "position_accuracy": position_accuracy,
        "raim_flag": raim_flag,
        "longitude": longitude,
        "latitude": latitude,
        "speed_over_ground": speed_over_ground,
        "course_over_ground": course_over_ground,
        "gnss_position_status": gnss_position_status
    }

def decode_ais_message(nmea_message):
    """Decode AIS message manually without pyais."""
    try:
        # Split NMEA sentence and extract the payload (5th field in the sentence)
        fields = nmea_message.split(',')
        payload = fields[5]

        # Convert 6-bit encoded payload to binary
        binary_data = sixbit_to_binary(payload)

        # Decode message based on the message type
        message_type = int(binary_data[0:6], 2)

        if message_type in [1, 2, 3]:
            return decode_position_report(binary_data)
        elif message_type == 5:
            return decode_static_voyage_data(binary_data)
        elif message_type == 4:
            return decode_base_station_report(binary_data)
        elif message_type == 6:
            return decode_binary_addressed(binary_data)
        elif message_type == 8:
            return decode_binary_broadcast(binary_data)
        elif message_type == 7:
            return decode_binary_acknowledge(binary_data)
        elif message_type == 9:
            return decode_sar_aircraft_position(binary_data)
        elif message_type == 10:
            return decode_utc_date_inquiry(binary_data)
        elif message_type == 11:
            return decode_base_station_report_utc(binary_data)
        elif message_type == 12:
            return decode_addressed_safety(binary_data)
        elif message_type == 13:
            return decode_acknowledge(binary_data)
        elif message_type == 14:
            return decode_safety_broadcast(binary_data)
        elif message_type == 15:
            return decode_interrogation(binary_data)
        elif message_type == 16:
            return decode_assignment(binary_data)
        elif message_type == 17:
            return decode_dgnss_binary(binary_data)
        elif message_type == 18:
            return decode_gps_correction(binary_data)
        elif message_type == 19:
            return decode_cpa_warning(binary_data)
        elif message_type == 20:
            return decode_utc_inquiry(binary_data)
        elif message_type == 21:
            return decode_static_vessel(binary_data)
        elif message_type == 23:
            return decode_single_slot(binary_data)
        elif message_type == 24:
            return decode_static_data_report(binary_data)
        elif message_type == 25:
            return decode_single_slot_binary(binary_data)
        elif message_type == 26:
            return decode_multiple_slot_binary(binary_data)
        elif message_type == 27:
            return decode_long_range(binary_data)
        else:
            return f"Message type {message_type} not handled in this example."

    except Exception as e:
        return f"Error decoding message: {e}"

# Example Usage
nmea_sentences = [
    # Type 1, 2, or 3 - Position Report
    "!AIVDM,1,1,,B,15Mv`;P00R8GpFP<JLPT3?wP0D00,0*6C",  

    # Type 4 - Base Station Report
    "!AIVDM,1,1,,B,402P?v1vS13j@<:O<UQEqgvN0000,0*1F",  

    # Type 5 - Static and Voyage Related Data
    "!AIVDM,1,1,,A,13q5W0PP1fQEpJVO9V>pIVgp0D7k,0*66",  
    
    # Type 6 - Addressed Binary Message
    "!AIVDM,1,1,,A,64:Ijv00000H1K3o2Tf:a000,0*5C",

    # Type 7 - Binary Acknowledge
    "!AIVDM,1,1,,A,15Mw9g0P0L00C0>2>P;F@=0P00,0*1C",

    # Type 9 - Standard SAR Aircraft Position Report
    "!AIVDM,1,1,,A,902:P=B1w;fRRVRe2rh0,0*34",

    # Type 10 - UTC/Date Inquiry
    "!AIVDM,1,1,,A,A0SEbdP00000Mwj,0*27",

    # Type 11 - UTC/Date Response
    "!AIVDM,1,1,,B,B0E8A=B8=EBDF00M00G00000,0*48",

    # Type 18 - Standard Class B Equipment Position Report
    "!AIVDM,1,1,,B,15NJ0E1P00RHDLDGww8V1?vN0000,0*60",

    # Type 24 - Static Data Report
    "!AIVDM,1,1,,B,24NjQa000001wvRD5Q??Uww2:RO,0*51",
]

for sentence in nmea_sentences:
    print(decode_ais_message(sentence))
