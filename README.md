pymtgx
======

Python API for generating Maltego MTGX files.

#### Install

<pre><code>$ python setup.py. install</code></pre>

#### Usage

<pre><code>>>> import pymtgx
>>> pymtgx = pymtgx.Pymtgx()
>>> pymtgx.add_node("maltego.EmailAddress", "some@email.com")
'n0'
>>> pymtgx.add_node("maltego.EmailAddress", "another@email.com")
'n1'
>>> pymtgx.add_edge("n0", "n1")
>>> pymtgx.create_mtgx("example.mtgx")</pre></code>
