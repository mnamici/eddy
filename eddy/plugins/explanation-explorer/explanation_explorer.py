# -*- coding: utf-8 -*-

##########################################################################
#                                                                        #
#  Eddy: a graphical editor for the specification of Graphol ontologies  #
#  Copyright (C) 2015 Daniele Pantaleone <danielepantaleone@me.com>      #
#                                                                        #
#  This program is free software: you can redistribute it and/or modify  #
#  it under the terms of the GNU General Public License as published by  #
#  the Free Software Foundation, either version 3 of the License, or     #
#  (at your option) any later version.                                   #
#                                                                        #
#  This program is distributed in the hope that it will be useful,       #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
#  GNU General Public License for more details.                          #
#                                                                        #
#  You should have received a copy of the GNU General Public License     #
#  along with this program. If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
#  #####################                          #####################  #
#                                                                        #
#  Graphol is developed by members of the DASI-lab group of the          #
#  Dipartimento di Ingegneria Informatica, Automatica e Gestionale       #
#  A.Ruberti at Sapienza University of Rome: http://www.dis.uniroma1.it  #
#                                                                        #
#     - Domenico Lembo <lembo@dis.uniroma1.it>                           #
#     - Valerio Santarelli <santarelli@dis.uniroma1.it>                  #
#     - Domenico Fabio Savo <savo@dis.uniroma1.it>                       #
#     - Daniele Pantaleone <pantaleone@dis.uniroma1.it>                  #
#     - Marco Console <console@dis.uniroma1.it>                          #
#                                                                        #
##########################################################################


from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from eddy.core.datatypes.graphol import Item, Identity
from eddy.core.datatypes.qt import Font
from eddy.core.datatypes.system import File
from eddy.core.functions.misc import first, rstrip
from eddy.core.functions.signals import connect, disconnect
from eddy.core.items.common import AbstractItem
from eddy.core.jvm import getJavaVM
from eddy.core.output import getLogger
from eddy.core.plugin import AbstractPlugin
from eddy.ui.dock import DockWidget
from eddy.ui.fields import StringField

LOGGER = getLogger()


class ExplanationExplorerPlugin(AbstractPlugin):
    """
    This plugin provides the Explanation Explorer widget.
    """
    sgnFakeExplanationAdded = QtCore.pyqtSignal(str)
    sgnFakeAxiomAdded = QtCore.pyqtSignal('QStandardItem', str)
    sgnFakeItemAdded = QtCore.pyqtSignal('QGraphicsScene', 'QGraphicsItem', 'QStandardItem')

    #############################################
    #   SLOTS
    #################################

    @QtCore.pyqtSlot()
    def onSessionReady(self):
        """
        Executed whenever the main session completes the startup sequence.
        """
        self.widget('explanation_explorer').doClear()

    @QtCore.pyqtSlot()
    def onConsistencyCheckStarted(self):
        """
        Executed when the consistency check is started.
        """
        self.widget('explanation_explorer').doClear()

    @QtCore.pyqtSlot()
    def onConsistencyCheckReset(self):
        """
        Executed when the consistency check is resetted.
        """
        self.widget('explanation_explorer').doClear()
        if self.widget('explanation_explorer_dock').isVisible():
            self.widget('explanation_explorer_dock').toggleViewAction().trigger()

    @QtCore.pyqtSlot()
    def onPerfectOntology(self):
        """
        Executed when the consistency check detects that the ontology is consistent and all classes
        are satisfiable.
        """
        self.widget('explanation_explorer').doClear()

    @QtCore.pyqtSlot()
    def onInconsistentOntology(self):
        """
        Executed when the consistency check detects that the active ontology is inconsistent.
        """
        self.widget('explanation_explorer').doClear()
        self.doUpdateExplanations()

    @QtCore.pyqtSlot()
    def onUnsatisfiableEntities(self):
        """
        Executed whenever the main session completes the startup sequence.
        """
        self.widget('explanation_explorer').doClear()

    @QtCore.pyqtSlot()
    def doUpdateExplanations(self):
        """
        Executed when the ontology is inconsistent or there are unsatisfiable classes to update the explanations.
        """
        # CONNECT TO PROJECT SPECIFIC SIGNALS
        widget = self.widget('explanation_explorer')
        widget.doClear()

        # FILL IN EXPLANATION EXPLORER WITH DATA
        connect(self.sgnFakeExplanationAdded, widget.doAddExplanation)
        connect(self.sgnFakeAxiomAdded, widget.doAddAxiom)
        connect(self.sgnFakeItemAdded, widget.doAddNodeOREdge)

        self.vm = getJavaVM()
        if not self.vm.isRunning():
            self.vm.initialize()
        self.vm.attachThreadToJVM()

        # Choose the explanation
        if len(self.project.explanations_for_inconsistent_ontology) > 0:
            explanations_for_widget = self.project.explanations_for_inconsistent_ontology
        else:
            if 'ConceptNode' in self.project.uc_as_input_for_explanation_explorer:
                unsatisfiable_entities = self.project.unsatisfiable_classes
                explanations_unsatisfiable_entity = self.project.explanations_for_unsatisfiable_classes
            elif 'AttributeNode' in self.project.uc_as_input_for_explanation_explorer:
                unsatisfiable_entities = self.project.unsatisfiable_attributes
                explanations_unsatisfiable_entity = self.project.explanations_for_unsatisfiable_attributes
            elif 'RoleNode' in self.project.uc_as_input_for_explanation_explorer:
                unsatisfiable_entities = self.project.unsatisfiable_roles
                explanations_unsatisfiable_entity = self.project.explanations_for_unsatisfiable_roles

            inp_node = None

            for n in self.project.nodes():
                if str(n) == self.project.uc_as_input_for_explanation_explorer:
                    inp_node = n
                    break

            OWL_term_uc_as_input_for_explanation_explorer = self.project.getOWLtermfornode(inp_node)
            index_uc = unsatisfiable_entities.index(OWL_term_uc_as_input_for_explanation_explorer)
            explanations_for_widget = explanations_unsatisfiable_entity[index_uc]

        for explanation_count, e in enumerate(explanations_for_widget):
            self.sgnFakeExplanationAdded.emit(str(explanation_count + 1))

        for explanation_count, e in enumerate(explanations_for_widget):
            axioms_for_iteration = []

            if self.project.inconsistent_ontology:
                axioms_temp = e.getAxioms()
                axioms_temp_itr = axioms_temp.iterator()
                while axioms_temp_itr.hasNext():
                    axiom_temp = axioms_temp_itr.next()
                    axioms_for_iteration.append(axiom_temp)
            else:
                e_itr = e.iterator()
                while e_itr.hasNext():
                    axiom_temp = e_itr.next()
                    axioms_for_iteration.append(axiom_temp)

            for axiom_count, axiom_e in enumerate(axioms_for_iteration):
                q_exp_items = widget.model.findItems('Explanation - ' + str(explanation_count + 1),
                                                     flags=QtCore.Qt.MatchExactly, column=0)
                if len(q_exp_items) != 1:
                    LOGGER.error('multiple or 0 QStandardItems found for q_exp_item')

                self.sgnFakeAxiomAdded.emit(q_exp_items[0], axiom_e.toString())
                q_axiom_item = q_exp_items[0].child(axiom_count, 0)
                nodes_and_edges = self.project.axioms_to_nodes_edges_mapping[q_axiom_item.text()]
                nodes_to_add_in_widget = set()
                edges_to_add_in_widget = set()

                for ne in nodes_and_edges:
                    if 'eddy.core.items.nodes' in str(type(ne)):
                        nodes_to_add_in_widget.add(ne)
                    elif 'eddy.core.items.edges' in str(type(ne)):
                        edges_to_add_in_widget.add(ne)

                for node in nodes_to_add_in_widget:
                    self.sgnFakeItemAdded.emit(node.diagram, node, q_axiom_item)

                for edge in edges_to_add_in_widget:
                    self.sgnFakeItemAdded.emit(edge.diagram, edge, q_axiom_item)

        disconnect(self.sgnFakeExplanationAdded, widget.doAddExplanation)
        disconnect(self.sgnFakeAxiomAdded, widget.doAddAxiom)
        disconnect(self.sgnFakeItemAdded, widget.doAddNodeOREdge)

        # SHOW THE PLUGIN DOCK WIDGET
        if not self.widget('explanation_explorer_dock').isVisible():
            self.widget('explanation_explorer_dock').toggleViewAction().trigger()
            self.widget('explanation_explorer_dock').raise_()

    #############################################
    #   HOOKS
    #################################

    def dispose(self):
        """
        Executed whenever the plugin is going to be destroyed.
        """
        # DISCONNECT FROM CURRENT PROJECT
        widget = self.widget('explanation_explorer')
        self.debug('Disconnecting from project: %s', self.project.name)
        disconnect(self.project.sgnItemAdded, widget.doAddNode)
        disconnect(self.project.sgnItemRemoved, widget.doRemoveNode)

        # DISCONNECT FROM ACTIVE SESSION
        self.debug('Disconnecting from active session')
        disconnect(self.session.sgnReady, self.onSessionReady)
        disconnect(self.session.sgnConsistencyCheckStarted, self.onConsistencyCheckStarted)
        disconnect(self.session.sgnConsistencyCheckReset, self.onConsistencyCheckReset)
        disconnect(self.session.sgnPerfectOntology, self.onPerfectOntology)
        disconnect(self.session.sgnInconsistentOntology, self.onInconsistentOntology)
        disconnect(self.session.sgnUnsatisfiableEntities, self.onUnsatisfiableEntities)

        # REMOVE DOCKING AREA WIDGET MENU ENTRY
        self.debug('Removing docking area widget toggle from "view" menu')
        menu = self.session.menu('view')
        menu.removeAction(self.widget('explanation_explorer_dock').toggleViewAction())

        # UNINSTALL THE PALETTE DOCK WIDGET
        self.debug('Uninstalling docking area widget')
        self.session.removeDockWidget(self.widget('explanation_explorer_dock'))

    def start(self):
        """
        Perform initialization tasks for the plugin.
        """
        # INITIALIZE THE WIDGET
        self.debug('Creating Explanation explorer widget')
        widget = ExplanationExplorerWidget(self)
        widget.setObjectName('explanation_explorer')
        self.addWidget(widget)

        # CREATE DOCKING AREA WIDGET
        self.debug('Creating docking area widget')
        widget = DockWidget('Explanation Explorer', QtGui.QIcon(':icons/18/ic_explore_black'), self.session)
        widget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea|QtCore.Qt.BottomDockWidgetArea)
        widget.setObjectName('explanation_explorer_dock')
        widget.setWidget(self.widget('explanation_explorer'))
        self.addWidget(widget)

        # CREATE ENTRY IN VIEW MENU
        self.debug('Creating docking area widget toggle in "view" menu')
        menu = self.session.menu('view')
        menu.addAction(self.widget('explanation_explorer_dock').toggleViewAction())

        # CONFIGURE SIGNALS
        self.debug('Configuring session specific signals')
        connect(self.session.sgnReady, self.onSessionReady)
        connect(self.session.sgnConsistencyCheckStarted, self.onConsistencyCheckStarted)
        connect(self.session.sgnConsistencyCheckReset, self.onConsistencyCheckReset)
        connect(self.session.sgnPerfectOntology, self.onPerfectOntology)
        connect(self.session.sgnInconsistentOntology, self.onInconsistentOntology)
        connect(self.session.sgnUnsatisfiableEntities, self.onUnsatisfiableEntities)

        # INSTALL DOCKING AREA WIDGET
        self.debug('Installing docking area widget')
        self.session.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.widget('explanation_explorer_dock'))

        # HIDE THE DOCK WIDGET BY DEFAULT
        if self.widget('explanation_explorer_dock').isVisible():
            self.widget('explanation_explorer_dock').toggleViewAction().trigger()


class ExplanationExplorerWidget(QtWidgets.QWidget):
    """
    This class implements the Explanation explorer used to list Explanation predicates.
    """
    sgnItemClicked = QtCore.pyqtSignal('QGraphicsItem')
    sgnItemDoubleClicked = QtCore.pyqtSignal('QGraphicsItem')
    sgnItemRightClicked = QtCore.pyqtSignal('QGraphicsItem')
    sgnFakeItemAdded = QtCore.pyqtSignal('QGraphicsScene', 'QGraphicsItem')
    sgnColourItem = QtCore.pyqtSignal('QStandardItem')

    def __init__(self, plugin):
        """
        Initialize the Explanation explorer widget.
        :type plugin: Session
        """
        super().__init__(plugin.session)

        self.plugin = plugin

        self.iconAttribute = QtGui.QIcon(':/icons/18/ic_treeview_attribute')
        self.iconConcept = QtGui.QIcon(':/icons/18/ic_treeview_concept')
        self.iconInstance = QtGui.QIcon(':/icons/18/ic_treeview_instance')
        self.iconRole = QtGui.QIcon(':/icons/18/ic_treeview_role')
        self.iconValue = QtGui.QIcon(':/icons/18/ic_treeview_value')

        self.search = StringField(self)
        self.search.setAcceptDrops(False)
        self.search.setClearButtonEnabled(True)
        self.search.setPlaceholderText('Search...')
        self.search.setFixedHeight(30)
        self.model = QtGui.QStandardItemModel(self)
        self.proxy = QtCore.QSortFilterProxyModel(self)
        self.proxy.setDynamicSortFilter(False)
        self.proxy.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxy.setSortCaseSensitivity(QtCore.Qt.CaseSensitive)
        self.proxy.setSourceModel(self.model)
        self.ontoview = ExplanationExplorerView(self)
        self.ontoview.setModel(self.proxy)
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.search)
        self.mainLayout.addWidget(self.ontoview)

        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(216)

        self.setStyleSheet("""
            QLineEdit,
            QLineEdit:editable,
            QLineEdit:hover,
            QLineEdit:pressed,
            QLineEdit:focus {
              border: none;
              border-radius: 0;
              background: #FFFFFF;
              color: #000000;
              padding: 4px 4px 4px 4px;
            }
        """)

        header = self.ontoview.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        connect(self.ontoview.doubleClicked, self.onItemDoubleClicked)
        connect(self.ontoview.pressed, self.onItemPressed)
        connect(self.search.textChanged, self.doFilterItem)
        connect(self.sgnItemDoubleClicked, self.session.doFocusItem)
        connect(self.sgnItemRightClicked, self.session.doFocusItem)

        connect(self.sgnColourItem, self.doColorItems)

    #############################################
    #   PROPERTIES
    #################################

    @property
    def project(self):
        """
        Returns the reference to the active project.
        :rtype: Session
        """
        return self.session.project

    @property
    def session(self):
        """
        Returns the reference to the active session.
        :rtype: Session
        """
        return self.plugin.parent()

    #############################################
    #   EVENTS
    #################################

    def paintEvent(self, paintEvent):
        """
        This is needed for the widget to pick the stylesheet.
        :type paintEvent: QPaintEvent
        """
        option = QtWidgets.QStyleOption()
        option.initFrom(self)
        painter = QtGui.QPainter(self)
        style = self.style()
        style.drawPrimitive(QtWidgets.QStyle.PE_Widget, option, painter, self)

    #############################################
    #   SLOTS
    #################################

    @QtCore.pyqtSlot('QStandardItem')
    def doColorItems(self, item):
        row_count = item.rowCount()
        self.session.doResetConsistencyCheck(updateNodes=False, clearReasonerCache=False)
        self.project.nodes_or_edges_of_axioms_to_display_in_widget = []
        self.project.nodes_or_edges_of_explanations_to_display_in_widget = []

        for r in range(row_count):
            child = item.child(r, 0)
            node_or_edge_or_axiom = child.data()

            if 'eddy.core.items' in str(type(node_or_edge_or_axiom)):
                # item is an axiom
                # child is a node or an edge
                explanation_item = item.parent()
                explanation_item_row_count = explanation_item.rowCount()

                for r2 in range(0, explanation_item_row_count):
                    child_of_explanation_item = explanation_item.child(r2, 0)
                    child_of_explanation_item_row_count = child_of_explanation_item.rowCount()

                    for r3 in range(0, child_of_explanation_item_row_count):
                        nephew_or_child = child_of_explanation_item.child(r3, 0)
                        nephew_or_child_data = nephew_or_child.data()

                        if 'eddy.core.items' in str(type(nephew_or_child_data)):
                            if nephew_or_child_data.id == node_or_edge_or_axiom.id:
                                # if (nephew_or_child_data.text() == nephew_or_child_data.text()):
                                # print('nephew_or_child_data not coloured - ',nephew_or_child_data)
                                pass
                            else:
                                self.project.nodes_or_edges_of_explanations_to_display_in_widget.append(
                                    nephew_or_child_data)

                self.project.nodes_or_edges_of_axioms_to_display_in_widget.append(node_or_edge_or_axiom)

            if (str(type(node_or_edge_or_axiom)) == '<class \'str\'>') or (str(type(node_or_edge_or_axiom)) == 'str'):
                # item is an explanation
                # child is an axiom
                # colour all the nodes and edges involved in the axiom
                row_count_2 = child.rowCount()

                for r2 in range(0, row_count_2):
                    grand_child = child.child(r2, 0)
                    node_or_edge = grand_child.data()

                    if 'eddy.core.items' in str(type(node_or_edge)):
                        self.project.nodes_or_edges_of_explanations_to_display_in_widget.append(node_or_edge)

        self.project.colour_items_in_case_of_unsatisfiability_or_inconsistent_ontology()

    @QtCore.pyqtSlot(str)
    def doAddExplanation(self, explanation_number):
        explanation_number_to_add = QtGui.QStandardItem('Explanation - ' + explanation_number)
        explanation_number_to_add.setData(explanation_number)
        self.model.appendRow(explanation_number_to_add)
        self.proxy.sort(0, QtCore.Qt.AscendingOrder)

    @QtCore.pyqtSlot('QStandardItem', str)
    def doAddAxiom(self, q_item, axiom):
        axiom_to_add = QtGui.QStandardItem(axiom)
        axiom_to_add.setData(axiom)
        q_item.appendRow(axiom_to_add)
        self.proxy.sort(0, QtCore.Qt.AscendingOrder)

    @QtCore.pyqtSlot('QGraphicsScene', 'QGraphicsItem', 'QStandardItem')
    def doAddNodeOREdge(self, diagram, node_or_edge, q_item):
        icon = None

        if 'eddy.core.items.nodes' in str(type(node_or_edge)):
            button_name = str(node_or_edge.id) + ':' + str(node_or_edge.text())
            icon = self.iconFor(node_or_edge)
        elif 'eddy.core.items.edges' in str(type(node_or_edge)):
            button_name = str(node_or_edge.id) + ':' + str(node_or_edge.type()).replace('Item.', '')

        node_or_edge_to_append = QtGui.QStandardItem(button_name)

        if icon is not None:
            node_or_edge_to_append.setIcon(icon)

        node_or_edge_to_append.setData(node_or_edge)
        q_item.appendRow(node_or_edge_to_append)

    @QtCore.pyqtSlot('QGraphicsScene', 'QGraphicsItem')
    def doAddNode(self, diagram, node):
        """
        Add a node in the tree view.
        :type diagram: QGraphicsScene
        :type node: AbstractItem
        """
        if node.type() in {Item.ConceptNode, Item.RoleNode, Item.AttributeNode, Item.IndividualNode}:
            parent = self.parentFor(node)
            if not parent:
                parent = QtGui.QStandardItem(self.parentKey(node))
                parent.setIcon(self.iconFor(node))
                self.model.appendRow(parent)
                self.proxy.sort(0, QtCore.Qt.AscendingOrder)
            child = QtGui.QStandardItem(self.childKey(diagram, node))
            child.setData(node)
            parent.appendRow(child)
            self.proxy.sort(0, QtCore.Qt.AscendingOrder)

    @QtCore.pyqtSlot()
    def doClear(self):
        """
        Clear all the nodes in the tree view.
        """
        self.search.clear()
        self.model.clear()
        self.ontoview.update()

    @QtCore.pyqtSlot(str)
    def doFilterItem(self, key):
        """
        Executed when the search box is filled with data.
        :type key: str
        """
        self.proxy.setFilterFixedString(key)
        self.proxy.sort(QtCore.Qt.AscendingOrder)

    @QtCore.pyqtSlot('QGraphicsScene', 'QGraphicsItem')
    def doRemoveNode(self, diagram, node):
        """
        Remove a node from the tree view.
        :type diagram: QGraphicsScene
        :type node: AbstractItem
        """
        if node.type() in {Item.ConceptNode, Item.RoleNode, Item.AttributeNode, Item.IndividualNode}:
            parent = self.parentFor(node)
            if parent:
                child = self.childFor(parent, diagram, node)
                if child:
                    parent.removeRow(child.index().row())
                if not parent.rowCount():
                    self.model.removeRow(parent.index().row())

    @QtCore.pyqtSlot('QModelIndex')
    def onItemDoubleClicked(self, index):
        """
        Executed when an item in the treeview is double clicked.
        :type index: QModelIndex
        """
        # noinspection PyArgumentList
        if QtWidgets.QApplication.mouseButtons() & QtCore.Qt.LeftButton:
            item = self.model.itemFromIndex(self.proxy.mapToSource(index))
            if item and item.data():
                if (str(type(item.data())) == '<class \'str\'>') or (str(type(item.data())) == 'str'):
                    # item is an explanation or an axiom
                    self.sgnColourItem.emit(item)
                else:
                    self.sgnItemDoubleClicked.emit(item.data())

    @QtCore.pyqtSlot('QModelIndex')
    def onItemPressed(self, index):
        """
        Executed when an item in the treeview is clicked.
        :type index: QModelIndex
        """
        # noinspection PyArgumentList
        if QtWidgets.QApplication.mouseButtons() & QtCore.Qt.LeftButton:
            item = self.model.itemFromIndex(self.proxy.mapToSource(index))
            if item and item.data():
                if (str(type(item.data())) == '<class \'str\'>') or (str(type(item.data())) == 'str'):
                    # item is an explanation or an axiom
                    self.sgnColourItem.emit(item)
                else:
                    self.sgnItemClicked.emit(item.data())

    #############################################
    #   INTERFACE
    #################################

    def childFor(self, parent, diagram, node):
        """
        Search the item representing this node among parent children.
        :type parent: QtGui.QStandardItem
        :type diagram: Diagram
        :type node: AbstractNode
        """
        key = self.childKey(diagram, node)
        for i in range(parent.rowCount()):
            child = parent.child(i)
            if child.text() == key:
                return child
        return None

    @staticmethod
    def childKey(diagram, node):
        """
        Returns the child key (text) used to place the given node in the treeview.
        :type diagram: Diagram
        :type node: AbstractNode
        :rtype: str
        """
        predicate = node.text().replace('\n', '')
        diagram = rstrip(diagram.name, File.Graphol.extension)
        return '{0} ({1} - {2})'.format(predicate, diagram, node.id)

    def iconFor(self, node):
        """
        Returns the icon for the given node.
        :type node:
        """
        if node.type() is Item.AttributeNode:
            return self.iconAttribute
        if node.type() is Item.ConceptNode:
            return self.iconConcept
        if node.type() is Item.IndividualNode:
            if node.identity() is Identity.Individual:
                return self.iconInstance
            if node.identity() is Identity.Value:
                return self.iconValue
        if node.type() is Item.RoleNode:
            return self.iconRole

    def parentFor(self, node):
        """
        Search the parent element of the given node.
        :type node: AbstractNode
        :rtype: QtGui.QStandardItem
        """
        for i in self.model.findItems(self.parentKey(node), QtCore.Qt.MatchExactly):
            n = i.child(0).data()
            if node.type() is n.type():
                return i
        return None

    @staticmethod
    def parentKey(node):
        """
        Returns the parent key (text) used to place the given node in the treeview.
        :type node: AbstractNode
        :rtype: str
        """
        return node.text().replace('\n', '')

    def sizeHint(self):
        """
        Returns the recommended size for this widget.
        :rtype: QtCore.QSize
        """
        return QtCore.QSize(216, 266)


class ExplanationExplorerView(QtWidgets.QTreeView):
    """
    This class implements the Explanation explorer tree view.
    """

    def __init__(self, widget):
        """
        Initialize the Explanation explorer view.
        :type widget: ExplanationExplorerWidget
        """
        super().__init__(widget)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.setEditTriggers(QtWidgets.QTreeView.NoEditTriggers)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setHeaderHidden(True)
        self.setHorizontalScrollMode(QtWidgets.QTreeView.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setSelectionMode(QtWidgets.QTreeView.SingleSelection)
        self.setSortingEnabled(True)
        self.setWordWrap(True)

    #############################################
    #   PROPERTIES
    #################################

    @property
    def session(self):
        """
        Returns the reference to the Session holding the ExplanationExplorer widget.
        :rtype: Session
        """
        return self.widget.session

    @property
    def widget(self):
        """
        Returns the reference to the ExplanationExplorer widget.
        :rtype: ExplanationExplorerWidget
        """
        return self.parent()

    #############################################
    #   EVENTS
    #################################

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the treeview.
        :type mouseEvent: QMouseEvent
        """
        self.clearSelection()
        super().mousePressEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the tree view.
        :type mouseEvent: QMouseEvent
        """
        if mouseEvent.button() == QtCore.Qt.RightButton:
            index = first(self.selectedIndexes())
            if index:
                model = self.model().sourceModel()
                index = self.model().mapToSource(index)
                item = model.itemFromIndex(index)
                node_edge_or_axiom = item.data()

                if 'eddy.core.items.nodes' in str(type(item.data())):
                    self.widget.sgnItemRightClicked.emit(node_edge_or_axiom)
                    menu = self.session.mf.create(node_edge_or_axiom.diagram, [node_edge_or_axiom])
                    menu.exec_(mouseEvent.screenPos().toPoint())

        super().mouseReleaseEvent(mouseEvent)

    #############################################
    #   INTERFACE
    #################################

    def sizeHintForColumn(self, column):
        """
        Returns the size hint for the given column.
        This will make the column of the treeview as wide as the widget that contains the view.
        :type column: int
        :rtype: int
        """
        return max(super().sizeHintForColumn(column), self.viewport().width())
