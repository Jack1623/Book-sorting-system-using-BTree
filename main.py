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

        if node != self.root and not self.check_leaf_levels(self.root):
            for value in node.values:
                node.parent.values.append(value)
            node.parent.values.sort()
            node.parent.children.remove(node)
            for children in node.children:
                node.parent.children.append(children)
                children.parent = node.parent
                children.level -= 1

            if node.parent != None and len(node.parent.values) > 2:     # 오류의 근원지. node.parent가 아니라 다른 것을 입력해야 되는 것으로 추정.
                self.fix_overflow(node.parent)

    def fix_overflow(self, node):                                       # fix_overflow() 함수와 연계해서 생각
        left_node = BTreeNode()
        right_node = BTreeNode()
        for lr_node in [left_node, right_node]:
            lr_node.parent = node
            lr_node.level = node.level + 1
            for children in lr_node.children:
                children.level += 1
                children.parent = lr_node
        left_node.children = node.children[:(len(node.children)//2)]
        right_node.children = node.children[(len(node.children)//2):]
        left_node.values = [node.values[0]]
        right_node.values = [node.values[2]]
        node.values = [node.values[1]]
        node.children = [left_node, right_node]

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

    '''def get(self, value):
        return self.get_value(self.root, value)

    def get_value(self, node, value):
        if not node.children:  
            return value in node.values
        else:  
            i = 0
            while i < len(node.values):
                if value == node.values[i]:
                    return True
                if value < node.values[i]:
                    return self.get_value(node.children[i], value)
                i += 1
            return self.get_value(node.children[i], value)'''
    
    def inorder(self, standard):
        flag = 0
        def _inorder(node, level=0):
            if node:
                _inorder(node.children[0])
                for k in range(len(node.values)):
                    if node.values[k] == standard:
                        flag = 1
                    if not flag:
                        listLeft.append(node.values[k])
                    else:
                        listRight.append(node.values[k])
                _inorder(node.children[1])

            '''for k in range(len(node.values)):
                if node.values[k] == standard:
                    _inorder(node[k+1], flag=1)
                if not len(node.children):
                    if node.children[0]:
                        if not flag:
                            listLeft.append(node.values[k])
                        else:
                            listRight.append(node.values[k])
                        _inorder(node.children[0], flag)
                    if node.children[1]:
                        if not flag:
                            listLeft.append(node.values[k])
                        else:
                            listRight.append(node.values[k])
                        _inorder(node.children[1], flag)
                else:
                    _inorder(node, level+1, flag)'''
        _inorder(self.root)
'''
    def inorder(self, standard):
        def _inorder(node, level=0, flag=0):
            for k in range(len(node.values)):
                if node.values[k] == standard:
                    _inorder(node[k+1], flag=1)
                print(f"Level {level}: ", end='')
                try: 
                    print(f"{book_callNoDict[node.values[k]]}", end=' | ')
                except KeyError: 
                    print(f"{standardNo}", end=' | ')
                if node.children[0]:
                    print()
                    if flag == 0:
                        listLeft.append(node.values[k])
                    else:
                        listRight.append(node.values[k])
                    _inorder(node.children[0], level+1)
                if node.children[1]:
                    print()
                    if flag == 0:
                        listLeft.append(node.values[k])
                    else:
                        listRight.append(node.values[k])
                    _inorder(node.children[1], level+1)
        _inorder(self.root)

'''
'''def print_tree(node, level=0):
    if node is not None:
        for k in range(len(node.values)):
            print(f"Level {level}: ", end='')
            try: 
                print(f"{book_callNoDict[node.values[k]]}", end=' | ')
            except KeyError: 
                print(f"{standardNo}", end=' | ')
            for child in node.children:
                print()
                print_tree(child, level+1)'''
def print_tree(node, level=0):
    if node is not None:
        print(f"Level {level}: {node.values}")
        if node.parent != None:
            print(f"Parent: {node.parent.values}")
        for child in node.children:
            print_tree(child, level + 1)

btree = BTree()

values_insert = [1, 2, 3, 4, 5, 6, 7, 8]
for value in values_insert:
    btree.insert(value)

print_tree(btree.root)

btree = BTree()

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
    print(f"Sort 1: {listLeft}\nSort 2: {listRight}")