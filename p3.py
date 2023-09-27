# project: p3
# submitter: rgsroda
# partner: none
# hours: 13

import json
import math
import graphviz as gv
import pandas as pd
from collections import deque
import scrape

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []
        self.sequence = ''

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        # 1. clear out visited set
        self.order = []
        self.visited.clear()
        self.sequence = ''
        # 2. start recursive search by calling dfs_visit
        self.dfs_visit(node)


    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return 
        # 2. mark node as visited by adding it to the set
        self.visited.add(node)
        # 3. add this node to the end of self.order
        self.order.append(node)
        # 4. get list of node's children with this: self.go(node)
        children = self.go(node)
        # 5. in a loop, call dfs_visit on each of the children
        for child in children:
            self.dfs_visit(child)
            
    def bfs_search(self, node):
        self.visited.clear()
        self.sequence = ''
        self.bfs_visit(node)
            
    def bfs_visit(self, node):
        todo = deque([node])
        while len(todo) > 0:
            curr = todo.popleft()
            if curr in self.visited:
                pass
            self.visited.add(curr)
            self.order.append(curr)
            children = self.go(curr)
            for child in children:
                if child not in todo and child not in self.visited:
                    todo.append(child)
                    
                                  
            
class MatrixSearcher(GraphSearcher):
    
    def __init__(self,df):
        super().__init__()
        self.df = df
        
    def go(self,node):
        children = []
        for node, has_edge in self.df.loc[f"{node}"].items():
            if has_edge:
                children.append(node)
        return children
    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
        self.sequence = ''
        
    def go(self, node):
        with open('file_nodes/'+node) as f:
            text = f.read()
        lines = text.split("\n")
        self.sequence = self.sequence + lines[0]
        children = lines[1]
        return children.split(",")
    
    def message(self):
        return self.sequence
    
class WebSearcher(GraphSearcher):
    def __init__(self,driver):
        super().__init__()
        self.driver = driver
        self.tablelist = []
        
    def go(self,url):
        self.driver.get(url)
        pagesource = self.driver.page_source
        children1 = self.driver.find_elements(by = 'tag name', value = 'a')
        smalltable = pd.read_html(pagesource)[0]
        self.tablelist.append(smalltable)
        result = []
        for link in children1:
            attr = link.get_attribute('href')
            result.append(attr)
        return result
    
    def table(self):
        return pd.concat(self.tablelist, ignore_index = True)