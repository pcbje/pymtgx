#!/usr/bin/env python
"""
This work is made available under the Apache License, Version 2.0.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
"""
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

  def testLayout(self):
    mtgx = pymtgx.Pymtgx()

    id1 = mtgx.add_node("maltego.Person", "Jon Doe")
    id2 = mtgx.add_node("maltego.EmailAddress", "jon.doe@mail.com")
    
    mtgx.add_edge(id1, id2)

    for node in mtgx.positions:
      self.assertFalse('x' in mtgx.positions[node].position.attrib)
      self.assertFalse('y' in mtgx.positions[node].position.attrib)

    mtgx.layout('spring_layout')

    for node in mtgx.positions:
      self.assertNotEqual(None, mtgx.positions[node].position.attrib['x'])
      self.assertNotEqual(None, mtgx.positions[node].position.attrib['y'])

    mtgx.create('test5')

  def testNodeFormat(self):
    mtgx = pymtgx.Pymtgx()

    mtgx.add_node("maltego.Person", "Jon Doe")

    nodes = mtgx.nodes(data=True)

    element = nodes[0][1]['MaltegoEntity'].data

    entity = element.getchildren()[0]

    self.assertEqual("maltego.Person", entity.attrib['type'])

    prop = entity.getchildren()[0].getchildren()[0]

    self.assertEqual("person.fullname", prop.attrib['name'])
    self.assertEqual("string", prop.attrib['type'])

    value = prop.getchildren()[0].text

    self.assertEqual("Jon Doe", value)

  def testRegisterEntities(self):
    mtgx = pymtgx.Pymtgx()

    self.assertEqual(6, len(mtgx.entities))

    mtgx.register_entities("test_entities.mtz")

    self.assertEqual(8, len(mtgx.entities))

    registered_entity = mtgx.entities["maltego.Humbug"]

    self.assertEqual("humbug.Id", registered_entity['name'])
    
if __name__ == '__main__':
  unittest.main()
