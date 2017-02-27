
# expr = expr OR term | term 
# term = term AND factor | factor
# factor = NOT factor | atom
# atom = ( expr ) | NUM 

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
            print "parse error 1"
    elif isinstance (lookahead, int) == True :
        a = lookahead
        eat ()
        return ('NUM', a, None)
    else :
        print "parse error 2"
      
       

def code (e, true_line, false_line) :
   global line
   line += 10
   my_line = line
   type = e[0]
   left = e[1]
   right = e[2]   
   if type == 'NOT' :
       right_line = code (left, false_line, true_line)
   elif type == 'OR' :
       right_line = code (right, true_line, false_line)
       left_line = code (left, true_line, right_line)
   elif type == 'AND' :
       right_line = code (right, true_line, false_line)
       left_line = code (left, right_line, false_line)
   elif type == 'NUM' :
       print "%d %s T %d F %d" % (my_line, left, true_line, false_line)
   else :
       print "bad code"
   return my_line

def main () :
    global input
    input = ['NOT', '(', 123, 'OR', 234, ')', 'AND', 456, 'AND', 'NOT', 890, 'OR', 777]
    # input = ['(', 123, 'OR', 234, ')', 'AND', 456, 'AND', 890, 'OR', 777]
    print input
    eat ()
    e = expr ()
    print e

    code (e, 1000, 2000)


if __name__ == "__main__":
    main()





