# -*- coding: utf-8 -*-

##########################################################################
#                                                                        #
#  Eddy: a graphical editor for the construction of Graphol ontologies.  #
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
#  A.Ruberti at Sapienza University of Rome: http://www.dis.uniroma1.it/ #
#                                                                        #
#     - Domenico Lembo <lembo@dis.uniroma1.it>                           #
#     - Valerio Santarelli <santarelli@dis.uniroma1.it>                  #
#     - Domenico Fabio Savo <savo@dis.uniroma1.it>                       #
#     - Marco Console <console@dis.uniroma1.it>                          #
#                                                                        #
##########################################################################


from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPainterPath

from eddy.core.datatypes import Font, Item, XsdDatatype, DiagramMode, Identity
from eddy.core.items.nodes.common.base import AbstractNode
from eddy.core.items.nodes.common.label import Label


class ValueDomainNode(AbstractNode):
    """
    This class implements the 'Value-Domain' node.
    """
    identities = {Identity.DataRange}
    item = Item.ValueDomainNode
    minheight = 40
    minwidth = 90
    padding = 16
    radius = 8

    # noinspection PyTypeChecker
    def __init__(self, width=minwidth, height=minheight, brush='#fcfcfc', **kwargs):
        """
        Initialize the Value-Domain node.
        :type width: int
        :type height: int
        :type brush: T <= QBrush | QColor | Color | tuple | list | bytes | unicode
        """
        super().__init__(**kwargs)
        self.brush = brush
        self.pen = QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine)
        self.polygon = self.createRect(self.minwidth, self.minheight)
        self.label = Label('xsd:string', movable=False, editable=False, parent=self)
        self.updateRect()

    ####################################################################################################################
    #                                                                                                                  #
    #   PROPERTIES                                                                                                     #
    #                                                                                                                  #
    ####################################################################################################################

    @property
    def datatype(self):
        """
        Returns the datatype associated with this node.
        :rtype: XsdDatatype
        """
        return XsdDatatype.forValue(self.text())

    @property
    def identity(self):
        """
        Returns the identity of the current node.
        :rtype: Identity
        """
        return Identity.DataRange

    @identity.setter
    def identity(self, identity):
        """
        Set the identity of the current node.
        :type identity: Identity
        """
        pass

    ####################################################################################################################
    #                                                                                                                  #
    #   INTERFACE                                                                                                      #
    #                                                                                                                  #
    ####################################################################################################################

    def copy(self, scene):
        """
        Create a copy of the current item.
        :type scene: DiagramScene
        """
        kwargs = {
            'brush': self.brush,
            'description': self.description,
            'height': self.height(),
            'id': self.id,
            'url': self.url,
            'width': self.width(),
        }
        node = scene.itemFactory.create(item=self.item, scene=scene, **kwargs)
        node.setPos(self.pos())
        node.setText(self.text())
        node.setTextPos(node.mapFromScene(self.mapToScene(self.textPos())))
        return node

    def height(self):
        """
        Returns the height of the shape.
        :rtype: int
        """
        return self.polygon.height()

    def updateRect(self):
        """
        Update current shape rect according to the selected datatype.
        Will also center the shape text after the width adjustment.
        """
        shape_w = max(self.label.width() + self.padding, self.minwidth)
        self.polygon = self.createRect(shape_w, self.minheight)
        self.updateTextPos()
        self.updateEdges()

    def width(self):
        """
        Returns the width of the shape.
        :rtype: int
        """
        return self.polygon.width()

    ####################################################################################################################
    #                                                                                                                  #
    #   AUXILIARY METHODS                                                                                              #
    #                                                                                                                  #
    ####################################################################################################################

    @staticmethod
    def createRect(shape_w, shape_h):
        """
        Returns the initialized rect according to the given width/height.
        :type shape_w: int
        :type shape_h: int
        :rtype: QRectF
        """
        return QRectF(-shape_w / 2, -shape_h / 2, shape_w, shape_h)

    ####################################################################################################################
    #                                                                                                                  #
    #   GEOMETRY                                                                                                       #
    #                                                                                                                  #
    ####################################################################################################################

    def boundingRect(self):
        """
        Returns the shape bounding rectangle.
        :rtype: QRectF
        """
        o = self.selectionOffset
        return self.polygon.adjusted(-o, -o, o, o)

    def painterPath(self):
        """
        Returns the current shape as QPainterPath (used for collision detection).
        :rtype: QPainterPath
        """
        path = QPainterPath()
        path.addRoundedRect(self.polygon, self.radius, self.radius)
        return path

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        :rtype: QPainterPath
        """
        path = QPainterPath()
        path.addRoundedRect(self.polygon, self.radius, self.radius)
        return path

    ####################################################################################################################
    #                                                                                                                  #
    #   LABEL SHORTCUTS                                                                                                #
    #                                                                                                                  #
    ####################################################################################################################

    def textPos(self):
        """
        Returns the current label position in item coordinates.
        :rtype: QPointF
        """
        return self.label.pos()

    def text(self):
        """
        Returns the label text.
        :rtype: str
        """
        return self.label.text()

    def setTextPos(self, pos):
        """
        Set the label position.
        :type pos: QPointF
        """
        self.label.setPos(pos)

    def setText(self, text):
        """
        Set the label text.
        :type text: str
        """
        datatype = XsdDatatype.forValue(text) or XsdDatatype.string
        self.label.setText(datatype.value)
        self.updateRect()

    def updateTextPos(self, *args, **kwargs):
        """
        Update the label position.
        """
        self.label.updatePos(*args, **kwargs)

    ####################################################################################################################
    #                                                                                                                  #
    #   DRAWING                                                                                                        #
    #                                                                                                                  #
    ####################################################################################################################

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        :type painter: QPainter
        :type option: int
        :type widget: QWidget
        """
        scene = self.scene()

        if self.isSelected():
            painter.setPen(self.selectionPen)
            painter.drawRect(self.boundingRect())

        if scene.mode is DiagramMode.EdgeInsert and scene.mouseOverNode is self:

            edge = scene.command.edge
            brush = self.brushConnectionOk
            if not scene.validator.valid(edge.source, edge, scene.mouseOverNode):
                brush = self.brushConnectionBad

            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            painter.drawRoundedRect(self.boundingRect(), self.radius, self.radius)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawRoundedRect(self.polygon, self.radius, self.radius)

    @classmethod
    def image(cls, **kwargs):
        """
        Returns an image suitable for the palette.
        :rtype: QPixmap
        """
        # Initialize the pixmap
        pixmap = QPixmap(kwargs['w'], kwargs['h'])
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)

        # Initialize the shape
        rect = cls.createRect(54, 34)

        # Draw the rectangle
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin))
        painter.setBrush(QColor(252, 252, 252))
        painter.translate(kwargs['w'] / 2, kwargs['h'] / 2)
        painter.drawRoundedRect(rect, 6.0, 6.0)

        # Draw the text within the rectangle
        painter.setFont(Font('Arial', 10, Font.Light))
        painter.drawText(rect, Qt.AlignCenter, 'xsd:string')

        return pixmap