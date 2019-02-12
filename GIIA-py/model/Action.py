# -*- coding: utf-8 -*-


class UserDefinedAction(object):
    """Actions defined by user"""
    def __init__(self, action_id, action_label=None):
        self.action_id = action_id
        self.action_label = str(action_id) if action_label is None else action_label.replace(',', '')

    def __repr__(self):
        return "<UserDefinedAction {0} : \"{1}\">".format(self.action_id, self.action_label)

    def __str__(self):
        return "{0} : {1}".format(self.action_id, self.action_label)

    def __eq__(self, other):
        return type(self) == type(other) and self.action_id == other.action_id


class ActionSet(object):
    """Set of user defined actions"""
    def __init__(self, name):
        self.actions = set()
        self.name = name

    def __sizeof__(self):
        return self.actions.__sizeof__()

    def addAction(self, action):
        self.actions.add(action)
