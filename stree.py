# in order of precendence
OPS = ['*', '/', '+', '-']

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

LEFT_PAREN = '('
RIGHT_PAREN = ')'

class STree():
    def __init__(self, string):
        # remove whitespace
        self._string = string.replace(" ", "")

        return self.string_to_tree(self._string)

    def string_to_tree(self, string):

        chars = self.to_chars(string)

        for op in OPS:
            self.rewrite_list(chars, op)

        print(chars)

    def to_chars(self, string):
        chars = []
        i = 0
        lookahead = i + 1
        char_buffer = ''
        string = string.replace(" ", "")

        while True:
            try:
                cursor = string[i]
            except IndexError:
                break

            if cursor in DIGITS:

                while cursor in DIGITS:
                    try:
                        char_buffer += cursor
                        i += 1
                        cursor = string[i]
                    except IndexError:
                        break
                chars.append(char_buffer)
                char_buffer = ''

            else:
                chars.append(cursor)
                i += 1
            
        return chars


    def rewrite_list(self, chars, op):
        i = 0
        if op not in chars:
            return
        else:
            for char in chars:
                if char == op:
                    triple = [op, chars[i - 1], chars[i + 1]]
                    chars[i] = triple
                    del chars[i - 1]
                    del chars[i]
                    self.rewrite_list(chars, op)
                i += 1


STree("1 + 2 * 3 + 4")
STree("5 + 1 * 2 * 3").to_chars("12 + 2 * 3 + 4")