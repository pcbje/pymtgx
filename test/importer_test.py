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

  def testReadIndexedformat_spec(self):
    importer = pymtgx.Importer(input_file='test/importer/data.csv', 
      format_spec_file='test/importer/indexed.format', 
      output_file='test/importer/output', 
      entity_files=['test/test_entities.mtz'],
      delimiter=',', quotechar='"', skip_lines=1,
      map_header=False)

    self.assertEqual(3, len(importer.format_spec))

    self.assertEqual(0, importer.format_spec[0]['from_index'])
    self.assertEqual('Person', importer.format_spec[0]['from_type'])
    self.assertEqual(2, importer.format_spec[0]['to_index'])
    self.assertEqual('EmailAddress', importer.format_spec[0]['to_type'])
    self.assertEqual('Edge label 1', importer.format_spec[0]['edge_label'])

    self.assertEqual(2, importer.format_spec[2]['from_index'])
    self.assertEqual('EmailAddress', importer.format_spec[2]['from_type'])
    self.assertEqual(1, importer.format_spec[2]['to_index'])
    self.assertEqual('Person', importer.format_spec[2]['to_type'])
    self.assertEqual('Edge label 3', importer.format_spec[2]['edge_label'])

  def testReadMappedformat_spec(self):
    importer = pymtgx.Importer(input_file='test/importer/data.csv', 
      format_spec_file='test/importer/mapped.format', 
      output_file='test/importer/output', 
      entity_files=['test/test_entities.mtz'],
      delimiter=',', quotechar='"', skip_lines=0,
      map_header=True)

    self.assertEqual(3, len(importer.format_spec))

    self.assertEqual(0, importer.format_spec[0]['from_index'])
    self.assertEqual('Person', importer.format_spec[0]['from_type'])
    self.assertEqual(2, importer.format_spec[0]['to_index'])
    self.assertEqual('EmailAddress', importer.format_spec[0]['to_type'])
    self.assertEqual('Edge label 1', importer.format_spec[0]['edge_label'])

    self.assertEqual(2, importer.format_spec[2]['from_index'])
    self.assertEqual('EmailAddress', importer.format_spec[2]['from_type'])
    self.assertEqual(1, importer.format_spec[2]['to_index'])
    self.assertEqual('Person', importer.format_spec[2]['to_type'])
    self.assertEqual('Edge label 3', importer.format_spec[2]['edge_label'])

  def testParseLine(self):
    importer = pymtgx.Importer(input_file='test/importer/data.csv', 
      format_spec_file='test/importer/indexed.format', 
      output_file='test/importer/output', 
      entity_files=['test/test_entities.mtz'],
      delimiter=',', quotechar='"', skip_lines=1,
      map_header=False)
    
    row = ['X', 'Y', 'Z']

    self.assertEqual(3, importer._parse_line(row))
  
  def testCreate(self):
    importer = pymtgx.Importer(input_file='test/importer/data.csv', 
      format_spec_file='test/importer/indexed.format', 
      output_file='test/importer/output', 
      entity_files=['test/test_entities.mtz'],
      delimiter=',', quotechar='"', skip_lines=1,
      map_header=False)

    importer.create()
    
if __name__ == '__main__':
  unittest.main()
