class BlockService:
    def __init__(self,nodeAllList):
        block = self.service(self.url, self.nodeAllList)
        blockList = be.blockList
        self.imgOut.outBlock(blockList, self.fileName, 0)
        return blockList