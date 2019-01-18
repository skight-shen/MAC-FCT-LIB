#!/usr/bin/env python
#encoding=utf-8

import zmq
import json
import traceback
import logging


class StateSwitch(object):

    def __init__(self, initial_state, publisher):
        self.curr_state = initial_state
        self.publisher = publisher
        self.sm = {}
        
      
    def add_transition(self, old_state, new_state, event, func):  
        self.sm.setdefault(old_state, {})
        self.sm[old_state].setdefault(event, {})
        self.sm[old_state][event].setdefault("func", func)
        self.sm[old_state][event].setdefault("new_state", new_state)

    
        
    def state_switch(self, event, *args, **kwargs):
        try:
            func = self.sm[self.curr_state][event]["func"]
            new_state = self.sm[self.curr_state][event]["new_state"]
            
            if func is not None:
                func(*args, **kwargs)
                logging.info("sm state %s --> %s", self.curr_state, new_state)
                self.curr_state = new_state

            else:
                logging.warn("there is no function for state:%s event:%s", self.curr_state, event)
            
                
        except (KeyError, TypeError, AttributeError) as e:
            logging.error("%s", str(traceback.format_exc()))
            return -1
        
        return 0


