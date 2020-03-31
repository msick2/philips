SUBSCRIPT_CAPITAL_E_CHAR = 0xE145  # SUBSCRIPT CAPITAL E
SUBSCRIPT_CAPITAL_L_CHAR = 0xE14C  # SUBSCRIPT CAPITAL L
LITER_PER_CHAR = 0xE400  # LITER PER - used in 4 char unit "l/min"
HYDROGEN_CHAR = 0xE401  # HYDROGEN - Used in 4 char unit "cmH2O"
ALARM_STAR_CHAR = 0xE40D  # ALARM STAR
CAPITAL_V_WITH_DOT_ABOVE_CHAR = 0xE425  # CAPITAL_V_WITH_DOT_ABOVE (V with dot)
ZERO_WIDTH_NO_BREAK_SPACE_CHAR = 0xFEFF  # The character 0xFEFF is used as FILL character.For each wide asian character, a FILL character isappended for size calculations.

ROIV_APDU = 1  #
RORS_APDU = 2  #
ROER_APDU = 3  #
ROLRS_APDU = 5  #

RORLS_FIRST = 1  # set in the first message
RORLS_NOT_FIRST_NOT_LAST = 2  #
RORLS_LAST = 3  # last RORLSapdu, one RORSapdu to follow

CMD_EVENT_REPORT = 0  #
CMD_CONFIRMED_EVENT_REPORT = 1  #
CMD_GET = 3  #
CMD_SET = 4  #
CMD_CONFIRMED_SET = 5  #
CMD_CONFIRMED_ACTION = 7  #

NO_SUCH_OBJECT_CLASS = 0  #
NO_SUCH_OBJECT_INSTANCE = 1  #
ACCESS_DENIED = 2  #
GET_LIST_ERROR = 7  #
SET_LIST_ERROR = 8  #
NO_SUCH_ACTION = 9  #
PROCESSING_FAILURE = 10  #
INVALID_ARGUMENT_VALUE = 15  #
INVALID_SCOPE = 16  #
INVALID_OBJECT_INSTANCE = 17  #

NOM_NOTI_MDS_CREAT = 3334  # MDS Create Notification
NOM_NOTI_CONN_INDIC = 3351  # connect indication event type
NOM_ACT_POLL_MDIB_DATA = 3094  # poll data action
NOM_ACT_POLL_MDIB_DATA_EXT = 61755  # extended poll data action

NOM_POLL_PROFILE_SUPPORT = 1  # id for polling profile
NOM_MDIB_OBJ_SUPPORT = 258  # supported objects for the active profile
NOM_ATTR_POLL_PROFILE_EXT = 61441  # id for poll profile extensions opt. package

MDDL_VERSION1 = 0x80000000  # Data Export Protocol Version
NOMEN_VERSION = 0x40000000  # Nomenclature Version
SYST_CLIENT = 0x80000000  # System Type Client
SYST_SERVER = 0x00800000  # System Type Server
HOT_START = 0x80000000  # Startup Mode Hotstart
WARM_START = 0x40000000  # Startup Mode Warmstart
COLD_START = 0x20000000  # Startup Mode Coldstart
POLL_PROFILE_REV_0 = 0x80000000  # Poll Profile Revision
P_OPT_DYN_CREATE_OBJECTS = 0x40000000  # option dynamic object creation
P_OPT_DYN_DELETE_OBJECTS = 0x20000000  # option dynamic object deletion
POLL_EXT_PERIOD_NU_1SEC = 0x80000000  # 1 sec Real-time Numerics
POLL_EXT_PERIOD_NU_AVG_12SEC = 0x40000000  # 12 sec averaged Numerics
POLL_EXT_PERIOD_NU_AVG_60SEC = 0x20000000  # 1 min. averaged Numerics
POLL_EXT_PERIOD_NU_AVG_300SEC = 0x10000000  # 5 min. averaged Numerics
POLL_EXT_PERIOD_RTSA = 0x08000000  # allow enumeration objects
POLL_EXT_ENUM = 0x04000000  # allow numeric priority list to be set
POLL_EXT_NU_PRIO_LIST = 0x02000000  # send timestamps for numerics with dynamic modalities
POLL_EXT_DYN_MODALITIES = 0x01000000  #
