'''nums = [3,7,8,3]
target = 6
def twoSum(nums,target):
    summ = 0
    for j in range(len(nums)):
        for i in range(len(nums)-1):
            summ = nums[i] + nums[j]
            if summ == target and i != j:
                return [i,j]
print(twoSum(nums,target))
'''

class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None
    def printTree(self,root):
        h = self.height(root)
        matrix = [[''for n in range((2**h)-1)] for m in range(h)]
        self.place(root,matrix,0,(2**h)-1,0)
        return matrix
    def height(self,node):
        return max(1+self.height(node.left),1+self.height(node.right)) if node else 0
    def place(self,node,matrix,i,j,row):
        if node:
            col = (i+j) // 2
            matrix[row][col] = str(node.val)
            self.place(node.left,matrix,i,col,row+1)
            self.place(node.right,matrix, col+1, j, row+1)



root = Tree()
root.data = 1
root.left = Tree()
root.left.data = 2
root.right = Tree()
root.right.data = 3

root.left.left = Tree()
root.left.left.data = 4
root.left.right = Tree()
root.left.right.data = 5
