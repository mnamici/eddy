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
from PyQt5 import QtPrintSupport

from eddy.core.datatypes.system import File
from eddy.core.exporters.common import AbstractDiagramExporter
from eddy.core.items.common import AbstractItem
from eddy.core.output import getLogger
from eddy.ui.dialogs import DiagramsSelectionDialog
from eddy.core.datatypes.owl import OWLStandardIRIPrefixPairsDict
from eddy.core.datatypes.qt import Font
from eddy.core.datatypes.graphol import Item
from eddy.core.datatypes.graphol import Special

import math


LOGGER = getLogger()


class PdfDiagramExporter(AbstractDiagramExporter):
    """
    Extends AbstractDiagramExporter with facilities to export the structure of Graphol diagrams in PDF format.
    """
    def __init__(self, diagram, session=None):
        """
        Initialize the Pdf Exporter.
        :type session: Session
        """
        super().__init__(diagram, session)

        self.project = diagram.project
        self.success = False

    def append_row_and_column_to_table_2(self,list_inp,entity=None):

        item_predicate_name = QtWidgets.QTableWidgetItem()
        item_predicate_name.setText(list_inp[0])
        self.table_2.setItem(self.table_2.rowCount() - 1, 0, item_predicate_name)

        if list_inp[1] is False:
            item_predicate_attribute_A = QtWidgets.QTableWidgetItem()
            self.table_2.setItem(self.table_2.rowCount() - 1, 1, item_predicate_attribute_A)
        else:
            checkbox_A = QtWidgets.QCheckBox()
            checkbox_A.setEnabled(True)
            checkbox_A.setChecked(True)
            self.table_2.setCellWidget(self.table_2.rowCount() - 1, 1, checkbox_A)

        if list_inp[2] is False:
            item_predicate_attribute_B = QtWidgets.QTableWidgetItem()
            self.table_2.setItem(self.table_2.rowCount() - 1, 2, item_predicate_attribute_B)
        else:
            checkbox_B = QtWidgets.QCheckBox()
            checkbox_B.setEnabled(True)
            checkbox_B.setChecked(True)
            self.table_2.setCellWidget(self.table_2.rowCount() - 1, 2, checkbox_B)

        if list_inp[3] is False:
            item_predicate_attribute_C = QtWidgets.QTableWidgetItem()
            self.table_2.setItem(self.table_2.rowCount() - 1, 3, item_predicate_attribute_C)
        else:
            checkbox_C = QtWidgets.QCheckBox()
            checkbox_C.setEnabled(True)
            checkbox_C.setChecked(True)
            #hl = QtWidgets.QHBoxLayout()
            #hl.addSpacing(6)
            #hl.addWidget(checkbox_C)
            #hl.addSpacing(6)
            #checkbox_C.setLayout(hl)
            self.table_2.setCellWidget(self.table_2.rowCount() - 1, 3, checkbox_C)

        if list_inp[4] is False:
            item_predicate_attribute_D = QtWidgets.QTableWidgetItem()
            self.table_2.setItem(self.table_2.rowCount() - 1, 4, item_predicate_attribute_D)
        else:
            checkbox_D = QtWidgets.QCheckBox()
            checkbox_D.setEnabled(True)
            checkbox_D.setChecked(True)
            self.table_2.setCellWidget(self.table_2.rowCount() - 1, 4, checkbox_D)

        if list_inp[5] is False:
            item_predicate_attribute_E = QtWidgets.QTableWidgetItem()
            self.table_2.setItem(self.table_2.rowCount() - 1, 5, item_predicate_attribute_E)
        else:
            checkbox_E = QtWidgets.QCheckBox()
            checkbox_E.setEnabled(True)
            checkbox_E.setChecked(True)
            self.table_2.setCellWidget(self.table_2.rowCount() - 1, 5, checkbox_E)

        if list_inp[6] is False:
            item_predicate_attribute_F = QtWidgets.QTableWidgetItem()
            self.table_2.setItem(self.table_2.rowCount() - 1, 6, item_predicate_attribute_F)
        else:
            checkbox_F = QtWidgets.QCheckBox()
            checkbox_F.setEnabled(True)
            checkbox_F.setChecked(True)
            self.table_2.setCellWidget(self.table_2.rowCount() - 1, 6, checkbox_F)

        if list_inp[7] is False:
            item_predicate_attribute_G = QtWidgets.QTableWidgetItem()
            self.table_2.setItem(self.table_2.rowCount() - 1, 7, item_predicate_attribute_G)
        else:
            checkbox_G = QtWidgets.QCheckBox()
            checkbox_G.setEnabled(True)
            checkbox_G.setChecked(True)
            self.table_2.setCellWidget(self.table_2.rowCount() - 1, 7, checkbox_G)

        self.table_2.setRowCount(self.table_2.rowCount() + 1)

    def append_row_and_column_to_table(self,iri,prefix,brush,bold=None):

        item_iri = QtWidgets.QTableWidgetItem()
        item_iri.setText(iri)

        if brush is not None:
            item_iri.setBackground(brush)

        item_prefix = QtWidgets.QTableWidgetItem()
        item_prefix.setText(prefix)

        if bold:
            font_iri = QtGui.QFont(item_iri.text())
            font_iri.setBold(True)
            item_iri.setFont(font_iri)

            font_prefix = QtGui.QFont(item_prefix.text())
            font_prefix.setBold(True)
            item_prefix.setFont(font_prefix)

        if brush is not None:
            item_prefix.setBackground(brush)

        self.table.setItem(self.table.rowCount() - 1, 0, item_iri)
        self.table.setItem(self.table.rowCount() - 1, 1, item_prefix)

        self.table.setRowCount(self.table.rowCount() + 1)

    def FillTableWithMetaDataInfoForRolesAndAttributes(self):

        self.table_2.setRowCount(1)
        self.table_2.setColumnCount(8)

        header_entity = QtWidgets.QTableWidgetItem()
        header_entity.setText('ENTITY')
        header_entity.setFont(Font('Roboto', 15, bold=True))
        header_entity.setTextAlignment(QtCore.Qt.AlignCenter)
        header_entity.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
        header_entity.setForeground(QtGui.QBrush(QtGui.QColor(90, 80, 80, 200)))
        header_entity.setFlags(QtCore.Qt.NoItemFlags)

        header_functional = QtWidgets.QTableWidgetItem()
        header_functional.setText('FUNCT')
        header_functional.setFont(Font('Roboto', 15, bold=True))
        header_functional.setTextAlignment(QtCore.Qt.AlignCenter)
        header_functional.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
        header_functional.setForeground(QtGui.QBrush(QtGui.QColor(90, 80, 80, 200)))
        header_functional.setFlags(QtCore.Qt.NoItemFlags)

        header_inversefunctional = QtWidgets.QTableWidgetItem()
        header_inversefunctional.setText('INV\nFUNCT')
        header_inversefunctional.setFont(Font('Roboto', 15, bold=True))
        header_inversefunctional.setTextAlignment(QtCore.Qt.AlignCenter)
        header_inversefunctional.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
        header_inversefunctional.setForeground(QtGui.QBrush(QtGui.QColor(90, 80, 80, 200)))
        header_inversefunctional.setFlags(QtCore.Qt.NoItemFlags)

        header_transitive = QtWidgets.QTableWidgetItem()
        header_transitive.setText('TRANS')
        header_transitive.setFont(Font('Roboto', 15, bold=True))
        header_transitive.setTextAlignment(QtCore.Qt.AlignCenter)
        header_transitive.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
        header_transitive.setForeground(QtGui.QBrush(QtGui.QColor(90, 80, 80, 200)))
        header_transitive.setFlags(QtCore.Qt.NoItemFlags)

        header_reflexive = QtWidgets.QTableWidgetItem()
        header_reflexive.setText('REFL')
        header_reflexive.setFont(Font('Roboto', 15, bold=True))
        header_reflexive.setTextAlignment(QtCore.Qt.AlignCenter)
        header_reflexive.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
        header_reflexive.setForeground(QtGui.QBrush(QtGui.QColor(90, 80, 80, 200)))
        header_reflexive.setFlags(QtCore.Qt.NoItemFlags)
        
        header_irreflexive = QtWidgets.QTableWidgetItem()
        header_irreflexive.setText('IRREFL')
        header_irreflexive.setFont(Font('Roboto', 15, bold=True))
        header_irreflexive.setTextAlignment(QtCore.Qt.AlignCenter)
        header_irreflexive.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
        header_irreflexive.setForeground(QtGui.QBrush(QtGui.QColor(90, 80, 80, 200)))
        header_irreflexive.setFlags(QtCore.Qt.NoItemFlags)
        
        header_symmetric = QtWidgets.QTableWidgetItem()
        header_symmetric.setText('SYMM')
        header_symmetric.setFont(Font('Roboto', 15, bold=True))
        header_symmetric.setTextAlignment(QtCore.Qt.AlignCenter)
        header_symmetric.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
        header_symmetric.setForeground(QtGui.QBrush(QtGui.QColor(90, 80, 80, 200)))
        header_symmetric.setFlags(QtCore.Qt.NoItemFlags)

        header_asymmetric = QtWidgets.QTableWidgetItem()
        header_asymmetric.setText('ASYMM')
        header_asymmetric.setFont(Font('Roboto', 15, bold=True))
        header_asymmetric.setTextAlignment(QtCore.Qt.AlignCenter)
        header_asymmetric.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
        header_asymmetric.setForeground(QtGui.QBrush(QtGui.QColor(90, 80, 80, 200)))
        header_asymmetric.setFlags(QtCore.Qt.NoItemFlags)

        self.table_2.setItem(self.table_2.rowCount() - 1, 0, header_entity)
        self.table_2.setItem(self.table_2.rowCount() - 1, 1, header_functional)
        self.table_2.setItem(self.table_2.rowCount() - 1, 2, header_inversefunctional)
        self.table_2.setItem(self.table_2.rowCount() - 1, 3, header_reflexive)
        self.table_2.setItem(self.table_2.rowCount() - 1, 4, header_irreflexive)
        self.table_2.setItem(self.table_2.rowCount() - 1, 5, header_symmetric)
        self.table_2.setItem(self.table_2.rowCount() - 1, 6, header_asymmetric)
        self.table_2.setItem(self.table_2.rowCount() - 1, 7, header_transitive)

        self.table_2.setRowCount(self.table_2.rowCount() + 1)

        wanted_attributes = ['functional','inverseFunctional','reflexive','irreflexive','symmetric','asymmetric','transitive']

        attribute_predicates_filtered = set()
        for attribute_predicate in self.project.predicates(item=Item.AttributeNode):
            if (attribute_predicate.text() in Special.return_group(Special.AllTopEntities)) or (attribute_predicate.text() in Special.return_group(Special.AllBottomEntities)):
                continue
            else:
                attribute_predicates_filtered.add(attribute_predicate.text())

        #print('len(attribute_predicates_filtered)',len(attribute_predicates_filtered))

        for attribute_predicate_txt in sorted(attribute_predicates_filtered):
            meta_data = self.project.meta(Item.AttributeNode, attribute_predicate_txt)

            #print('meta_data',meta_data)

            attributes = []

            if len(meta_data) > 0:
                for k in wanted_attributes:
                    if k in meta_data:
                        value = meta_data[k]
                    else:
                        value = False
                    attributes.append(value)
            else:
                attributes.append(False)
                attributes.append(False)
                attributes.append(False)
                attributes.append(False)
                attributes.append(False)
                attributes.append(False)
                attributes.append(False)

            #print(attribute_predicate_txt, '-', attributes)

            attribute_predicate_plus_attributes = []

            attribute_predicate_plus_attributes.append(attribute_predicate_txt)
            attribute_predicate_plus_attributes.extend(attributes)

            self.append_row_and_column_to_table_2(attribute_predicate_plus_attributes,entity='attribute')
        
        
        role_predicates_filtered = set()
        for role_predicate in self.project.predicates(item=Item.RoleNode):
            if (role_predicate.text() in Special.return_group(Special.AllTopEntities)) or (role_predicate.text() in Special.return_group(Special.AllBottomEntities)):
                continue
            else:
                role_predicates_filtered.add(role_predicate.text())

        #print('len(role_predicates_filtered)', len(role_predicates_filtered))

        for role_predicate_txt in sorted(role_predicates_filtered):
            meta_data = self.project.meta(Item.RoleNode, role_predicate_txt)

            attributes = []

            if len(meta_data) >0:
                for k in wanted_attributes:
                    value = meta_data[k]
                    attributes.append(value)
            else:
                attributes.append(False)
                attributes.append(False)
                attributes.append(False)
                attributes.append(False)
                attributes.append(False)
                attributes.append(False)
                attributes.append(False)

            #print(role_predicate_txt,'-',attributes)

            role_predicate_plus_attributes = []

            role_predicate_plus_attributes.append(role_predicate_txt)
            role_predicate_plus_attributes.extend(attributes)

            self.append_row_and_column_to_table_2(role_predicate_plus_attributes)

        self.table_2.setRowCount(self.table_2.rowCount() - 1)

    def FillTableWithIRIPrefixNodesDictionaryKeysAndValues(self):

        self.table.setRowCount(1)
        self.table.setColumnCount(2)

        header_iri = QtWidgets.QTableWidgetItem()
        header_iri.setText('IRI')
        header_iri.setFont(Font('Roboto', 15, bold=True))
        header_iri.setTextAlignment(QtCore.Qt.AlignCenter)
        header_iri.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
        header_iri.setForeground(QtGui.QBrush(QtGui.QColor(90, 80, 80, 200)))
        header_iri.setFlags(QtCore.Qt.NoItemFlags)

        header_prefix = QtWidgets.QTableWidgetItem()
        header_prefix.setText('PREFIX')
        header_prefix.setFont(Font('Roboto', 15, bold=True))
        header_prefix.setTextAlignment(QtCore.Qt.AlignCenter)
        header_prefix.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
        header_prefix.setForeground(QtGui.QBrush(QtGui.QColor(90, 80, 80, 200)))
        header_prefix.setFlags(QtCore.Qt.NoItemFlags)


        self.table.setItem(self.table.rowCount() - 1, 0, header_iri)
        self.table.setItem(self.table.rowCount() - 1, 1, header_prefix)

        self.table.setRowCount(self.table.rowCount() + 1)

        for iri in self.project.IRI_prefixes_nodes_dict.keys():
            if iri in OWLStandardIRIPrefixPairsDict.std_IRI_prefix_dict.keys():
                standard_prefixes = self.project.IRI_prefixes_nodes_dict[iri][0]
                standard_prefix = standard_prefixes[0]
                self.append_row_and_column_to_table(iri, standard_prefix, None)
                                                    #QtGui.QBrush(QtGui.QColor(50, 50, 205, 50)))

        for iri in sorted(self.project.IRI_prefixes_nodes_dict.keys()):

            if iri in OWLStandardIRIPrefixPairsDict.std_IRI_prefix_dict.keys():
                continue

            prefixes = self.project.IRI_prefixes_nodes_dict[iri][0]

            if len(prefixes) > 0:
                for p in prefixes:
                    if iri == self.project.iri:
                        self.append_row_and_column_to_table(iri, p, None, bold=True)
                    else:
                        self.append_row_and_column_to_table(iri, p, None)
            else:
                if 'display_in_widget' in self.project.IRI_prefixes_nodes_dict[iri][2]:
                    if iri == self.project.iri:
                        self.append_row_and_column_to_table(iri, '', None, bold=True)
                    else:
                        self.append_row_and_column_to_table(iri, '', None)

        #self.append_row_and_column_to_table('', '', None)

        self.table.setRowCount(self.table.rowCount() - 1)

    def set_properties_of_table(self,table):

        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def split_table(self,table,n):

        if n == 1:
            return [table]

        headers = []

        for c in range(0,table.columnCount()):
            cell_widget = table.item(0,c)
            headers.append(cell_widget)

        #print('table.rowCount()',table.rowCount())

        #table.rowCount()-1 as 1st row contains headers
        base_row_count = math.floor((table.rowCount()-1)/n)
        remainder = (table.rowCount()-1) % n

        row_nos_of_tables = []
        max = 1
        for i in range(0,n):

            rows = []
            for j in range(max,max+base_row_count):
                rows.append(j)

            r=0
            if remainder>0:
                rows.append(max+base_row_count)
                remainder = remainder-1
                r=1

            max = max + base_row_count + r

            row_nos_of_tables.append(rows)


        tables = []

        all_predicates_in_table_list = []
        all_predicates_in_table_set = set()

        for r in range(0,table.rowCount()):
            pred = table.item(r,0).text()
            all_predicates_in_table_list.append(pred)
            all_predicates_in_table_set.add(pred)

        all_predicates_in_split_tables_list = []
        all_predicates_in_split_tables_set = set()

        for i in range(0,n):
            t = QtWidgets.QTableWidget()
            self.set_properties_of_table(t)

            t.setRowCount(1)
            t.setColumnCount(table.columnCount())

            for c,h in enumerate(headers):
                t.setItem(0,c,h.clone())
                t.setRowHeight(0, table.rowHeight(0))
            t.setRowCount(t.rowCount()+1)

            row_nos = row_nos_of_tables[i]

            count = 0

            for i,row_no in enumerate(row_nos):
                for col_no in range(0,table.columnCount()):

                    original_item = table.item(row_no,col_no)
                    original_cell_widget = table.cellWidget(row_no,col_no)

                    if original_cell_widget is None:
                        if original_item is None:
                            LOGGER.critical('Programming error, please contact programmer')
                        else:
                            #t.setItem(t.rowCount() - 1, col_no, original_item.clone())
                            if col_no == 0:
                                all_predicates_in_split_tables_list.append(original_item.text())
                                all_predicates_in_split_tables_set.add(original_item.text())

                            t.setItem(i + 1, col_no, original_item.clone())
                            count = count + 1
                    else:
                        checkbox = QtWidgets.QCheckBox()
                        checkbox.setEnabled(True)
                        checkbox.setChecked(True)
                        #t.setCellWidget(t.rowCount() - 1, col_no, checkbox)
                        t.setCellWidget(i + 1, col_no, checkbox)
                        count = count + 1

                #t.setRowHeight(t.rowCount()-1,table.rowHeight(row_no))
                t.setRowHeight(i + 1, table.rowHeight(row_no))
                t.setRowCount(t.rowCount() + 1)

            for col_no in range(0,t.columnCount()):
                t.setColumnWidth(col_no,table.columnWidth(col_no))

            t.setRowCount(t.rowCount() - 1)

            sum_height_rows = 0
            for r in range(0,t.rowCount()):
                sum_height_rows = sum_height_rows+t.rowHeight(r)

            t.setFixedHeight(sum_height_rows+1)
            t.setFixedWidth(table.width())

            #print('t.rowCount()',t.rowCount())
            #print('count',count)

            tables.append(t)

        #print('A',len(all_predicates_in_table_list))
        #print('B',len(all_predicates_in_table_set))

        #print('C',len(all_predicates_in_split_tables_list))
        #print('D',len(all_predicates_in_split_tables_set))

        return tables

    def split_table_if_necessary_and_render_it(self,table,printer,painter,meta_tada_table=False):

        #size of A4 sheet = 210 × 297 mm
        #if height of the table > 297/210*width of the table, split the table into 2 or more tables
        # if height of the table > 297/210*width && < 2*297/210*width of the table, split the table into 2 tables
        # if height of the table > 2*297/210*width && < 3*297/210*width of the table, split the table into 3 tables
        # if height of the table > n*297/210*width && < (n+1)*297/210*width of the table, split the table into n tables

        n=0
        if meta_tada_table is False:
            while(table.height() > (n*297/210)*table.width()):
                n=n+1
        else:
            while (table.height() > (n * 210 / 297) * table.width()):
                n = n + 1
        #n=1

        #print('n',n)

        #n is the number of pages or number of tables that will result after the split
        tables = self.split_table(table,n)

        for t in tables:

            shape = t.rect()
            # shape_2 = self.table.visibleRegion().boundingRect()

            width_to_set = (shape.width())/17
            height_to_set = (shape.height())/17

            #valid = printer.setPageSize(QtGui.QPageSize(QtCore.QSizeF(width_to_set, height_to_set), QtPrintSupport.QPrinter.DevicePixel))
            valid = printer.setPageSize(QtGui.QPageSize(QtCore.QSizeF(width_to_set+3, height_to_set+3), QtGui.QPageSize.Point))
            if not valid:
                LOGGER.critical('Error in setting page size. please contact programmer')
                return

            # 5 points = 83 QSize() units
            # 1 point = 17 QSize() units
            # 10 points = 167 QSize() units
            # 100 points = 167 QSize() units  i.e. margin with 100 points was not set correctly

            printer.setPageMargins(1,1,1,1, QtPrintSupport.QPrinter.Point)

            printer.newPage()

            if painter.isActive() or painter.begin(printer):
                t.render(painter, sourceRegion=QtGui.QRegion(shape))
    #############################################
    #   INTERFACE
    #################################

    @classmethod
    def filetype(cls):
        """
        Returns the type of the file that will be used for the export.
        :return: File
        """
        return File.Pdf

    def run(self, path):
        """
        Perform PDF document generation.
        :type path: str
        """
        #diagrams = self.diagram.project.diagrams()
        diagrams_selection_dialog = DiagramsSelectionDialog(self.diagram.project, self.session)
        diagrams_selection_dialog.exec_()
        selected_diagrams = diagrams_selection_dialog.diagrams_selected

        if len(selected_diagrams) == 0:
            return

        selected_diagrams_sorted = diagrams_selection_dialog.sort(selected_diagrams)

        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
        printer.setOutputFileName(path)
        #printer.setPaperSize(QtPrintSupport.QPrinter.Custom)
        printer.setPrinterName(self.diagram.project.name)

        size_of_pages = []

        for c, diag in enumerate(selected_diagrams_sorted):

            shape = diag.visibleRect(margin=200)

            page_size = []

            page_size.append(shape.width())
            page_size.append(shape.height())

            size_of_pages.append(page_size)

        painter = QtGui.QPainter()

        for c, diag in enumerate(selected_diagrams_sorted):

            LOGGER.info('Exporting diagram %s to %s', diag.name, path)

            shape = diag.visibleRect(margin=200)

            width_to_set = size_of_pages[c][0]
            height_to_set = size_of_pages[c][1]

            valid = printer.setPageSize(
               QtGui.QPageSize(QtCore.QSizeF(width_to_set, height_to_set), QtGui.QPageSize.Point))

            if not valid:
                LOGGER.critical('Error in setting page size. please contact programmer')
                return

            if c != 0:
                printer.newPage()

            if painter.isActive() or painter.begin(printer):
                # TURN CACHING OFF
                for item in diag.items():
                    if item.isNode() or item.isEdge():
                        item.setCacheMode(AbstractItem.NoCache)
                # RENDER THE DIAGRAM IN THE PAINTER
                diag.render(painter, source=shape)
                # TURN CACHING ON
                for item in diag.items():
                    if item.isNode() or item.isEdge():
                        item.setCacheMode(AbstractItem.DeviceCoordinateCache)
        
        LOGGER.info('All diagrams exported ')

        self.table = QtWidgets.QTableWidget()
        self.set_properties_of_table(self.table)
        self.FillTableWithIRIPrefixNodesDictionaryKeysAndValues()

        max_size = 0
        max_A = 0
        max_B = 0

        #set font size for all cells
        for r in range(0, self.table.rowCount()):
            for c in range(0,2):
                cell_item = self.table.item(r,c)

                font = cell_item.font()

                if c == 0:
                    max_A = max(max_A,len(cell_item.text()))
                if c == 1:
                    max_B = max(max_B,len(cell_item.text()))

                max_size = max(max_size,font.pointSize())

        for r in range(0, self.table.rowCount()+1):
            self.table.setRowHeight(r,max_size+5)

        self.table.setColumnWidth(0, max_A*10)
        self.table.setColumnWidth(1, max_B*30)

        self.table.setFixedWidth(self.table.columnWidth(0) + self.table.columnWidth(1))

        #does not work; self.table.horizontalScrollBar().isVisible() method always returns false
        #while(self.table.horizontalScrollBar().isVisible()):
            #make all cells visible
            #self.table.setFixedWidth(self.table.width()+1)

       #set the table width and height
        total_height_of_all_rows = 0
        for r in range(0, self.table.rowCount()):
            total_height_of_all_rows = total_height_of_all_rows + self.table.rowHeight(r)
        self.table.setFixedHeight(total_height_of_all_rows+1)

        self.split_table_if_necessary_and_render_it(self.table,printer,painter)

        LOGGER.info('IRI-Prefix table exported')

        ##############################################################
        #table for meta data of roles and attributes

        self.table_2 = QtWidgets.QTableWidget()
        self.set_properties_of_table(self.table_2)
        self.FillTableWithMetaDataInfoForRolesAndAttributes()

        for r in range(0, self.table_2.rowCount() + 1):
            self.table_2.setRowHeight(r, 20)

        self.table_2.setRowHeight(0, 40)

        total_height_of_all_rows = 0
        for r in range(0, self.table_2.rowCount()):
            total_height_of_all_rows = total_height_of_all_rows + self.table_2.rowHeight(r)
        self.table_2.setFixedHeight(total_height_of_all_rows + 1)

        max_size = 0

        #set font size for all cells
        for r in range(0, self.table.rowCount()):
            cell_item = self.table.item(r,0)
            font = cell_item.font()
            max_size = max(max_size,font.pointSize(),len(cell_item.text()))

        self.table_2.setColumnWidth(0, max_size*10)
        self.table_2.setColumnWidth(1, 70)
        self.table_2.setColumnWidth(2, 70)
        self.table_2.setColumnWidth(3, 70)
        self.table_2.setColumnWidth(4, 70)
        self.table_2.setColumnWidth(5, 70)
        self.table_2.setColumnWidth(6, 70)
        self.table_2.setColumnWidth(7, 70)

        self.table_2.setFixedWidth(self.table_2.columnWidth(0) + self.table_2.columnWidth(1) + \
                                 self.table_2.columnWidth(2) + self.table_2.columnWidth(3) + \
                                 self.table_2.columnWidth(4) + self.table_2.columnWidth(5) + \
                                 self.table_2.columnWidth(6) + self.table_2.columnWidth(7))

        self.split_table_if_necessary_and_render_it(self.table_2, printer, painter, meta_tada_table=True)

        if painter.isActive():
            # COMPLETE THE EXPORT
            painter.end()
        # OPEN THE DOCUMENT
        self.success = True