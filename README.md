pymtgx
======

Python API for generating Maltego MTGX files.

#### Install

<pre><code>$ python setup.py. install</code></pre>

#### Usage

<pre><code>import pymtgx
pymtgx = pymtgx.Pymtgx()
pymtgx.register_entities("custom_entities.mtz")
id1 = pymtgx.add_node("maltego.EmailAddress", "some@email.com")
id2 = pymtgx.add_node("maltego.EmailAddress", "another@email.com")
pymtgx.add_edge(id1, id2)
pymtgx.create_mtgx("example.mtgx")</pre></code>
