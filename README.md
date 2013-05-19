puppet-node-visualiser
======================

Simple analysis and visualisation of Puppet nodes &amp; classes include syntax to hopefully help with the refactoring of site.pp

Code Analysis is done using [python-ply](http://www.dabeaz.com/ply/) library, [Flask](http://flask.pocoo.org/) is used to expose the data over HTTP to javascript which uses [d3](http://d3js.org/) for the visualisation.
