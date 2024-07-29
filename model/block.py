class Block:
    __slots__ = (
        'id', 'block_visual', 'block_divide', "block_dividable","Doc")
    clac_count = 0

    def __init__(self):
        Block.clac_count += 1
        self.id = str(Block.clac_count)
        # 用于VIPS使用
        self.block_dividable = True
        self.block_divide = False
        self.block_visual = True
        self.Doc = 0
