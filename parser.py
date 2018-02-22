NUM = "NUM"
STR = "STR"
SYM = "SYM"
LBR = "("
RBR = ")"


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.cursor = 0

    def lookahead(self):
        return self.tokens[self.cursor][0]

    def list(self):
        self.consume(LBR)
        ret = self.elements()
        self.consume(RBR)
        return ret

    def elements(self):
        ret = [self.element()]
        while(self.lookahead() != RBR):
            ret.append(self.element())
        return ret

    def element(self):
        return self.atom() or self.list()

    def atom(self):
        ln = self.lookahead()
        if (ln == NUM):
            return self.consume(NUM)
        elif (ln == SYM):
            return self.consume(SYM)
        elif (ln == STR):
            return self.consume(STR)

    def consume(self, tokenClass):
        token = self.tokens[self.cursor]
        if self.lookahead() == tokenClass:
            self.cursor += 1
            return token
        else:
            raise Exception("Expecting token class " + tokenClass)


p = Parser([(LBR, "("), (STR, "asd"), (NUM, 32432), (LBR, "("), (NUM, 65765), (RBR, ")"), (RBR, ")")])
print(p.list())
