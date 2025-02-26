fourDA_BBB_fields   = ["reading","percentage"]
fourDA_WIA_fields   = ["light", "temperature", "humidity", "motion", "soundPeak", "soundAvg"]
fourDA_CIVIC_fields = ["speed", "headway", "occupancy", "gap", "volume"]
HiData_fields       = ["occupancy", "light", "noise"]
WIA_fields          = ["light", "temperature", "humidity", "motion", "soundPeak", "soundAvg"]
CIVIC_fields        = ["speed", "headway", "occupancy", "gap", "volume"]

sensor_types = ['WIA_TYPE', 'HIDATA_TYPE', 'CIVIC_TYPE', '4DA_WIA_TYPE', '4DA_BBB_TYPE', '4DA_CIVIC_TYPE']
sensor_areas = ['ALL_DCU', 'Stokes Building', 'Business School', 'Marconi Building', 'Sports Complex']
sensor_rooms = ['1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2', '3.3', '4.1', '4.2', '4.3', '505']

CIVIC_classes = ['PEDESTRIAN', 'BIKE', 'LONG TRUCK', 'MOTORBIKE', 'SHORT TRUCK', 'CAR', 'UNDEFINED']

firebase_types = ['entering', 'exiting', 'people']