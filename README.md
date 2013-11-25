pymtgx
======

Python API for generating Maltego mtgx files.

#### Install

<pre><code>$ python setup.py install</code></pre>

#### Usage

<pre><code>import pymtgx
mtgx = pymtgx.Pymtgx()
mtgx.register_entities("custom_entities.mtz")
id1 = mtgx.add_node("maltego.EmailAddress", "some@email.com")
id2 = mtgx.add_node("maltego.EmailAddress", "another@email.com")
id3 = mtgx.add_node("maltego.EmailAddress", "third@email.com")
mtgx.add_edge(id1, id2)
mtgx.add_edge(id1, id3, "I am edge label")
mtgx.create("example")</pre></code>
