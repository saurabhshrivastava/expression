
# stmt = [ expr ]
# expr = expr OR term | term 
# term = term AND factor | factor
# factor = NOT factor | atom
# atom = ( expr ) | NUM 

# stmt = [ expr ]
# expr = term expr_
# expr_ = OR term expr_ | eps
# term = factor term_
# term_ = AND factor term_ | eps
# factor = NOT factor | atom
# atom = ( expr ) | NUM 




input = None
lookahead = None
line = 10

def eat () :
    global lookahead
    global input
    if len (input) :
        lookahead = input.pop(0)
    else :
        lookahead = None

def stmt () :
    global lookahead
    if lookahead == '[' :
        eat ()
        e = expr ()
        if lookahead == ']' :
            eat ()
            return e
        else :
            print "parse error, ']' expected" 
    else :
        print "parse error, unexpected token"

def expr () :
    l = term ()
    n = expr_ (l)
    return n

def expr_ (l) :
    global lookahead
    if lookahead == 'OR' :
        eat ()
        r = term ()
        l2 = ('OR', l, r)
        n = expr_ (l2)
        return n
    else :
        return l

def term () :
    l = factor ()
    n = term_ (l)
    return n

def term_ (l) :
    global lookahead
    if lookahead == 'AND' :
        eat ()
        r = factor ()
        l2 = ('AND', l, r)
        n = term_ (l2)
        return n
    else :
        return l

def factor () :
    global lookahead
    if lookahead == 'NOT' :
        eat ()
        f = factor ()
        return ('NOT', f, None)
    else :
        f = atom ()
        return f

def atom () :
    global lookahead
    if lookahead == '(' :
        eat ()
        a = expr ()
        if lookahead == ')' :
            eat ()
            return a
        else :
            print "parse error, ')' expected" 
    elif isinstance (lookahead, int) == True :
        a = lookahead
        eat ()
        return ('NUM', a, None)
    else :
        print "parse error, unexpected token"
      
       

def code (e, true_line, false_line) :
   global line
   type = e[0]
   left = e[1]
   right = e[2]   
   if type == 'NOT' :
       left_line = code (left, false_line, true_line)
       my_line = left_line
   elif type == 'OR' :
       right_line = code (right, true_line, false_line)
       left_line = code (left, true_line, right_line)
       my_line = left_line
   elif type == 'AND' :
       right_line = code (right, true_line, false_line)
       left_line = code (left, right_line, false_line)
       my_line = left_line
   elif type == 'NUM' :
       line += 10
       my_line = line
       print "%d %s T %d F %d" % (my_line, left, true_line, false_line)
   else :
       print "bad code"
   return my_line

def main () :
    global input
    input = ['[', '(', '(', '(', 10, 'AND', 20, ')', 'AND', 30, ')', 'AND', '(', 40, 'OR', 50, ')',')', 'OR', '(', 60, 'AND', 70, ')', ']' ]
    # input = ['[', 'NOT', '(', 123, 'OR', 234, ')', 'AND', 456, 'AND', 'NOT', 890, 'OR', 777, ']']
    # input = ['[', '(', 123, 'OR', 234, ')', 'AND', 456, 'AND', 890, 'OR', 777, ']']
    print input
    eat ()
    s = stmt ()
    if lookahead != None :
        print "junk at the end, starting %s" % lookahead
    print s

    st = code (s, 1000, 2000)
    print "start %d" % st

if __name__ == "__main__":
    main()





