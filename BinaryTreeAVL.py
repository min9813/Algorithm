#coding:utf-8
import sys
import time
from sklearn.utils import shuffle
LEFT = 0
RIGHT = 1


class Node:
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None
        self.left_sum = 0
        self.right_sum = 0
        self.balance = 0
        
class Path:
    def __init__(self):
        self.node = None
        self.direction = None
        self.next = None
        self.prev = None
        
        
class BinaryTreeAVL:
    def __init__(self):
        self.root = None
        self.node_count = 0
        
    def is_empty(self):
        return self.root is None
    
    def rotate_right(self,node):
        lnode = node.left
        node.left = lnode.right
        lnode.right = node
        if node.left is not None:
            node.left_sum = node.left.left_sum + node.left.right_sum + 1
        else:
            node.left_sum = 0
        lnode.right_sum = node.left_sum + node.right_sum + 1
        return lnode
    
    def rotate_left(self,node):
        rnode = node.right
        node.right = rnode.left
        rnode.left = node
        if node.right is not None:
            node.right_sum = node.right.right_sum + node.right.left_sum + 1
        else:
            node.right_sum = 0
        rnode.left_sum = node.right_sum + node.left_sum + 1
        return rnode
    
    def search(self,value):
        # if exists return the node which has same value
        # else return null
        tmp = self.root
        is_founded = False
        while(tmp is not None):
            if (value > tmp.value):
                tmp = tmp.right
            elif (value == tmp.value):
                is_founded = True
                break
            else:
                tmp = tmp.left
        return is_founded
            
    
    def insert(self,value):
        if self.root is None:        
            self.root = Node(value)
            self.node_count += 1
            return -1
        elif self.search(value):
            return -1
        else:
            node = self.root
            head_path = Path()
            head_path.node = node
            path = head_path
            while(True):
                if value < node.value:
                    node.left_sum += 1
                    path.node = node
                    path.direction = LEFT
                    if node.left is None:
                        if head_path != path:
                            head_path.prev = path
                        node.left = Node(value)
                        break           
                    node = node.left
                    path.next = Path()
                    path.next.prev = path
                    path = path.next
                else:
                    node.right_sum += 1
                    path.node = node
                    path.direction = RIGHT
                    if node.right is None:
                        if head_path != path:
                            head_path.prev = path
                        node.right = Node(value)
                        break
                    node = node.right
                    path.next = Path()
                    path.next.prev = path
                    path = path.next
                    
            if path != head_path:
                path.next = head_path
            while(path != head_path):
                path = path.prev
        self.node_count += 1
        self.root = self.balance(head_path)
        return self.root
    

    
    def balance(self,head_path):
        if head_path.prev is None:
            path = head_path
        else:
            path = head_path.prev

        new_node = None
        while(path is not None):
            direction = path.direction
            pnode = path.node
            path = path.prev
            head_path.prev = None
            if path is not None:
                path.next = None
            if direction == LEFT:
                pnode.balance += 1
            else:
                pnode.balance -= 1
            b = pnode.balance
            if b==0:
                # 修正不要
                return self.root
            elif b>1:
                # 左に傾いている
                if pnode.left.balance < 0:
                    # 子が右に傾いている
                    pnode.left = self.rotate_left(pnode.left)
                    new_node = self.rotate_right(pnode)
                    self.update_balance(new_node)
                else:
                    new_node = self.rotate_right(pnode)
                    new_node.balance = 0
                    pnode.balance = 0
                break
            elif b<-1:
                # 右に傾いている
                if pnode.right.balance > 0:
                    # 子が左に傾いている
                    pnode.right = self.rotate_right(pnode.right)
                    new_node = self.rotate_left(pnode)
                    self.update_balance(new_node)
                else:
                    new_node = self.rotate_left(pnode)
                    new_node.balance = 0
                    pnode.balance = 0
                break
        if path is not None:
            gnode, gdirection = path.node, path.direction
            if gdirection == LEFT:
                gnode.left = new_node
                gnode.left_sum = new_node.left_sum + new_node.right_sum + 1
            else:
                gnode.right = new_node
                gnode.right_sum = new_node.left_sum + new_node.right_sum + 1
        elif new_node is not None:
            return new_node
        return self.root
            
    def update_balance(self,node):
        if node.balance == 1:
            node.right.balance = -1
            node.left.balance = 0
        elif node.balance == -1:
            node.right.balance = 0
            node.left.balance = 1
        else:
            node.right.balance = 0
            node.left.balance = 0
        node.balance = 0
        
    def search_by_order(self,search_order, saiki = False, node = None):
        if saiki:
            if search_order < 0 or search_order > self.node_count:
                sys.exit("index {} out of array",search_order)
            if node is None:
                node = self.root
            node_order = node.left_sum + 1
            if search_order > node_order:
                search_order -= node_order
                found_node = self.search_by_order(search_order, saiki = True, node = node.right)
            elif search_order == node_order:
                return node
            else:
                found_node = self.search_by_order(search_order, saiki = True, node = node.left)
        else:
            node = self.root
            found_node = None
            if search_order < 0 or search_order > self.node_count:
                sys.exit("index {} out of array",search_order)
            while(True):
                node_order = node.left_sum + 1
                if search_order > node_order:
                    node = node.right
                    search_order -= node_order
                elif search_order == node_order:
                    found_node = node
                    break
                else:
                    node = node.left
        return found_node
        
    
    
            
            
    
    def patrol(self,node):
        if node is not None:
            for x in self.patrol(node.left):
                yield x
            yield node.value
            for x in self.patrol (node.right):
                yield x
    
    def print_tree(self):
        buffer = "binarytree("
        for x in self.patrol(self.root):
            buffer += str(x) + ","
        buffer += ")"
        return buffer
    
    def print_node_main(self,draw_index = False):
        self.print_node_value(node = self.root)
        if draw_index:
            print("------------index----------------")
            self.print_node_index(node = self.root)
        
    def draw_for_check(self,mark):
        print("---------dra_for_check {}----------------".format(mark))
        self.print_node_main()
        
    def print_node_value(self, node=None, depth = 0):
        if node is not None:
            self.print_node_value(node = node.left, depth = depth + 1)
            print("|","  "*depth, node.value)
            self.print_node_value(node = node.right, depth = depth + 1)
            
    def print_node_index(self, node=None, depth = 0):
        if node is not None:
            self.print_node_index(node = node.left, depth = depth + 1)
            print("|","  "*depth, node.left_sum)
            self.print_node_index(node = node.right, depth = depth + 1)

if __name__ == "__main__":
    start = time.time()
    avl_tree = BinaryTreeAVL()
    for x in shuffle(range(1, 100)):
        avl_tree.insert(x)
    finish = time.time()
    print("time:",finish - start)
    avl_tree.print_node_main(draw_index = True)
            
        
        
