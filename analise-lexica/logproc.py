# ------------------------------------------------------------
# Processing a log file
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = [
    'TIMESTAMP',
    'PROC',
    'MESSAGE'
] 

def t_TIMESTAMP(t):
    # Regular expression for TIMESTAMP
    r'\d+:\d+:\d+.\d+\s-\d+'
    t.type = 'TIMESTAMP'
    #print("TIMESTAMP '%s'" % t.value)
    return t

def t_PROC(t):
    # Regular expression for PROC
    r'\t.*\t'
    t.type = 'PROC'
    t.value = t.value[1:len(t.value) - 1]
    #print("PROC '%s'" % t.value)
    return t

def t_MESSAGE(t):
    # Regular expression for MESSAGE
    r'.+\n*'
    t.type = 'MESSAGE'
    #print("MESSAGE '%s'" % t.value)
    t.value = t.value[:len(t.value) - 1]
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value)
    t.lexer.skip(1)


class LogProcLexer:
    data = None
    lexer = None
    def __init__(self):
        fh = open("log", 'r')
        self.data = fh.read()
        fh.close()
        self.lexer = lex.lex()
        self.lexer.input(self.data)

    def collect_messages(self):
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break  # No more input
            if (tok.type == "PROC" and tok.value == "kernel"):
                tok = self.lexer.token()
                tokens.append(tok)
        return tokens
        
if __name__ == '__main__':
    print(LogProcLexer().collect_messages())
