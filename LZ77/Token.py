class Token:
    def __init__(self, offset: int, length: int, next_symbol: str):
        self.offset = offset
        self.length = length
        self.next_symbol = next_symbol
    
    def __repr__(self):
        return f"Token(distance={self.distance}, length={self.length}, next_symbol='{self.next_symbol}')"
