#!/usr/bin/env python
import unittest
import pymtgx

class PymtgxUnitTest(unittest.TestCase):
  def setUp(self):
    pass

  def testNodesAndEdgesAreAdded(self):
    mtgx = pymtgx.Pymtgx()

    self.assertEqual(0, len(mtgx.nodes()))

    id1 = mtgx.add_node("maltego.Person", "Jon Doe")
    id2 = mtgx.add_node("maltego.EmailAddress", "jon.doe@mail.com")

    self.assertEqual(2, len(mtgx.nodes()))
		
    self.assertEqual(0, len(mtgx.edges()))

    mtgx.add_edge(id1, id2)

    self.assertEqual(1, len(mtgx.edges()))

  def testNodeFormat(self):
    mtgx = pymtgx.Pymtgx()

    mtgx.add_node("maltego.Person", "Jon Doe")

    nodes = mtgx.nodes(data=True)

    element = nodes[0][1]['MaltegoEntity'].data

    entity = element.getchildren()[0]

    self.assertEqual("maltego.Person", entity.attrib['type'])

    prop = entity.getchildren()[0].getchildren()[0]

    self.assertEqual("person.fullname", prop.attrib['name'])
    self.assertEqual("Full name", prop.attrib['displayName'])
    self.assertEqual("string", prop.attrib['type'])

    value = prop.getchildren()[0].text

    self.assertEqual("Jon Doe", value)

  def testRegisterEntities(self):
    mtgx = pymtgx.Pymtgx()

    self.assertEqual(2, len(mtgx.entities))

    mtgx.register_entities("test_entities.mtz")

    self.assertEqual(4, len(mtgx.entities))

    registered_entity = mtgx.entities["maltego.Humbug"]

    self.assertEqual("humbug.Id", registered_entity['name'])
    self.assertEqual("ID", registered_entity['displayName'])
    self.assertEqual("string", registered_entity['dataType'])

if __name__ == '__main__':
  unittest.main()