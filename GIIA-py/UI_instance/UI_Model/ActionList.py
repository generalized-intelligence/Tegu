# -*- coding: utf-8 -*-

from collections import OrderedDict

from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QEvent
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QGridLayout, QVBoxLayout, QLineEdit, \
    QScrollArea

from config import defaults
from config.defaults import to_css_format, ANNOTATION_TAG_COLORS
from model.Action import UserDefinedAction




class ActionItem(QWidget):
    """Action item UI widget shown in the action list"""

    actionLabelChange = pyqtSignal(int, str)
    actionItemGetFocus = pyqtSignal(int)

    def __init__(self, action, parent=None):
        super(ActionItem, self).__init__(parent)
        self.locked = False
        self.selected = False
        self.user_action = action
        self.action_number = QLabel(self)
        self.color_label = QLabel('█', self) # ascii 219
        self.action_name = QLineEdit(self)
        self.initUI()

    def initUI(self):
        self.action_number.setText(str(self.user_action.action_id))
        self.action_number.setFixedSize(50, 50)
        self.action_number.setAlignment(Qt.AlignCenter)
        self.action_number.setStyleSheet(defaults.ITEM_NUMBER_STYLE_NORMAL)

        self.action_name.setDragEnabled(True)
        self.action_name.setText(str(self.user_action.action_label))
        self.action_name.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.color_label.setStyleSheet('color: ' + to_css_format(ANNOTATION_TAG_COLORS[self.user_action.action_id % 9]))

        self.action_name.installEventFilter(self)

        layout = QHBoxLayout()
        layout.addWidget(self.action_number)
        layout.addWidget(self.color_label)
        layout.addWidget(self.action_name)
        self.setLayout(layout)

    def setUserAction(self, action):
        self.user_action = action
        self.action_number.setText(str(self.user_action.action_id))
        self.action_name.setText(str(self.user_action.action_label))
        self.color_label.setStyleSheet('color: ' + to_css_format(ANNOTATION_TAG_COLORS[self.user_action.action_id % 9]))

    def setSelected(self, selected):
        if self.locked:
            self.selected = False
        else:
            self.selected = selected
        self.updateStyle()

    def updateStyle(self):
        if self.locked:
            self.action_number.setStyleSheet(defaults.ITEM_NUMBER_STYLE_LOCKED)
            return
        if self.selected:
            self.action_number.setStyleSheet(defaults.ITEM_NUMBER_STYLE_SELECTED)
            return
        self.action_number.setStyleSheet(defaults.ITEM_NUMBER_STYLE_NORMAL)



    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                obj.parent().focusNextChild()
        if event.type() == QEvent.FocusOut:
            if self.user_action.action_label != self.action_name.text():
                self.actionLabelChange.emit(self.user_action.action_id, self.action_name.text())
        if event.type() == QEvent.FocusIn:
            self.setSelected(True)
            self.actionItemGetFocus.emit(self.user_action.action_id)
        return super(ActionItem, self).eventFilter(obj, event)


class ActionList(QWidget):

    startAnnotation=pyqtSignal()
    annotationDocChange=pyqtSignal(str)
    annotationModeChange=pyqtSignal(int)
    actionSelect=pyqtSignal(int)

    def __init__(self,parent=None):
        super(ActionList, self).__init__(parent)

        # visually selected action item
        self.selectedActionItemId = -1
        self.action_items = OrderedDict()
        self.user_actions = OrderedDict()
        self.notice_label = QLabel('')
        self.add_action_button=QPushButton(None)
        self.delete_action_button=QPushButton(None)
        self.start_annotation_button=QPushButton(None)


        self.action_item_grid = QGridLayout()

        self.initUI()
    def setupButtons(self,btn_add,btn_del,btn_start):
        del self.add_action_button
        del self.delete_action_button
        del self.start_annotation_button
        self.add_action_button = btn_add
        self.delete_action_button = btn_del
        self.start_annotation_button = btn_start
        self.add_action_button.clicked.connect(self.addActionItem)
        self.delete_action_button.clicked.connect(self.deleteActionItem)
        self.start_annotation_button.clicked.connect(self.startAnnotationClicked)
        self.delete_action_button.setEnabled(False)

    def initUI(self):
        self.actionSelect.connect(self.selectedActionChanged)
        controls = QWidget()
        controls.setMaximumHeight(80)
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.notice_label)
        controls.setLayout(control_layout)
        items_wrapper = QWidget(self)
        items_wrapper.setLayout(self.action_item_grid)
        scrollArea = QScrollArea(self)
        scrollArea.setMinimumHeight(360)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(items_wrapper)
        outer_layout = QVBoxLayout()
        outer_layout.addWidget(scrollArea)
        outer_layout.addWidget(controls)
        self.setLayout(outer_layout)
        self.reset()
        self.loadDefaultActionSet()

    def selectActionItem(self, action_id):
        for k, v in self.action_items.items():
            if k == action_id:
                v.setSelected(True)
                self.selectedActionItemId = action_id
            else:
                v.setSelected(False)
        if self.selectedActionItemId != -1:
            self.actionSelect.emit(self.selectedActionItemId)

    def deselectActionItem(self):
        for i in self.action_items.values():
            i.setSelected(False)
        self.selectedActionItemId = -1
        self.actionSelect.emit(self.selectedActionItemId)

    def selectedActionChanged(self, action_id):
        if action_id > 0:
            self.delete_action_button.setEnabled(True)
        else:
            self.delete_action_button.setEnabled(False)

    def loadDefaultActionSet(self):
        self.setActionSetWithString(defaults.INIT_USER_ACTION_SET_STRING)
        self.updateActionItems()

    def addActionItem(self):
        max_id = 0 if len(self.user_actions) < 1 else max(self.user_actions.keys())
        action_id = max_id + 1
        if action_id >= defaults.MAX_ACTION_NUMBER:
            return
        self.user_actions[action_id] = UserDefinedAction(action_id, "Label-" + str(action_id))
        self.updateActionItems()

    def allActionItemsLocked(self):
        return all(map(lambda a:a.locked, self.action_items.values()))

    def deleteActionItem(self):
        #print("del")
        id_to_del = self.selectedActionItemId
        #print(id_to_del)
        #print(len(self.user_actions))
        if id_to_del < 1:
            return
        if len(self.user_actions) < 2:
            return
        if self.action_items[id_to_del].locked:
            return
        # re-assign action ids if deleted in the middle
        max_id = max(self.user_actions.keys())
        if max_id > id_to_del:
            for i in range(id_to_del, max_id):
                assert self.user_actions.get(i+1) is not None
                self.user_actions[i+1].action_id = i
                self.user_actions[i] = self.user_actions[i+1]
        del self.user_actions[max_id]
        self.updateActionItems()
        if max_id > id_to_del:
            self.selectActionItem(id_to_del)
        else:
            self.deselectActionItem()

    def updateActionItems(self):
        """Update action items (the view) according to user action set (the model)"""
        user_action_ids = set(self.user_actions.keys())
        items_to_delete = []
        items_updated = []
        # first, update existing items that have an action
        for item_id in self.action_items.keys():
            if item_id in user_action_ids:
                self.updateUserAction(item_id, self.user_actions[item_id])
                items_updated.append(item_id)
            else:
                items_to_delete.append(item_id)
        # then, remove those items without an action
        for item_id in items_to_delete:
            self.action_items[item_id].disconnect()
            self.action_item_grid.removeWidget(self.action_items[item_id])
            self.action_items[item_id].deleteLater()
            del self.action_items[item_id]
        # finally, add items for remaining (new) actions
        items_to_add = list(sorted(user_action_ids - set(self.action_items.keys())))
        for action_id in items_to_add:
            self.action_items[action_id] = ActionItem(self.user_actions[action_id], self)
            self.action_items[action_id].actionLabelChange.connect(self.actionLabelChanged)
            self.action_items[action_id].actionItemGetFocus.connect(self.actionItemFocused)
            self.action_item_grid.addWidget(self.action_items[action_id], (action_id - 1) // 3, (action_id - 1) % 3, Qt.AlignTop)
        self.deselectActionItem()
        if len(self.user_actions) < 1:
            self.start_annotation_button.setEnabled(False)
        else:
            self.start_annotation_button.setEnabled(True)

    def reset(self):
        """Reset only deselect item and clear annotation doc selection, won't remove user action set."""
        self.deselectActionItem()


    @pyqtSlot()
    def startAnnotationClicked(self):
        self.start_annotation_button.setFocus(Qt.MouseFocusReason)
        self.startAnnotation.emit()

    @pyqtSlot(int)
    def actionItemFocused(self, action_id):
        self.selectActionItem(action_id)

    def setActionSetWithString(self, actions_string):
        self.user_actions = OrderedDict()
        action_lines = actions_string.strip().split(',')
        last_updated_id = 0
        for line in action_lines:
            try:
                action_id_txt, action_label = line.split(":", 1)
                action_id = int(action_id_txt)
                if action_id == 0: # or action_id > defaults.MAX_ACTION_NUMBER:
                    continue
                while last_updated_id + 1 != action_id:
                    padding_action_id = last_updated_id + 1
                    self.user_actions[padding_action_id] = UserDefinedAction(padding_action_id,
                                                                             _("Label-{0}").format(padding_action_id))
                    last_updated_id = padding_action_id
                last_updated_id = action_id
                self.user_actions[action_id] = UserDefinedAction(action_id, action_label)
            except:
                continue
        self.updateActionItems()

    def updateUserAction(self, index, action):
        if self.user_actions[index] is not action:
            self.user_actions[index] = action
        if 0 < index:
            if self.action_items[index] is None:
                return
            self.action_items[index].setUserAction(self.user_actions[index])


    @pyqtSlot(int, str)
    def actionLabelChanged(self, index, new_label):
        self.user_actions[index] = UserDefinedAction(index, new_label)
        if index > 0 and len(self.action_items) >= index:
            self.action_items[index].setUserAction(self.user_actions[index])


    def mousePressEvent(self, mouse_event):
        if not self.isEnabled():
            mouse_event.ignore()
            return
        item = self.childAt(mouse_event.pos())
        if item is None:
            mouse_event.ignore()
            return
        if not isinstance(item, ActionItem):
            if isinstance(item.parent(), ActionItem):
                item = item.parent()
            else:
                self.deselectActionItem()
                mouse_event.accept()
                return
        if not item.selected:
            self.selectActionItem(item.user_action.action_id)
        mouse_event.accept()
