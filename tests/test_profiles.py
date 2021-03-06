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


"""
Tests for Eddy profiles.
"""

import pytest

from PyQt5 import QtCore

from eddy.core.datatypes.graphol import Item
from eddy.core.datatypes.misc import DiagramMode
from eddy.core.functions.misc import first
from eddy.core.functions.path import expandPath
from eddy.ui.session import Session


@pytest.fixture
def session(qapp, qtbot, logging_disabled):
    """
    Provide an initialized Session instance.
    """
    with logging_disabled:
        session = Session(qapp, expandPath('@tests/test_project_2'))
        session.show()
    qtbot.addWidget(session)
    qtbot.waitExposed(session, timeout=3000)
    yield session


@pytest.fixture(autouse=True)
def profile_reset(monkeypatch, mocker):
    """
    Mock profile reset.
    """
    monkeypatch.setattr('eddy.core.profiles.common.AbstractProfile.reset', mocker.Mock())


#############################################
#   UTILITY METHODS
#################################

def __give_focus_to_diagram(session, name, qtbot):
    """
    Gives focus to the given diagram.
    :type session: Session
    :type name: str
    :type qtbot: QtBot
    """
    with qtbot.waitSignal(session.sgnDiagramFocused):
        session.sgnFocusDiagram.emit(session.project.diagram(name))


def __insert_edge_between(session, item, source, target, qtbot):
    """
    Insert the given edge between the source and the target node.
    :type session: Session
    :type item: Item
    :type source: T <= tuple|AbstractNode
    :type target: T <= tuple|AbstractNode
    :type qtbot: QtBot
    """
    project = session.project
    diagram = session.mdi.activeDiagram()
    diagram.setMode(DiagramMode.EdgeAdd, item)
    view = session.mdi.activeView()
    if isinstance(source, tuple):
        source = first(project.predicates(source[0], source[1], diagram))
    if isinstance(target, tuple):
        target = first(project.predicates(target[0], target[1], diagram))
    sourcePos = view.mapFromScene(source.pos())
    targetPos = view.mapFromScene(target.pos())
    qtbot.mousePress(view.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, sourcePos)
    qtbot.mouseRelease(view.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, targetPos)


#############################################
#   INCLUSION
#################################

def test_inclusion_no_graphol_expression(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.IndividualNode, 'test:I1'), (Item.IndividualNode, 'test:I2'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: inclusion must involve two graphol expressions'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_concept_and_role(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.ConceptNode, 'test:C1'), (Item.RoleNode, 'test:R1'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: inclusion between Concept and Role'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_concept_and_attribute(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.ConceptNode, 'test:C1'), (Item.AttributeNode, 'test:A1'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: inclusion between Concept and Attribute'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_concept_and_value_domain(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.ConceptNode, 'test:C1'), (Item.ValueDomainNode, 'xsd:string'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: inclusion between Concept and Value Domain'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_role_and_attribute(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.RoleNode, 'test:R1'), (Item.AttributeNode, 'test:A1'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: inclusion between Role and Attribute'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_role_and_value_domain(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.RoleNode, 'test:R1'), (Item.ValueDomainNode, 'xsd:string'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: inclusion between Role and Value Domain'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_attribute_and_value_domain(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.AttributeNode, 'test:A1'), (Item.ValueDomainNode, 'xsd:string'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: inclusion between Attribute and Value Domain'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_role_and_union_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.UnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.RoleNode, 'test:R1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: role node and union node are not compatible'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_role_and_disjoint_union_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DisjointUnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.RoleNode, 'test:R1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: role node and disjoint union node are not compatible'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_role_and_intersection_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.IntersectionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.RoleNode, 'test:R1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: role node and intersection node are not compatible'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_attribute_and_union_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.UnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.AttributeNode, 'test:A1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: attribute node and union node are not compatible'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_attribute_and_disjoint_union_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DisjointUnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.AttributeNode, 'test:A1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: attribute node and disjoint union node are not compatible'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_attribute_and_intersection_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.IntersectionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.AttributeNode, 'test:A1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: attribute node and intersection node are not compatible'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_value_domain_expressions(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DatatypeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.ValueDomainNode, 'xsd:string'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: inclusion between value-domain expressions'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_complement_node_and_role(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.ComplementNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, source, (Item.RoleNode, 'test:R1'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid source for Role inclusion: complement node'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_complement_node_and_attribute(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.ComplementNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, source, (Item.AttributeNode, 'test:A1'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid source for Attribute inclusion: complement node'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_role_chain_node_and_role_chain_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.RoleChainNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.RoleChainNode and x is not source, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Inclusion between role chain node and role chain node is forbidden'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_role_and_role_chain_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.RoleChainNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.RoleNode, 'test:R1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Role chain nodes cannot be target of a Role inclusion'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_role_and_complement_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram49', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.ComplementNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.RoleNode, 'test:R9'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Detected unsupported operator sequence on intersection node'
    assert not session.project.profile.pvr().isValid()


def test_inclusion_between_attribute_and_complement_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram50', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.ComplementNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InclusionEdge, (Item.AttributeNode, 'test:A1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Detected unsupported operator sequence on intersection node'
    assert not session.project.profile.pvr().isValid()


#############################################
#   EQUIVALENCE
#################################

def test_equivalence_no_graphol_expression(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.IndividualNode, 'test:I1'), (Item.IndividualNode, 'test:I2'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() =='Type mismatch: equivalence must involve two graphol expressions'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_concept_and_role(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.ConceptNode, 'test:C1'), (Item.RoleNode, 'test:R1'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: equivalence between Concept and Role'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_concept_and_attribute(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.ConceptNode, 'test:C1'), (Item.AttributeNode, 'test:A1'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: equivalence between Concept and Attribute'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_concept_and_value_domain(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.ConceptNode, 'test:C1'), (Item.ValueDomainNode, 'xsd:string'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: equivalence between Concept and Value Domain'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_role_and_attribute(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.RoleNode, 'test:R1'), (Item.AttributeNode, 'test:A1'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: equivalence between Role and Attribute'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_role_and_value_domain(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.RoleNode, 'test:R1'), (Item.ValueDomainNode, 'xsd:string'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: equivalence between Role and Value Domain'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_attribute_and_value_domain(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.AttributeNode, 'test:A1'), (Item.ValueDomainNode, 'xsd:string'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: equivalence between Attribute and Value Domain'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_role_and_union_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.UnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.RoleNode, 'test:R1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: role node and union node are not compatible'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_role_and_disjoint_union_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DisjointUnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.RoleNode, 'test:R1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: role node and disjoint union node are not compatible'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_role_and_intersection_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.IntersectionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.RoleNode, 'test:R1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: role node and intersection node are not compatible'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_attribute_and_union_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.UnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.AttributeNode, 'test:A1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: attribute node and union node are not compatible'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_attribute_and_disjoint_union_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DisjointUnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.AttributeNode, 'test:A1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: attribute node and disjoint union node are not compatible'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_attribute_and_intersection_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.IntersectionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.AttributeNode, 'test:A1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: attribute node and intersection node are not compatible'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_value_domain_expressions(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DatatypeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.ValueDomainNode, 'xsd:string'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: equivalence between value-domain expressions'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_complement_node_and_role(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.ComplementNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, source, (Item.RoleNode, 'test:R1'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Equivalence is forbidden when expressing Role disjointness'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_complement_node_and_attribute(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.ComplementNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, source, (Item.AttributeNode, 'test:A1'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Equivalence is forbidden when expressing Attribute disjointness'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_role_chain_node_and_role_chain_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.RoleChainNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.RoleChainNode and x is not source, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Equivalence is forbidden in presence of a role chain node'
    assert not session.project.profile.pvr().isValid()


def test_equivalence_between_role_and_role_chain_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.RoleChainNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.EquivalenceEdge, (Item.RoleNode, 'test:R1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Equivalence is forbidden in presence of a role chain node'
    assert not session.project.profile.pvr().isValid()


#############################################
#   INPUT
#################################

def test_input_between_concept_node_and_concept_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ConceptNode, 'test:C1'), (Item.ConceptNode, 'test:C2'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Input edges can only target constructor nodes'
    assert not session.project.profile.pvr().isValid()


def test_input_between_role_node_and_role_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.RoleNode, 'test:R1'), (Item.RoleNode, 'test:R2'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Input edges can only target constructor nodes'
    assert not session.project.profile.pvr().isValid()


def test_input_between_individual_node_and_complement_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.ComplementNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.IndividualNode, 'test:I1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to complement node: Individual'
    assert not session.project.profile.pvr().isValid()


def test_input_between_individual_node_and_union_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.UnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.IndividualNode, 'test:I1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to union node: Individual'
    assert not session.project.profile.pvr().isValid()


def test_input_between_individual_node_and_intersection_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram1', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.IntersectionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.IndividualNode, 'test:I1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to intersection node: Individual'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_domain_node_and_chain_of_inclusion_connected_neutral_operators(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram18', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.UnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ValueDomainNode, 'xsd:string'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: inclusion between value-domain expressions'
    assert not session.project.profile.pvr().isValid()


def test_input_between_concept_node_and_complement_node_with_already_an_input(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram15', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.ComplementNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ConceptNode, 'test:C2'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Too many inputs to complement node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_role_node_and_complement_node_with_outgoing_edge(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram19', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.ComplementNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.RoleNode, 'test:R1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid negative Role expression'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_domain_node_and_non_neutral_union_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram16', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.UnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ValueDomainNode, 'xsd:string'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: union between Value Domain and Concept'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_domain_node_and_non_neutral_disjoint_union_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram17', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DisjointUnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ValueDomainNode, 'xsd:string'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: disjoint union between Value Domain and Concept'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_domain_node_and_non_neutral_intersection_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram2', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.IntersectionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ValueDomainNode, 'xsd:string'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: intersection between Value Domain and Concept'
    assert not session.project.profile.pvr().isValid()


def test_input_between_range_restriction_node_and_union_of_value_domain_nodes(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram23', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.RangeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.UnionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to union node: range restriction node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_concept_node_and_enumeration_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram24', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.EnumerationNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ConceptNode, 'test:C5'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to enumeration node: Concept'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_node_and_enumeration_node_with_individuals(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram4', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.EnumerationNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.IndividualNode, '"32"^^xsd:string'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to enumeration node: Value'
    assert not session.project.profile.pvr().isValid()


def test_input_between_role_chain_node_and_role_inverse_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram20', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.RoleChainNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.RoleInverseNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to role inverse node: role chain node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_role_inverse_node_and_role_inverse_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram21', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.RoleInverseNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.RoleInverseNode and x is not source, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to role inverse node: role inverse node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_role_chain_node_and_role_chain_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram22', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.RoleChainNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.RoleChainNode and x is not source, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to role chain node: role chain node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_concept_node_and_datatype_restriction_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram25', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DatatypeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ConceptNode, 'test:C6'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to datatype restriction node: concept node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_domain_node_and_datatype_restriction_node_with_datatype_connected(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram26', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DatatypeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ValueDomainNode, 'xsd:integer'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Too many value-domain nodes in input to datatype restriction node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_domain_node_and_datatype_restriction_node_with_incompatible_facet_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram6', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DatatypeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ValueDomainNode, 'xsd:string'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: datatype xsd:string is not compatible by facet xsd:maxExclusive'
    assert not session.project.profile.pvr().isValid()


def test_input_between_facet_node_and_datatype_restriction_node_with_incompatible_datatype(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram29', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.FacetNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.DatatypeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Type mismatch: facet xsd:maxExclusive is not compatible by datatype xsd:string'
    assert not session.project.profile.pvr().isValid()


def test_input_between_concept_node_and_property_assertion_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram27', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ConceptNode, 'test:C1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to property assertion node: concept node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_individual_node_and_property_assertion_node_with_already_two_inputs(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram7', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.IndividualNode, 'test:I3'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Too many inputs to property assertion node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_node_and_property_assertion_node_set_as_role_instance(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram28', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.IndividualNode, '"12"^^xsd:integer'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to Role Instance: Value'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_node_and_property_assertion_node_with_no_subject(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram51', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.IndividualNode, '"12"^^xsd:integer'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Value cannot be used as the first component of a property assertion'
    assert not session.project.profile.pvr().isValid()


def test_input_between_individual_node_and_property_assertion_node_set_as_attribute_instance(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram31', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.IndividualNode, 'test:I2'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Too many individuals in input to Attribute Instance'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_node_and_property_assertion_node_set_as_attribute_instance(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram32', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.IndividualNode, '"32"^^xsd:integer'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Too many values in input to Attribute Instance'
    assert not session.project.profile.pvr().isValid()

def test_input_between_concept_node_and_domain_restriction_node_with_filler(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram11', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DomainRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ConceptNode, 'test:C2'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Too many inputs to domain restriction node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_individual_node_and_domain_restriction_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram33', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DomainRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.IndividualNode, 'test:I4'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to domain restriction node: Individual'
    assert not session.project.profile.pvr().isValid()


def test_input_between_role_chain_node_and_domain_restriction_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram10', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.RoleChainNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.DomainRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to domain restriction node: role chain node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_property_assertion_node_and_domain_restriction_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram5', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.DomainRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to domain restriction node: property assertion node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_concept_node_and_domain_restriction_node_with_self_restriction(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram12', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DomainRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ConceptNode, 'test:C1'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid restriction type for qualified domain restriction: self'
    assert not session.project.profile.pvr().isValid()


def test_input_between_concept_node_and_domain_restriction_node_with_attribute_in_input(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram3', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DomainRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ConceptNode, 'test:C7'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid qualified domain restriction: Concept + Attribute'
    assert not session.project.profile.pvr().isValid()


def test_input_between_role_node_and_domain_restriction_node_with_value_domain_in_input(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram14', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DomainRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.RoleNode, 'test:R5'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid qualified domain restriction: Role + Value Domain'
    assert not session.project.profile.pvr().isValid()


def test_input_between_attribute_node_and_domain_restriction_node_with_self_restriction(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram30', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DomainRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.AttributeNode, 'test:A4'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Attributes do not have self'
    assert not session.project.profile.pvr().isValid()


def test_input_between_attribute_node_and_domain_restriction_node_with_concept_in_input(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram9', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DomainRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.AttributeNode, 'test:A4'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid qualified domain restriction: Attribute + Concept'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_domain_node_and_domain_restriction_node_with_self_restriction(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram8', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DomainRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ValueDomainNode, 'xsd:string'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid restriction type for qualified domain restriction: self'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_domain_node_and_domain_restriction_node_with_role_in_input(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram13', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.DomainRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ValueDomainNode, 'xsd:string'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid qualified domain restriction: Value Domain + Role'
    assert not session.project.profile.pvr().isValid()


def test_input_between_concept_node_and_range_restriction_node_with_filler(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram34', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.RangeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ConceptNode, 'test:C2'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Too many inputs to range restriction node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_domain_node_and_range_restriction_node_with_attribute_as_input(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram35', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.RangeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ValueDomainNode, 'xsd:string'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Too many inputs to attribute range restriction'
    assert not session.project.profile.pvr().isValid()


def test_input_between_individual_node_and_range_restriction_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram36', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.RangeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.IndividualNode, 'test:I4'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to range restriction node: Individual'
    assert not session.project.profile.pvr().isValid()


def test_input_between_role_chain_node_and_range_restriction_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram37', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.RoleChainNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.RangeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to range restriction node: role chain node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_property_assertion_node_and_range_restriction_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram38', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.RangeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid input to range restriction node: property assertion node'
    assert not session.project.profile.pvr().isValid()


def test_input_between_role_node_and_range_restriction_node_with_role_node_in_input(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram39', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.RangeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.RoleNode, 'test:R5'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid qualified range restriction: Role + Role'
    assert not session.project.profile.pvr().isValid()


def test_input_between_attribute_node_and_range_restriction_node_with_self_restriction(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram40', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.RangeRestrictionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.AttributeNode, 'test:A4'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Attributes do not have self'
    assert not session.project.profile.pvr().isValid()


def test_input_between_value_domain_node_and_facet_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram41', qtbot)
    num_edges_in_project = len(session.project.edges())
    target = first(filter(lambda x: x.type() is Item.FacetNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.InputEdge, (Item.ValueDomainNode, 'xsd:string'), target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Facet node cannot be target of any input'
    assert not session.project.profile.pvr().isValid()


#############################################
#   MEMBERSHIP
#################################

def test_membership_between_concept_and_concept(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram42', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.MembershipEdge, (Item.ConceptNode, 'test:C1'), (Item.ConceptNode, 'test:C2'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid source for membership edge: Concept'
    assert not session.project.profile.pvr().isValid()


def test_membership_between_individual_and_role(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram44', qtbot)
    num_edges_in_project = len(session.project.edges())
    # WHEN
    __insert_edge_between(session, Item.MembershipEdge, (Item.IndividualNode, 'test:I1'), (Item.RoleNode, 'test:R4'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid target for Concept assertion: Role'
    assert not session.project.profile.pvr().isValid()


def test_membership_between_role_instance_and_role_chain_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram43', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.RoleChainNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.MembershipEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid target for Role assertion: role chain node'
    assert not session.project.profile.pvr().isValid()


def test_membership_between_role_instance_and_neutral_chained_complement_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram46', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.ComplementNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.MembershipEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Detected unsupported operator sequence on intersection node'
    assert not session.project.profile.pvr().isValid()


def test_membership_between_attribute_instance_and_role_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram45', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.MembershipEdge, source, (Item.RoleNode, 'test:R1'), qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Invalid target for Attribute assertion: Role'
    assert not session.project.profile.pvr().isValid()


def test_membership_between_attribute_instance_and_neutral_chained_complement_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram47', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.ComplementNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.MembershipEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Detected unsupported operator sequence on intersection node'
    assert not session.project.profile.pvr().isValid()


def test_membership_between_neutral_property_assertion_node_and_neutral_chained_complement_node(session, qtbot):
    # GIVEN
    __give_focus_to_diagram(session, 'diagram48', qtbot)
    num_edges_in_project = len(session.project.edges())
    source = first(filter(lambda x: x.type() is Item.PropertyAssertionNode, session.project.nodes(session.mdi.activeDiagram())))
    target = first(filter(lambda x: x.type() is Item.ComplementNode, session.project.nodes(session.mdi.activeDiagram())))
    # WHEN
    __insert_edge_between(session, Item.MembershipEdge, source, target, qtbot)
    # THEN
    assert len(session.project.edges()) == num_edges_in_project
    assert session.project.profile.pvr().message() == 'Detected unsupported operator sequence on intersection node'
    assert not session.project.profile.pvr().isValid()