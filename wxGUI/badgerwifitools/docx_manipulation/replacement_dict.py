# replacement_dict.py

image_search = {
    # AP Brackets, indoor APs
    'AP-MNT-A': {
        'image': 'AP-MNT-A.png',
        'height': 23},
    'AP-MNT-B': {
        'image': 'AP-MNT-B.png',
        'height': 23},
    'AP-MNT-C': {
        'image': 'AP-MNT-C.png',
        'height': 23},
    'AP-MNT-D': {
        'image': 'AP-MNT-D.png',
        'height': 23},
    'AP-MNT-E': {
        'image': 'AP-MNT-E.png',
        'height': 16},
    'AP-MNT-U': {
        'image': 'AP-MNT-U.png',
        'height': 16},

    # Antenna Brackets outdoor APs, full names
    'AP-270-MNT-H1': {
        'image': 'AP-270-MNT-H1.png',
        'height': 23},
    'AP-270-MNT-H2': {
        'image': 'AP-270-MNT-H2.png',
        'height': 23},
    'AP-270-MNT-H3': {
        'image': 'AP-270-MNT-H3.png',
        'height': 23},
    'AP-OUT-MNT-V1A': {
        'image': 'AP-OUT-MNT-V1A.png',
        'height': 23},
    'AP-270-MNT-V2': {
        'image': 'AP-270-MNT-V2.png',
        'height': 23},
    'AP-ANT-MNT-U': {
        'image': 'AP-ANT-MNT-U.png',
        'height': 23},

    # Antenna Brackets outdoor APs, short names
    'V1A': {
        'image': 'AP-OUT-MNT-V1A.png',
        'height': 23},
    'V2': {
        'image': 'AP-270-MNT-V2.png',
        'height': 23},
    'H1': {
        'image': 'AP-270-MNT-H1.png',
        'height': 23},
    'H2': {
        'image': 'AP-270-MNT-H2.png',
        'height': 23},
    'H3': {
        'image': 'AP-270-MNT-H3.png',
        'height': 23},

    # Antennas
    'Aruba AP-ANT-45 5GHz 5.5dBi': {
        'image': 'AP-ANT-45.png',
        'height': 18},
    'Aruba AP-ANT-345 5GHz': {
        'image': 'AP-ANT-345.png',
        'height': 18},

    # Angles of tilt
    '0.0°': {
        'image': 'EKA-TILT-0.png',
        'height': 18},
    '-20.0°': {
        'image': 'EKA-TILT-20.png',
        'height': 18},
    '-30.0°': {
        'image': 'EKA-TILT-30.png',
        'height': 18},
    '-45.0°': {
        'image': 'EKA-TILT-45.png',
        'height': 18},

    # fail-safes
    'unknown': {
        'image': 'unknown.png',
        'height': 18},
    'not-required': {
        'image': 'unknown.png',
        'height': 18},
    'Not-Required': {
        'image': 'unknown.png',
        'height': 18},

    # Access Points
    'Aruba AP-514 +  AP-ANT-45 5GHz': {
        'image': 'AP-514.png',
        'height': 18},
    'Aruba AP-514 +  Aruba AP-ANT-345': {
        'image': 'AP-514.png',
        'height': 18},
    'Aruba AP-514 +  AP-ANT-345': {
        'image': 'AP-514.png',
        'height': 18},
    'Aruba AP-514 + AP-ANT-345': {
        'image': 'AP-514.png',
        'height': 18},
    'Aruba AP-565': {
        'image': 'AP-565.png',
        'height': 18},
    'Aruba AP-567': {
        'image': 'AP-567.png',
        'height': 15},
    'Aruba AP-634': {
        'image': 'AP-634.png',
        'height': 18},
    'Aruba AP-635': {
        'image': 'AP-635.png',
        'height': 18},
    'Aruba AP-655 5GHz': {
        'image': 'AP-655.png',
        'height': 18},
    'Aruba AP-655': {
        'image': 'AP-655.png',
        'height': 18}
}

text_search = {
    # Antennas
    'Aruba AP-635 5GHz': 'integrated, omnidirectional',
    'Aruba AP-655 5GHz': 'integrated, omnidirectional',

    'Aruba AP-565 5GHz': 'integrated, omnidirectional',
    'Aruba AP-567 5GHz': 'integrated, directional',

    'Aruba AP-585 5GHz': 'integrated, omnidirectional',
    'Aruba AP-587 5GHz': 'integrated, directional',

    'Aruba AP-ANT-45 5GHz 5.5dBi': 'AP-ANT-45\x0D(external, directional)',
    'Aruba AP-ANT-345 5GHz': 'AP-ANT-345\x0D(external, directional)',

    # Access Point model correction
    'Aruba AP-514 +  Aruba AP-ANT-45': 'Aruba AP-514',
    'Aruba AP-514 + AP-ANT-345': 'Aruba AP-514',
    'Aruba AP-514 +  Aruba AP-ANT-345': 'Aruba AP-514',
}
