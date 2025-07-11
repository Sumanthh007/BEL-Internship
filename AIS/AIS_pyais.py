from pyais import NMEAMessage

def decode_ais_message(nmea_message):
    """Decode any AIS message type from NMEA format."""
    try:
        # Parse the NMEA message using pyais
        msg = NMEAMessage.from_string(nmea_message)
        
        # Decode the message
        decoded_msg = msg.decode()
        
        # Get the message type
        message_type = decoded_msg.msg_type
        print(f"Message Type: {message_type}")
        
        # Initialize the result dictionary
        result = {'message_type': message_type}

        # Generic attributes applicable to most AIS messages
        result['mmsi'] = getattr(decoded_msg, 'mmsi', 'N/A')

        # Handle different AIS message types (1 to 27)
        if message_type in [1, 2, 3]:
            # Position Reports (Types 1, 2, 3)
            result.update({
                'longitude': getattr(decoded_msg, 'longitude', 'N/A'),
                'latitude': getattr(decoded_msg, 'latitude', 'N/A'),
                'speed_over_ground': getattr(decoded_msg, 'sog', 'N/A'),
                'course_over_ground': getattr(decoded_msg, 'cog', 'N/A'),
                'true_heading': getattr(decoded_msg, 'true_heading', 'N/A'),
                'navigational_status': getattr(decoded_msg, 'navigational_status', 'N/A')
            })
        elif message_type == 4:
            # Base Station Report (Type 4)
            result.update({
                'timestamp': getattr(decoded_msg, 'timestamp', 'N/A'),
                'longitude': getattr(decoded_msg, 'longitude', 'N/A'),
                'latitude': getattr(decoded_msg, 'latitude', 'N/A')
            })
        elif message_type == 5:
            # Static and Voyage Related Data (Type 5)
            result.update({
                'imo_number': getattr(decoded_msg, 'imo_number', 'N/A'),
                'callsign': getattr(decoded_msg, 'call_sign', 'N/A').strip(),
                'ship_name': getattr(decoded_msg, 'name', 'N/A').strip(),
                'ship_type': getattr(decoded_msg, 'type_of_ship_and_cargo', 'N/A'),
                'destination': getattr(decoded_msg, 'destination', 'N/A').strip(),
                'eta': f"{getattr(decoded_msg, 'eta_month', 'N/A')}/{getattr(decoded_msg, 'eta_day', 'N/A')} {getattr(decoded_msg, 'eta_hour', 'N/A')}:{getattr(decoded_msg, 'eta_minute', 'N/A')}"
            })
        elif message_type == 6:
            # Addressed Binary Message (Type 6)
            result.update({
                'sequence_number': getattr(decoded_msg, 'sequence_number', 'N/A'),
                'destination_mmsi': getattr(decoded_msg, 'destination_mmsi', 'N/A'),
                'retransmit_flag': getattr(decoded_msg, 'retransmit_flag', 'N/A'),
                'binary_data': getattr(decoded_msg, 'binary_data', 'N/A')
            })
        # Add more message types handling as needed
        elif message_type == 24:
            # Static Data Report (Type 24)
            result.update({
                'part_number': getattr(decoded_msg, 'part_number', 'N/A'),
                'ship_name': getattr(decoded_msg, 'name', 'N/A').strip(),
                'callsign': getattr(decoded_msg, 'call_sign', 'N/A').strip(),
                'ship_type': getattr(decoded_msg, 'type_of_ship_and_cargo', 'N/A'),
                'dimension_to_bow': getattr(decoded_msg, 'dimension_to_bow', 'N/A'),
                'dimension_to_stern': getattr(decoded_msg, 'dimension_to_stern', 'N/A'),
                'dimension_to_port': getattr(decoded_msg, 'dimension_to_port', 'N/A'),
                'dimension_to_starboard': getattr(decoded_msg, 'dimension_to_starboard', 'N/A')
            })
        else:
            # Handle unsupported or unimplemented message types
            result['data'] = f"Decoding for message type {message_type} is not specifically handled."
        
        return result
    
    except AttributeError as e:
        print(f"An error occurred while decoding: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while decoding: {e}")
        return None


# Example NMEA messages for testing
nmea_messages = [
    "!AIVDM,1,1,,B,15Mv`;P00R8GpFP<JLPT3?wP0D00,0*6C",  # Type 1, 2, or 3 Position Report
    "!AIVDM,1,1,,B,402P?v1vS13j@<:O<UQEqgvN0000,0*1F",  # Type 4 Base Station Report
    "!AIVDM,2,1,1,B,55P:v`02>t@DN1K7G6C4QDpU0TKH0000000000000,0*3B",  # Type 5 Static and Voyage Data
    "!AIVDM,1,1,,A,64:Ijv00000H1K3o2Tf:a000,0*5C",  # Type 6 Binary Message
    "!AIVDM,1,1,,B,24NjQa000001wvRD5Q??Uww2:RO,0*51",  # Type 24 Static Data Report
]

# Decode and print output for each message
for nmea in nmea_messages:
    result = decode_ais_message(nmea)
    print(result)
