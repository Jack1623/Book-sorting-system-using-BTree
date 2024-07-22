import requests
from dotenv import load_dotenv
import os
import re

load_dotenv()

APIKEY = os.getenv('APIKEY')

leaf_levels = []

class BTreeNode:
    def __init__(self):
        self.values = []
        self.children = []
        self.parent = []
        self.level = 0

class BTree:
    def __init__(self):
        self.root = BTreeNode()
    
    def insert(self, value):
        self.insert_value(self.root, value)

    def insert_value(self, node, value, flag=0):
        if not node.children:
            node.values.append(value)
            node.values.sort()
        
        else:
            i = 0
            while i < len(node.values):
                if value < node.values[i]:
                    break
                i += 1
            self.insert_value(node.children[i], value, flag=1) 
            if flag:
                return

        if len(node.values) > 2:
            self.fix_overflow(node)

    def fix_overflow(self, node):                                 
        left_node = BTreeNode()
        right_node = BTreeNode()
        for lr_node in [left_node, right_node]:
            lr_node.parent = node
            lr_node.level = node.level + 1
            left_node.children = node.children[:(len(node.children)//2)]
            right_node.children = node.children[(len(node.children)//2):]
            for lr_node in [left_node, right_node]:
                for children in lr_node.children:
                    children.level += 1
                    children.parent = lr_node
        left_node.values = [node.values[0]]
        right_node.values = [node.values[2]]
        node.values = [node.values[1]]
        node.children = [left_node, right_node]

        if node != self.root and not self.check_leaf_levels(self.root):
            for value in node.values:
                node.parent.values.append(value)
            node.parent.values.sort()
            node.parent.children.remove(node)
            for children in node.children:
                node.parent.children.append(children)
                node.parent.children = sort_children(node.parent.children)
                children.parent = node.parent
                children.level -= 1

            if node.parent != None and len(node.parent.values) > 2:     
                self.fix_overflow(node.parent)

    def check_leaf_levels(self, node, flag=0):
        if not node.children:
            leaf_levels.append(node.level)
            return
        else:
            for child in node.children:
                self.check_leaf_levels(child, flag=1)
                
        if flag:
            return

        firstLevel = leaf_levels[0]
        for level in leaf_levels:
            if level != firstLevel:
                leaf_levels.clear()
                return False
        leaf_levels.clear()
        return True  
    
    def inorder(self, standard):
        def _inorder(node, standard, flag=0):
            for l in range(len(node.children)):
                flag = _inorder(node.children[l], standard, flag)
                if l < len(node.values):
                    if node.values[l] == standard:
                        flag = 1
                        continue
                    if not flag:
                        listLeft.append(node.values[l])
                    else:
                        listRight.append(node.values[l])
            if not len(node.children):
                for m in range(len(node.values)):
                    if node.values[m] == standard:
                        flag = 1
                        continue
                    if not flag:
                        listLeft.append(node.values[m])
                        listRight.append(node.values[m])
                return flag
        _inorder(self.root, standard)

def sort_children(children):
    children_value = []
    for child in children:
        children_value.append(child.values[0])
    for i in range(len(children)):
        min_idx = i
        for j in range(i + 1, len(children)):
            if children_value[min_idx] > children_value[j]:
                min_idx = j 
        children[i], children[min_idx] = children[min_idx], children[i]
    return children

def print_tree(node, level=0):
    if node is not None:
        print(f"Level {level}: {node.values}")
        for child in node.children:
            print_tree(child, level + 1)

def change_to_name(list):
    i = 0
    j = 0
    for value in list:
        for i in range(len(callNoList)):
            if value == callNoList[i]:
                break
        list[j] = book_callNoDict[callNoList[i]]
        j += 1
    return list

btree = BTree()

#6, 8, 10, 2, 1, 7, 3, 9, 11, 4, 5
values_insert = []
for value in values_insert:
    btree.insert(value)

baseURL = "https://www.nl.go.kr/NL/search/openApi/search.do?key=" + APIKEY
resultList = []
callNoList = []
listLeft = []
listRight = []
book_callNoDict = {}
standardNo = ""

if __name__ == '__main__':
    i = 0
    num = int(input("분류할 책의 개수 입력: "))
    while True:
        if(i == num):
            break
        kwd = input("분류할 책의 제목과 저자를 슬래시(/)로 구분하여 입력(%d): "%(i+1))
        kwdList = kwd.split('/')
        url = baseURL + "&apiType=json&srchTarget=total&kwd=" + kwdList[0] + "&detailSearch=true&f1=title&v1=" + kwdList[0] + "&f2=author&v2=" + kwdList[1] + "&pageSize=1&pageNum=1"
        response = requests.get(url)
        result = response.json()
        if result['total'] == 0:
            print("책을 찾을 수 없습니다. 다시 입력해주세요.")
            continue
        if result['result'][0]['callNo'] == '':
            print("청구 기호가 존재하지 않습니다. 다른 책을 입력해주세요.")
            continue
        resultList.append(result)
        i += 1

    for j in range(len(resultList)):
        callNoList.append(re.sub(r'[^0-9]', '', resultList[j]['result'][0]['callNo']))
        book_callNoDict[callNoList[j]] = resultList[j]['kwd']
        btree.insert(callNoList[j])

    standardNo = input("분류 청구 기호 기준 입력: ")
    btree.insert(standardNo)

    btree.inorder(standardNo)
    listLeft = change_to_name(listLeft)
    listRight = change_to_name(listRight)
    print(f"\nSort 1: {listLeft}\nSort 2: {listRight}")