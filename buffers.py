class Buffer:
    def __init__(self, _bytes: bytearray = None, string_mode: str = 'start-int') -> None:
        self.__content = _bytes or bytearray()
        self.__position = 0
        self.__string_mode = string_mode
    
    # Métodos de Lectura
    def __read(self, length: int):
        end_position = self.__position + length
        if end_position >= len(self.__content):
            return None
        ret = memoryview(self.__content)[self.__position:end_position].tobytes()
        self.__position += length
        return ret

    def get_u8(self):
        return int.from_bytes(self.__read(1), byteorder='little')

    def get_u16(self):
        return int.from_bytes(self.__read(2), byteorder='little')

    def get_u32(self):
        return int.from_bytes(self.__read(4), byteorder='little')

    def get_u64(self):
        return int.from_bytes(self.__read(8), byteorder='little')
    
    def get_string(self):
        if self.__string_mode == 'start-int':
            length = self.get_u8()
        elif self.__string_mode == 'end-char':
            length = self.__content.index(ord(' '), self.__position) - self.__position + 1
        
        return self.__read(length).decode('utf-8')
        
    
    def get_bool(self):
        return bool(self.__read(1))
    
    # Métodos de Escritura
    def __write(self, length: int, value: any):
        if not isinstance(value, (str, int, bool)):
            return
        
        if isinstance(value, (int, bool)):
            self.__content.extend(value.to_bytes(length))
            self.__position += length
        elif isinstance(value, str):
            self.__content.extend(length.to_bytes(length=1))
            self.__content.extend(value.encode('utf-8'))
            self.__position += length
        
    
    def put_u8(self, value: int):
        self.__write(1, value)
    
    def put_u16(self, value: int):
        self.__write(2, value)
    
    def put_u32(self, value: int):
        self.__write(4, value)
    
    def put_u64(self, value: int):
        self.__write(8, value)
    
    def put_bool(self, value: any):
        self.__write(1, bool(value))
    
    def put_string(self, string: str):
        self.__write(len(string), string)
    
    def seek(self, position: int):
        self.__position = max(0, min(len(self.__content), position))
    
    def skip(self, spaces: int):
        self.seek(self.__position + spaces)

    def get_position(self):
        return self.__position

    def get_size(self):
        return len(self.__content)

    def get_content(self):
        return self.__content
    