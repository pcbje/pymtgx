pymtgx
======

Python API for generating Maltego mtgx files.

### Installation

<pre><code>$ python setup.py install</code></pre>

### Usage

<pre><code>import pymtgx
mtgx = pymtgx.Pymtgx()
mtgx.register_entities("custom_entities.mtz")
id1 = mtgx.add_node("maltego.EmailAddress", "some@email.com")
id2 = mtgx.add_node("maltego.EmailAddress", "another@email.com")
id3 = mtgx.add_node("maltego.EmailAddress", "third@email.com")
mtgx.add_edge(id1, id2)
mtgx.add_edge(id1, id3, "I am edge label")
mtgx.create("example")</pre></code>


### The importer

The API comes with a built-in importer, capable of generating mtgx archives from CSV files based on some format specification file.
The format specification file can either be based on column name or column index.


#### Basic usage:

<pre><code>$ python pymtgx/importer.py -h
usage: importer.py [-h] -i INPUT_FILE -f FORMAT_FILE -o OUTPUT_FILE -e
                   ENTITY_FILES [-d DELIMITER] [-q QUOTECHAR] [-s SKIP_LINES]
                   [-m MAP_HEADER]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        Path to file to parse
  -f FORMAT_FILE, --format-file FORMAT_FILE
                        Path to format specification file.
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Path to output file. Extension is added if missing.
  -e ENTITY_FILES, --entity-files ENTITY_FILES
                        Comma separated list of .mtz files to use.
  -d DELIMITER, --delimiter DELIMITER
                        How values are delimited. Default: ,
  -q QUOTECHAR, --quotechar QUOTECHAR
                        How values are quoted, remember escape character.
                        Default: None
  -s SKIP_LINES, --skip-lines SKIP_LINES
                        Number of lines to skip. Default: 0
  -m MAP_HEADER, --map-header MAP_HEADER
                        Use column names in format specification. If not, the
                        columns in the specifications are 0-indexed.</pre></code>

The general syntax for entity and edge specifications is:

<pre><code>[FORM_COLUMN]:[FROM_ENTITY_TYPE] > [TO_COLUMN]:[TO_ENTITY_TYPE] | [EDGE LABEL]</pre></code>

The entity types field must match one of the entity types registered using the '-e' option, without the 'maltego.' prefix.

##### Example for specification file using column index:

<pre><code>0:Person > 2:EmailAddress | Edge label 1
0:Person > 1:Person | Edge label 2
2:EmailAddress > 1:Person | Edge label 3</pre></code>

##### Example for specification file using column names:

<pre><code>Col1:Person > Col3:EmailAddress | Edge label 1
Col1:Person > Col2:Person | Edge label 2
Col3:EmailAddress > Col2:Person | Edge label 3</pre></code>

Both of these are capable of parsing the input CSV file:

<pre><code>"Col1","Col2","Col3"
"P1","P3","P4"
"P2","P3","P4"</pre></code>

#### Example runs:

##### Based on column index:
<pre><code>$ python -m pymtgx.importer -i test/importer/data.csv -f test/importer/indexed.format -o index_test.mtgx -e test/test_entities.mtz -q \"
Parsed 3 lines. Created index_test.mtgx</pre></code>

##### Based on column name:
<pre><code>$ python -m pymtgx.importer -i test/importer/data.csv -f test/importer/mapped.format -o mapped_test.mtgx -e test/test_entities.mtz -m True -q \"
Parsed 3 lines. Created mapped_test.mtgx</pre></code>
