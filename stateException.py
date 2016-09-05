#!/usr/sbin/env python
#coding=utf-8


class StateException(Exception):
    def __init__(self, e, state):
        Exception.__init__(self, e)
        self.state = state
        self.mesg = '\n' + str(e)


    def get_state(self):
        return self.state


    def __str__(self):
        return self.mesg

