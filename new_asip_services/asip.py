# asip.py -   Arduino Services Interface Protocol (ASIP) V1.1
# 

#class ASIP(object):

# System messages
# Request messages to Arduino
SYSTEM_MSG_HEADER = '#'  # system requests are preceded with this tag
tag_SYSTEM_GET_INFO = '?'  # Get version and hardware info
tag_SERVICES_NAMES = 'N'  # get list of friendly service names
tag_PIN_SERVICES_LIST = 'S'  # gets a list of pins indicating registered service
tag_RESTART_REQUEST = 'R'  # disables all autoevents and attempts to restart all services


# messages from Arduino
EVENT_HEADER = '@'  # event messages are preceded with this tag
ERROR_MSG_HEADER = '~'  # error messages begin with this tag
INFO_MSG_HEADER = '!'  # info messages begin with this tag
DEBUG_MSG_HEADER = '!'  # debug txt with infor msgs preceeded with this tag

# tags available to all services 
tag_AUTOEVENT_REQUEST = 'A'  # this tag sets autoevent status
tag_REMAP_PIN_REQUEST = 'M'  # for services that can change pin numbers
# Reply tags common to all services
tag_SERVICE_EVENT = 'e' 

MIN_MSG_LEN = 4  # valid request messages must be at least this many characters

NO_EVENT = '\0'  # tag to indicate the a service does not produce an event
MSG_TERMINATOR = '\n'

#class Mirto(object):
# Motor service
id_MOTOR_SERVICE = 'M'
# Motor methods (messages to Arduino)
tag_SET_MOTOR = 'm'  # sets motor power
tag_SET_MOTORS = 'M'
tag_SET_MOTOR_RPM = 'r'  # wheel rpm
tag_SET_MOTORS_RPM = 'R'  # both wheels rpm
tag_SET_ROBOT_SPEED_CM = 'c'  # speed in Cm per Sec using PID
tag_ROTATE_ROBOT_ANGLE = 'a'  # Robot rotation using given degrees per second and angle
tag_STOP_MOTOR = 's'
tag_STOP_MOTORS = 'S'
tag_RESET_ENCODERS = 'E'  # rest total counts to zero


# Encoder service
id_ENCODER_SERVICE = id_MOTOR_SERVICE  #encoders are within motor service in ASIP v1.1
# Encoder methods - use system define, tag_AUTOEVENT_REQUEST ('A') to request autoevents
# Encoder events -  events use system tag: tag_SERVICE_EVENT  ('e')


# Bump detect service
id_BUMP_SERVICE = 'B'
# Bump sensor methods - use system define, tag_AUTOEVENT_REQUEST ('A') to request autoevents
# Bump Sensor events -  events use system tag: tag_SERVICE_EVENT  ('e')


# IR Line detect service
id_IR_REFLECTANCE_SERVICE = 'R'
# IR Line detect methods - use system define, tag_AUTOEVENT_REQUEST ('A') to request autoevents
# IR Line detect events -  events use system tag: tag_SERVICE_EVENT  ('e')


# LED LCD service
id_LCD_SERVICE = 'L'
# methods
tag_WRITE = 'W'            # write a line of text
tag_WRITE_RC = 'w'         # write text at given row and column
tag_GRAPH = 'G'            # draw graph
tag_CLEAR = 'C'            # clear screen

# RGB Pixel service
id_PIXELS_SERVICE = 'P'
# methods
tag_SET_PIXELS = 'P'  # 32 bit packed color value
tag_SET_PIXELS_RGB = 'p'  # colon seperated rgb values
tag_SET_PIXEL_SEQUENCE = 'S'
tag_SET_PIXEL_SEQUENCE_RGB = 's'
tag_SET_BRIGHTNESS = 'B'
tag_GET_NUMBER_PIXELS = 'I'
tag_CLEAR_ALL_PIXELS = 'C'

# Tone service
id_TONE_SERVICE = 'T'
# methods
tag_PLAY = 'P'           # play tone of given frequency and duration


NBR_WHEELS = 2  # defines the number of wheels (and encoders), note not tested with values other than 2

INFO_REQUEST = '#,?\n'
PIN_MODES_REQUEST = 'I,p\n'
CAPABILITY_REQUEST = 'I,c\n'
