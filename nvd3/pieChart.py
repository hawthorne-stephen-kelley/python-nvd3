#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3

Part of this code is inspired from goulib
https://github.com/goulu/Goulib/blob/master/Goulib/nvd3.py

This project aims to be reusuable with less dependencies and with the aim
to power more library using it. For instance Django-Nvd3.

General aims :
- keep a separation between the templating and the output generation
- don't tie with too many dependencies
- easy to use
- clean APIs
- Documented
- Clean code / PEP8
"""

from NVD3Chart import NVD3Chart, stab


#TODO: Add extensive documentation on pieChart
#settings supported
#examples
class pieChart(NVD3Chart):
    """
    usage ::

        chart = nvd3.pieChart(name='pieChart', height=400, width=400)
        xdata = ["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"]
        ydata = [3, 4, 0, 1, 5, 7, 3]
        chart.add_serie(y=ydata, x=xdata)
        chart.buildhtml()

    js example::

        data = [{ key: "Cumulative Return",
                  values: [
                    {
                      "label": "One",
                      "value" : 29.765957771107
                    },
                    {
                      "label": "Two",
                      "value" : 0
                    },
                    {
                      "label": "Three",
                      "value" : 32.807804682612
                    },
                  ]
                }]

        nv.addGraph(function() {
          var chart = nv.models.pieChart()
              .x(function(d) { return d.label })
              .y(function(d) { return d.value })
              .showLabels(true);

            d3.select("#div_id")
                .datum(data)
                .transition()
                .duration(1200)
                .call(chart);

          return chart;
        });
    """
    def __init__(self, height=450, width=None, **kwargs):
        NVD3Chart.__init__(self, **kwargs)
        self.create_x_axis('xAxis', format=None)
        self.create_y_axis('yAxis', format=None)
        # must have a specified height, otherwise it superimposes both chars
        if height:
            self.set_graph_height(height)
        if width:
            self.set_graph_width(width)

    def buildjschart(self):
        NVD3Chart.buildjschart(self)

        pie_jschart = '\n' + stab(2) + 'chart.x(function(d) { return d.x })\n' + \
            stab(3) + '.y(function(d) { return d.y })\n' + \
            stab(3) + '.values(function(d) { return d })\n' + \
            stab(3) + '.color(d3.scale.category10().range());\n'
        if self.width:
            pie_jschart += stab(2) + 'chart.width(%s);\n' % self.width
        if self.height:
            pie_jschart += stab(2) + 'chart.height(%s);\n' % self.height

        start_index = self.jschart.find('.pieChart();')
        string_len = len('.pieChart();')
        replace_index = start_index + string_len
        if start_index > 0:
            self.jschart = self.jschart[:replace_index] + pie_jschart + self.jschart[replace_index:]
