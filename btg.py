#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  btg.py
#  
#  Copyright 2019 Iván Ávalos <ivan.avalos.diaz@hotmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, see <http://www.gnu.org/licenses/>.
# 

from graphviz import Digraph
import sys, random, getopt

usage ='''\
Usage: btg [-o output] [-n] [-d depth] [-m min_value] [-x max_value]
Or:    btg -h
Commands:
  -o      Output file for graph
  -d      Number of levels in the tree
  -m      Minimum value for each node
  -x      Maximum value for each node
  -n      Only generate DOT file (skip rendering)
Examples:
  btg -d 100         # generate 100 levels
  btg -o graph.rv -n # output DOT file and skip render
  btg -m 0 -x 10000  # min is 0, max is 10000
'''

class Node:
    id = None
    left = None
    data = None
    right = None

class RandomBTG:
    auto_increment = 0
    total_nodes = 0
    total_edges = 0

    def __init__ (self, output, depth, min_val, max_val):
        self.output = output
        self.depth = depth
        self.min_val = min_val
        self.max_val = max_val
        self.dot = Digraph (comment='RandomBTG')
        self.root = self.add_node ()
        self.generate (self.root, self.depth)

    def create_graph (self, root=None, parent=None):
        if root is None:
            self.create_graph (self.root, None)
            return
        self.dot.node (root.id, str(root.data))
        if parent is not None:
            self.dot.edge (parent.id, root.id)
        if root.left is not None:
            self.create_graph (root.left, root)
        if root.right is not None:
            self.create_graph (root.right, root)

    def render_graph (self, view=True):
        self.dot.render (self.output, view=view)

    def save_graph (self):
        self.dot.save (self.output)

    def generate (self, root, levels):
        if levels <= 0:
            return self.root
        quant = bool(random.getrandbits (1)) # 1|2
        which = bool(random.getrandbits (1)) # L|R
        if not quant:
            self.total_edges += 1
            if which:
                root.left = self.add_node ()
                self.generate (root.left, levels - 1)
            else:
                root.right = self.add_node ()
                self.generate (root.right, levels - 1)
        else:
            self.total_edges += 2
            root.left = self.add_node ()
            self.generate (root.left, levels - 1)
            root.right = self.add_node ()
            self.generate (root.right, levels - 1)

    def add_node (self):
        self.auto_increment += 1
        self.total_nodes += 1
        
        node = Node()
        node.id = str(self.auto_increment)
        node.data = random.randint (self.min_val, self.max_val)
        return node

def main ():
    # Default values
    output = 'output.gv'
    tree_depth = 10
    min_value = 0
    max_value = 100
    skip_render = False
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'o:d:m:x:nh')
    except getopt.GetoptError as err:
        print (str (err))
        print (usage)
        sys.exit (2)

    for o, a in opts:
        if o == '-o':
            output = a
        elif o == '-d':
            tree_depth = int(a)
        elif o == '-m':
            min_value = int(a)
        elif o == '-x':
            max_value = int(a)
        elif o == '-n':
            skip_render = True
        elif o == '-h':
            print (usage)
            exit ()

    print ('Generating tree...')
    random_btg = RandomBTG (output = output,
                            depth = tree_depth,
                            min_val = min_value,
                            max_val = max_value)
    print ('Total levels:', random_btg.depth)
    print ('Total nodes:', random_btg.total_nodes)
    print ('Total edges:', random_btg.total_edges)
    print ('Generating graph...')
    random_btg.create_graph ()
    if not skip_render:
        print ('Rendering graph...')
        random_btg.render_graph ()
    else:
        print ('Saving graph...')
        random_btg.save_graph ()
        

if __name__ == "__main__":
    main ()
