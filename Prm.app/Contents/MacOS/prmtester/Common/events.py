SEQUENCE_START = 0
SEQUENCE_END = 1
ITEM_START = 2
ITEM_FINISH = 3
ATTRIBUTE_FOUND = 4
REPORT_ERROR = 5
UOP_DETECT = 6
SEQUENCE_LOADED = 7
LIST_ALL = 8
STATEMATHINE = 9
HEATBEAT =10

UUT_REMOVED = 11

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
        return 'LIST_ALL'
    elif event_type == 9:
        return 'STATEMATHINE'
    elif event_type == 10:
        return 'HEATBEAT'
    elif event_type ==11:
        return "UUT_REMOVED"
    else:
        return 'UNKNOWN event type: ' + str(event_type)
