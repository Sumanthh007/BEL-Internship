from pyais import decode

# Example AIS message string (as NMEA format)
nmea_messages = [
    # Type 1, 2, or 3 - Position Report
    "!AIVDM,1,1,,B,15Mv`;P00R8GpFP<JLPT3?wP0D00,0*6C",  

    # Type 4 - Base Station Report
    "!AIVDM,1,1,,B,402P?v1vS13j@<:O<UQEqgvN0000,0*1F",  

    # Type 5 - Static and Voyage Related Data
    "!AIVDM,2,1,1,B,55P:v`02>t@DN1K7G6C4QDpU0TKH0000000000000,0*3B",  
    
    # Type 6 - Addressed Binary Message
    "!AIVDM,1,1,,A,64:Ijv00000H1K3o2Tf:a000,0*5C",

    # Type 7 - Binary Acknowledge
    "!AIVDM,1,1,,A,702PA=0u:3fp,0*18",

    # Type 8 - Binary Broadcast Message
    "!AIVDM,1,1,,B,802I=b1P=gjWQ@PTHu`0000,0*0C",

    # Type 9 - Standard SAR Aircraft Position Report
    "!AIVDM,1,1,,A,902:P=B1w;fRRVRe2rh0,0*34",

    # Type 10 - UTC/Date Inquiry
    "!AIVDM,1,1,,A,A0SEbdP00000Mwj,0*27",

    # Type 11 - UTC/Date Response
    "!AIVDM,1,1,,B,B0E8A=B8=EBDF00M00G00000,0*48",

    # Type 12 - Addressed Safety Related Message
    "!AIVDM,1,1,,A,C60HH500b8dSD0,0*4C",

    # Type 13 - Safety Related Acknowledge
    "!AIVDM,1,1,,A,D02I=b1,0*36",

    # Type 14 - Safety Related Broadcast Message
    "!AIVDM,1,1,,A,E027jdP00000000000000000,0*6F",

    # Type 15 - Interrogation
    "!AIVDM,1,1,,B,F02INP01P51wo,0*1E",

    # Type 16 - Assigned Mode Command
    "!AIVDM,1,1,,A,G026hG00p1Cv,0*3A",

    # Type 17 - GNSS Binary Broadcast Message
    "!AIVDM,1,1,,A,H02SNB1=0001whw,0*18",

    # Type 18 - Standard Class B Equipment Position Report
    "!AIVDM,1,1,,B,15NJ0E1P00RHDLDGww8V1?vN0000,0*60",

    # Type 19 - Extended Class B Equipment Position Report
    "!AIVDM,1,1,,B,53uHEH2jOn3?1p3NJ20nBLqN0000,0*78",

    # Type 20 - Data Link Management
    "!AIVDM,1,1,,A,K026SNB1TnqFN,0*32",


    # Type 24 - Static Data Report
    "!AIVDM,1,1,,B,24NjQa000001wvRD5Q??Uww2:RO,0*51",


]

for nmea_message in nmea_messages:
# Decode the AIS message
    try:
        decoded_message = decode(nmea_message)
        print("Decoded Message:", decoded_message)
    except Exception as e:
        print(f"An error occurred: {e}")

