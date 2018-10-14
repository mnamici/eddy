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


import unittest

from eddy.core.datatypes.collections import DistinctList
from eddy.core.owl import IRI
from eddy.core.owl import PrefixManager
from eddy.core.owl import IllegalPrefixError
from eddy.core.owl import IllegalNamespaceError


class DistinctListTestCase(unittest.TestCase):

    def test_constructor_with_list(self):
        D1 = DistinctList([1, 2, 3, 3, 4, 1, 4, 5, 6, 7, 7, 8, 2])
        self.assertSequenceEqual(D1, DistinctList([1, 2, 3, 4, 5, 6, 7, 8]), seq_type=DistinctList)

    def test_constructor_with_tuple(self):
        D1 = DistinctList((1, 2, 3, 3, 4, 1, 4, 5, 6, 7, 7, 8, 2))
        self.assertSequenceEqual(D1, DistinctList((1, 2, 3, 4, 5, 6, 7, 8)), seq_type=DistinctList)

    def test_constructor_with_set(self):
        self.assertEqual(8, len(DistinctList({1, 2, 3, 4, 5, 6, 7, 8})))

    def test_append(self):
        D1 = DistinctList([1, 2, 3, 4, 5, 6, 7, 8])
        D1.append(9)
        self.assertSequenceEqual(D1, DistinctList([1, 2, 3, 4, 5, 6, 7, 8, 9]), seq_type=DistinctList)

    def test_insert(self):
        D1 = DistinctList([1, 2, 3, 4, 5, 6, 7, 8])
        D1.insert(5, 9)
        self.assertSequenceEqual(D1, DistinctList([1, 2, 3, 4, 5, 9, 6, 7, 8]), seq_type=DistinctList)

    def test_extend_with_list(self):
        D1 = DistinctList([1, 2, 3, 4, 5, 6, 7, 8])
        D1.extend([9, 10, 11, 12])
        self.assertSequenceEqual(D1, DistinctList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]), seq_type=DistinctList)

    def test_extend_with_tuple(self):
        D1 = DistinctList([1, 2, 3, 4, 5, 6, 7, 8])
        D1.extend((9, 10, 11, 12))
        self.assertSequenceEqual(D1, DistinctList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]), seq_type=DistinctList)

    def test_remove_with_match(self):
        D1 = DistinctList([1, 2, 3, 4, 5, 6, 7, 8])
        D1.remove(4)
        self.assertSequenceEqual(D1, DistinctList([1, 2, 3, 5, 6, 7, 8]), seq_type=DistinctList)

    def test_remove_with_no_match(self):
        D1 = DistinctList([1, 2, 3, 4, 5, 6, 7, 8])
        D1.remove(9)
        self.assertSequenceEqual(D1, DistinctList([1, 2, 3, 4, 5, 6, 7, 8]), seq_type=DistinctList)


class IRITestCase(unittest.TestCase):

    def test_constructor(self):
        IRI1 = IRI('http://example.com/')
        IRI2 = IRI('http://example.com/', 'res')
        self.assertEqual('http://example.com/', str(IRI1))
        self.assertEqual('http://example.com/res', str(IRI2))
        with self.assertRaises(IllegalNamespaceError):
            IRI('example namespace:', 'res')

    def test_get_scheme(self):
        IRI1 = IRI('http://domain.com:8080/resource/sub/path?query=xyz#fragment')
        self.assertEqual('http', IRI1.scheme)

    def test_get_authority(self):
        IRI1 = IRI('http://domain.com:8080/resource/sub/path?query=xyz#fragment')
        self.assertEqual('domain.com:8080', IRI1.authority)

    def test_get_path(self):
        IRI1 = IRI('http://domain.com:8080/resource/sub/path?query=xyz#fragment')
        self.assertEqual('/resource/sub/path', IRI1.path)

    def test_get_query(self):
        IRI1 = IRI('http://domain.com:8080/resource/sub/path?query=xyz#fragment')
        self.assertEqual('query=xyz', IRI1.query)

    def test_get_fragment(self):
        IRI1 = IRI('http://domain.com:8080/resource/sub/path?query=xyz#fragment')
        self.assertEqual('fragment', IRI1.fragment)

    def test_is_absolute(self):
        IRI1 = IRI('http://example.com/')
        IRI2 = IRI('http://example.com/res')
        IRI3 = IRI('http://example.com/', 'res')
        IRI4 = IRI('/myres', 'id')
        self.assertTrue(IRI1.isAbsolute())
        self.assertTrue(IRI2.isAbsolute())
        self.assertTrue(IRI3.isAbsolute())
        self.assertFalse(IRI4.isAbsolute())

    def test_is_relative(self):
        IRI1 = IRI('http://example.com/')
        IRI2 = IRI('http://example.com/res')
        IRI3 = IRI('http://example.com/', 'res')
        IRI4 = IRI('/myres', 'id')
        self.assertFalse(IRI1.isRelative())
        self.assertFalse(IRI2.isRelative())
        self.assertFalse(IRI3.isRelative())
        self.assertTrue(IRI4.isRelative())

    def test_is_uri(self):
        IRI1 = IRI('http://example.com/')
        IRI2 = IRI('http://example.com/res')
        IRI3 = IRI('http://example.com/', 'res')
        IRI4 = IRI('http://example.com/ontology', 'Città')
        self.assertTrue(IRI1.isURI())
        self.assertTrue(IRI2.isURI())
        self.assertTrue(IRI3.isURI())
        self.assertFalse(IRI4.isURI())

    def test_eq(self):
        IRI1 = IRI('http://example.com/')
        IRI2 = IRI('http://example.com/', 'res')
        self.assertFalse(IRI1 == IRI2)
        self.assertTrue(IRI1 == IRI1)
        self.assertTrue(IRI2 == IRI2)
        self.assertTrue(IRI2 == IRI('http://example.com/', 'res'))

    def test_getitem(self):
        IRI1 = IRI('http://example.com/')
        IRI2 = IRI('http://example.com/', 'res')
        self.assertEqual([c for c in 'http://example.com/'], [IRI1[i] for i in range(len(IRI1))])
        self.assertEqual([c for c in 'http://example.com/res'], [IRI2[i] for i in range(len(IRI2))])


class PrefixManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = PrefixManager()
        self.manager.setPrefix('', 'http://example.com/')
        self.manager.setPrefix('ex', 'http://example.com/')
        self.manager.setPrefix('ex2', 'http://example.com/')
        self.manager.setPrefix('data', IRI('http://data.example.org/'))

    def test_clear(self):
        self.manager.clear()
        self.assertEqual(0, len(self.manager))

    def test_get_default_prefix(self):
        self.assertEqual(IRI('http://example.com/'), self.manager.getDefaultPrefix())
        self.manager.setDefaultPrefix('http://data.example.org/')
        self.assertEqual(IRI('http://data.example.org/'), self.manager.getDefaultPrefix())

    def test_get_iri(self):
        self.assertEqual(IRI('http://example.com/res'), self.manager.getIRI(':res'))
        self.assertEqual(IRI('http://example.com/res'), self.manager.getIRI('ex:res'))
        self.assertEqual(IRI('http://example.com/res'), self.manager.getIRI('ex2:res'))
        self.assertEqual(IRI('http://example.com/', 'res'), self.manager.getIRI(':res'))
        self.assertEqual(IRI('http://example.com/', 'res'), self.manager.getIRI('ex:res'))
        self.assertEqual(IRI('http://example.com/', 'res'), self.manager.getIRI('ex2:res'))
        self.assertEqual(IRI('http://data.example.org/', 'res'), self.manager.getIRI(self.manager.getShortForm(IRI('http://data.example.org/res'))))

    def test_get_prefix(self):
        self.assertEqual(IRI('http://example.com/'), self.manager.getDefaultPrefix())
        self.assertEqual(self.manager.getPrefix('ex'), self.manager.getDefaultPrefix())
        self.assertEqual(IRI('http://example.com/'), self.manager.getPrefix('ex'))
        self.assertEqual(IRI('http://example.com/'), self.manager.getPrefix('ex2'))
        self.assertEqual(IRI('http://data.example.org/'), self.manager.getPrefix('data'))
        self.assertIsNone(self.manager.getPrefix('unk'))
        self.assertIsNone(self.manager.getPrefix('http://example.com/'))

    def test_get_prefix_name(self):
        self.manager.reset()
        self.manager.setPrefix('ex', 'http://example.com/')
        self.manager.setPrefix('ex2', 'http://example.com/ontology/')
        self.manager.setPrefix('ex3', 'http://example.com/ontology/subpath/')
        self.assertEqual('ex', self.manager.getPrefixName(IRI('http://example.com/')))
        self.assertEqual('ex2', self.manager.getPrefixName(IRI('http://example.com/ontology/')))
        self.assertEqual('ex3', self.manager.getPrefixName(IRI('http://example.com/ontology/subpath/')))

    def test_get_short_form1(self):
        self.assertEqual('data:res', self.manager.getShortForm(IRI('http://data.example.org/res')))
        self.assertEqual('data:res', self.manager.getShortForm(IRI('http://data.example.org/', 'res')))
        self.assertEqual('data:some/nested/resource', self.manager.getShortForm(IRI('http://data.example.org/some/nested/resource')))
        self.assertEqual('data:res', self.manager.getShortForm(self.manager.getIRI('data:res')))
        self.assertIsNone(self.manager.getShortForm('http://some-domain.com/myres'))

    def test_get_short_form2(self):
        self.manager.reset()
        self.manager.setPrefix('ex', 'http://example.com/')
        self.manager.setPrefix('ex2', 'http://example.com/ontology/')
        self.manager.setPrefix('ex3', 'http://example.com/ontology/subpath/')
        self.assertEqual(self.manager.getShortForm(IRI('http://example.com/res')), 'ex:res')
        self.assertEqual(self.manager.getShortForm(IRI('http://example.com/ontology/res')), 'ex2:res')
        self.assertEqual(self.manager.getShortForm(IRI('http://example.com/ontology/subpath/res')), 'ex3:res')

    def test_set_prefix(self):
        self.manager.setPrefix('ex', 'http://mydomain.com/')
        self.assertEqual(IRI('http://mydomain.com/'), self.manager.getPrefix('ex'))
        self.assertEqual(IRI('http://example.com/'), self.manager.getPrefix('ex2'))
        with self.assertRaises(IllegalPrefixError):
            self.manager.setPrefix('ill egal', 'http://some-domain.org/')
        with self.assertRaises(IllegalPrefixError):
            self.manager.setPrefix('ill:egal', 'http://some-domain.org/')
        with self.assertRaises(IllegalNamespaceError):
            self.manager.setPrefix('ex', 'some random string')

    def test_remove_prefix(self):
        self.manager.removePrefix('ex')
        self.assertIsNone(self.manager.getPrefix('ex'))
        self.assertEqual(IRI('http://example.com/'), self.manager.getPrefix('ex2'))

    def test_unregister_namespace1(self):
        self.manager.unregisterNamespace('http://example.com/')
        self.assertIsNone(self.manager.getDefaultPrefix())
        self.assertIsNone(self.manager.getPrefix('ex'))
        self.assertIsNone(self.manager.getPrefix('ex2'))
        self.assertEqual(IRI('http://data.example.org/'), self.manager.getPrefix('data'))

    def test_unregister_namespace2(self):
        self.manager.unregisterNamespace('http://www.example.org/')
        self.assertIsNotNone(self.manager.getDefaultPrefix())
        self.assertIsNotNone(self.manager.getPrefix('ex'))
        self.assertIsNotNone(self.manager.getPrefix('ex2'))
        self.assertEqual(IRI('http://data.example.org/'), self.manager.getPrefix('data'))
