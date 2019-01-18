SEQUENCE_START = 0
SEQUENCE_END = 1
ITEM_START = 2
ITEM_FINISH = 3
ATTRIBUTE_FOUND = 4
REPORT_ERROR = 5
UOP_DETECT = 6
SEQUENCE_LOADED = 7
FCT_HEARTBEAT = 8


def get_name(event_type):
    if event_type == 0:
        return 'SEQUENCE_START'
    elif event_type == 1:
        return 'SEQUENCE_END'
    elif event_type == 2:
        return 'ITEM_START'
    elif event_type == 3:
        return 'ITEM_FINISH'
    elif event_type == 4:
        return 'ATTRIBUTE_FOUND'
    elif event_type == 5:
        return 'REPORT_ERROR_OCCURRED'
    elif event_type == 6:
        return 'UOP_DETECTED'
    elif event_type == 7:
        return 'SEQUENCE LOADED'
    elif event_type == 8:
        return 'FCT_HEARTBEAT'
    else:
        return 'UNKNOWN event type: ' + str(event_type)
