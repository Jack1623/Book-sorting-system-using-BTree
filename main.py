import requests
from dotenv import load_dotenv
import os
import re

load_dotenv()

APIKEY = os.getenv('APIKEY')

class BTreeNode:
    def __init__(self):
        self.values = []
        self.children = []

class BTree:
    def __init__(self):
        self.root = BTreeNode()
    
    def insert(self, value):
        self.insert_value(self.root, value)

    def insert_value(self, node, value):
        if not node.children:
            node.values.append(value)
            node.values.sort()

            if len(node.values)>4:
                left_node = BTreeNode()
                right_node = BTreeNode()
                left_node.values = node.values[:2]
                right_node.values = node.values[3:]
                node.values = [node.values[2]]
                node.children = [left_node, right_node]
        
        else:
            i = 0
            while i < len(node.values):
                if value < node.values[i]:
                    break
                i += 1
            self.insert_value(node.children[i], value)  

    def get(self, value):
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
            return self.get_value(node.children[i], value)

def print_tree(node, level=0):
    if node is not None:
        for k in range(len(node.values)):
            print(f"Level {level}: ", end='')
            try: 
                print(f"{book_callNoDict[node.values[k]]}", end=' | ')
            except KeyError: 
                print(f"{standardNo}", end=' | ')
            for child in node.children:
                print()
                print_tree(child, level+1)

btree = BTree()

values_insert = [1, 2, 3, 4, 5, 6, 7, 8]
for value in values_insert:
    btree.insert(value)

#print_tree(btree.root)

baseURL = "https://www.nl.go.kr/NL/search/openApi/search.do?key=" + APIKEY
resultList = []
callNoList = []
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
        resultList.append(result)
        i += 1

    for j in range(len(resultList)):
        callNoList.append(re.sub(r'[^0-9]', '', resultList[j]['result'][0]['callNo']))
        book_callNoDict[callNoList[j]] = resultList[j]['kwd']
        btree.insert(callNoList[j])

    standardNo = input("분류 청구 기호 기준 입력: ")
    btree.insert(standardNo)
    
    print_tree(btree.root)