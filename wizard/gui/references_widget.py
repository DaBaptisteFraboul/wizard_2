# coding: utf-8
# Author: Leo BRUNEL
# Contact: contact@leobrunel.com

# Python modules
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal

# Wizard gui modules
from wizard.gui import search_reference_widget
from wizard.gui import gui_utils
from wizard.gui import create_ticket_widget

# Wizard modules
from wizard.core import assets
from wizard.core import project
from wizard.vars import ressources
from wizard.core import custom_logger
logger = custom_logger.get_logger(__name__)

class references_widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(references_widget, self).__init__(parent)
        self.search_reference_widget = search_reference_widget.search_reference_widget()
        self.reference_infos_thread = reference_infos_thread()
        self.work_env_id = None
        self.reference_ids = dict()
        self.stage_dic = dict()
        self.build_ui()
        self.connect_functions()

    def connect_functions(self):
        self.search_sc = QtWidgets.QShortcut(QtGui.QKeySequence('Tab'), self)
        self.search_sc.activated.connect(self.search_reference)
        self.reference_infos_thread.reference_infos_signal.connect(self.update_item_infos)

        self.remove_selection_button.clicked.connect(self.remove_selection)
        self.update_button.clicked.connect(self.update_selection)
        self.create_ticket_button.clicked.connect(self.create_ticket)

    def update_item_infos(self, infos_list):
        reference_id = infos_list[0]
        if reference_id in self.reference_ids.keys():
            self.reference_ids[reference_id].update_item_infos(infos_list)

    def search_reference(self):
        self.search_reference_widget = search_reference_widget.search_reference_widget()
        self.search_reference_widget.variant_ids_signal.connect(self.create_references_from_variant_ids)
        self.search_reference_widget.show()
        
        if self.work_env_id is not None:
            variant_row = project.get_variant_data(project.get_work_env_data(self.work_env_id, 'variant_id'))
            stage_row = project.get_stage_data(variant_row['stage_id'])
            asset_row = project.get_asset_data(stage_row['asset_id'])
            category_row = project.get_category_data(asset_row['category_id'])
            self.search_reference_widget.search_asset(f"{category_row['name']}:{asset_row['name']}")

    def create_references_from_variant_ids(self, variant_ids):
        if self.work_env_id is not None:
            for variant_id in variant_ids:
                assets.create_references_from_variant_id(self.work_env_id, variant_id)

    def change_work_env(self, work_env_id):
        self.reference_ids = dict()
        self.stage_dic = dict()
        self.list_view.clear()
        self.work_env_id = work_env_id
        self.refresh()

    def refresh(self):
        if self.isVisible():
            if self.work_env_id is not None:
                reference_rows = project.get_references(self.work_env_id)
                project_references_id = []
                if reference_rows is not None:
                    for reference_row in reference_rows:
                        project_references_id.append(reference_row['id'])
                        if reference_row['id'] not in self.reference_ids.keys():
                            stage = reference_row['stage']
                            if stage not in self.stage_dic.keys():
                                stage_item = custom_stage_tree_item(stage, self.list_view.invisibleRootItem())
                                self.stage_dic[stage] = stage_item
                            reference_item = custom_reference_tree_item(reference_row, self.stage_dic[stage])
                            self.reference_ids[reference_row['id']] = reference_item
                    references_list_ids = list(self.reference_ids.keys())
                    for reference_id in references_list_ids:
                        if reference_id not in project_references_id:
                            self.remove_reference_item(reference_id)
                    self.reference_infos_thread.update_references_rows(reference_rows)
                    self.update_stages_items()

    def remove_selection(self):
        selected_items = self.list_view.selectedItems()
        for selected_item in selected_items:
            reference_id = selected_item.reference_row['id']
            assets.remove_reference(reference_id)

    def create_ticket(self):
        selected_items = self.list_view.selectedItems()
        if len(selected_items) == 1:
            export_version_id = selected_items[0].reference_row['export_version_id']
            self.create_ticket_widget = create_ticket_widget.create_ticket_widget(export_version_id)
            self.create_ticket_widget.show()
        else:
            logger.warning('Please select one reference')

    def update_selection(self):
        selected_items = self.list_view.selectedItems()
        for selected_item in selected_items:
            reference_id = selected_item.reference_row['id']
            assets.set_reference_last_version(reference_id)

    def remove_reference_item(self, reference_id):
        if reference_id in self.reference_ids.keys():
            item = self.reference_ids[reference_id]
            item.parent().removeChild(item)
            del self.reference_ids[reference_id]

    def update_stages_items(self):
        stages_list = list(self.stage_dic.keys())
        for stage in stages_list:
            item = self.stage_dic[stage]
            childs = item.childCount()
            if childs >= 1:
                item.update_infos(childs)
            else:
                self.list_view.invisibleRootItem().removeChild(item)
                del self.stage_dic[stage]

    def build_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        self.info_widget = gui_utils.info_widget()
        self.info_widget.setVisible(0)
        self.main_layout.addWidget(self.info_widget)

        self.list_view = QtWidgets.QTreeWidget()
        self.list_view.setAnimated(1)
        self.list_view.setExpandsOnDoubleClick(1)
        self.list_view.setObjectName('tree_as_list_widget')
        self.list_view.setColumnCount(5)
        self.list_view.setIndentation(20)
        self.list_view.setAlternatingRowColors(True)
        self.list_view.setHeaderLabels(['Stage', 'Namespace', 'Variant', 'Exported asset', 'Export version'])
        self.list_view.header().resizeSection(0, 200)
        self.list_view.header().resizeSection(1, 250)
        self.list_view.header().resizeSection(3, 250)
        self.list_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_view_scrollBar = self.list_view.verticalScrollBar()
        self.main_layout.addWidget(self.list_view)

        self.buttons_widget = QtWidgets.QWidget()
        self.buttons_widget.setObjectName('dark_widget')
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setContentsMargins(8,8,8,0)
        self.buttons_layout.setSpacing(4)
        self.buttons_widget.setLayout(self.buttons_layout)
        self.main_layout.addWidget(self.buttons_widget)

        self.buttons_layout.addSpacerItem(QtWidgets.QSpacerItem(0,0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        
        self.search_bar = gui_utils.search_bar()
        gui_utils.application_tooltip(self.search_bar, "Search for a specific version")
        self.search_bar.setPlaceholderText('"0023", "user:j.smith", "comment:retake eye", "from:houdini"')
        self.buttons_layout.addWidget(self.search_bar)

        self.remove_selection_button = QtWidgets.QPushButton()
        gui_utils.application_tooltip(self.remove_selection_button, "Remove selected references")
        self.remove_selection_button.setFixedSize(35,35)
        self.remove_selection_button.setIconSize(QtCore.QSize(30,30))
        self.remove_selection_button.setIcon(QtGui.QIcon(ressources._tool_archive_))
        self.buttons_layout.addWidget(self.remove_selection_button)

        self.create_ticket_button = QtWidgets.QPushButton()
        gui_utils.application_tooltip(self.create_ticket_button, "Open a ticket")
        self.create_ticket_button.setFixedSize(35,35)
        self.create_ticket_button.setIconSize(QtCore.QSize(30,30))
        self.create_ticket_button.setIcon(QtGui.QIcon(ressources._tool_ticket_))
        self.buttons_layout.addWidget(self.create_ticket_button)     

        self.update_button = QtWidgets.QPushButton()
        gui_utils.application_tooltip(self.update_button, "Update selected references")
        self.update_button.setFixedSize(35,35)
        self.update_button.setIconSize(QtCore.QSize(30,30))
        self.update_button.setIcon(QtGui.QIcon(ressources._tool_update_))
        self.buttons_layout.addWidget(self.update_button)     

        self.infos_widget = QtWidgets.QWidget()
        self.infos_widget.setObjectName('dark_widget')
        self.infos_layout = QtWidgets.QHBoxLayout()
        self.infos_layout.setContentsMargins(8,8,8,8)
        self.infos_layout.setSpacing(4)
        self.infos_widget.setLayout(self.infos_layout)
        self.main_layout.addWidget(self.infos_widget)

        self.infos_layout.addSpacerItem(QtWidgets.QSpacerItem(0,0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))

        self.versions_count_label = QtWidgets.QLabel()
        self.versions_count_label.setObjectName('gray_label')
        self.infos_layout.addWidget(self.versions_count_label)

        self.selection_count_label = QtWidgets.QLabel()
        self.infos_layout.addWidget(self.selection_count_label)

class custom_stage_tree_item(QtWidgets.QTreeWidgetItem):
    def __init__(self, stage, parent=None):
        super(custom_stage_tree_item, self).__init__(parent)
        self.stage = stage
        self.setFlags(QtCore.Qt.ItemIsEnabled)
        self.fill_ui()

    def fill_ui(self):
        self.setText(0, self.stage)
        self.setIcon(0, QtGui.QIcon(ressources._stage_icons_dic_[self.stage]))

    def update_infos(self, childs):
        self.setText(0, f"{self.stage} ({childs})")

class custom_reference_tree_item(QtWidgets.QTreeWidgetItem):
    def __init__(self, reference_row, parent=None):
        super(custom_reference_tree_item, self).__init__(parent)
        self.reference_row = reference_row
        self.fill_ui()

    def fill_ui(self):
        self.setText(1, self.reference_row['namespace'])
        bold_font=QtGui.QFont()
        bold_font.setBold(True)
        self.setFont(1, bold_font)
        self.setFont(4, bold_font)
        self.setIcon(0, QtGui.QIcon(ressources._stage_icons_dic_[self.reference_row['stage']]))

    def update_item_infos(self, infos_list):
        self.setText(2, infos_list[1])
        self.setText(3, infos_list[2])
        self.setText(4, infos_list[3])
        if infos_list[4]:
            self.setForeground(4, QtGui.QBrush(QtGui.QColor('#9ce87b')))
        else:
            self.setForeground(4, QtGui.QBrush(QtGui.QColor('#f79360')))

class reference_infos_thread(QtCore.QThread):

    reference_infos_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(reference_infos_thread, self).__init__(parent)
        self.reference_rows = None
        self.running = True

    def run(self):
        if self.reference_rows is not None:
            for reference_row in self.reference_rows:
                export_version_row = project.get_export_version_data(reference_row['export_version_id'])
                export_row = project.get_export_data(export_version_row['export_id'])
                variant_row = project.get_variant_data(export_row['variant_id'])
                last_export_version_id = project.get_last_export_version(export_row['id'], 'id')

                if last_export_version_id[0] != reference_row['export_version_id']:
                    up_to_date = 0
                else:
                    up_to_date = 1

                self.reference_infos_signal.emit([reference_row['id'], variant_row['name'], export_row['name'], export_version_row['name'], up_to_date])

    def update_references_rows(self, reference_rows):
        self.running = False
        self.reference_rows = reference_rows
        self.running = True
        self.start()