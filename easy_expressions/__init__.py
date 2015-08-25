"""
__init__.py

Contains most of the Easy logic.

"""

import re

class Easy(object):
    """
    Easy.

    Makes Regular Expressions really, really easy.
    """

    def __init__(self):

        self.flags = ""
        self._literal = []
        self._groups_used = 0
        self.clear()

    def clear(self):
        """
        Reset the current state.
        """

        self._min = -1
        self._max = -1
        self._of = ""
        self._of_any = False
        self._of_group = -1
        self._from = ""
        self._not_from = ""
        self._like = ""
        self._either = ""
        self._reluctant = False
        self._capture = False 

    def flush(self):
        """
        If there's anything in the state, add the current state to the stack and clear.

        Returns nothing.

        """

        if (    self._of != "" or 
                self._of_any or 
                self._of_group > 0 or
                self._from != "" or
                self._not_from != "" or
                self._like != ""
            ):
                capture_literal = "" if self._capture else "?:"
                quantity_literal = self.getQuantityLiteral()
                character_literal = self.getCharacterLiteral()
                reluctant_literal = "?" if self._reluctant else ""
                self._literal.append("(" + capture_literal + "(?:" + character_literal + ")" + quantity_literal + reluctant_literal + ")");
                self.clear();

        return

    def getQuantityLiteral(self):
        """
        Gets the 'quantity' literal.

        Returns a string.
        """

        if self._min != -1:
            if self._max != -1:
                return "{" + str(self._min) + "," + str(self._max) + "}"
            return "{" + str(self._min) + ",}"
        else:
            return "{0," + str(self._max) + "}"

    def getCharacterLiteral(self):
        """
        Gets the 'character' literal.

        Returns a string.
        """
        if self._of != "":
            return str(self._of)

        if self._of_any:
            return "."
        
        if self._of_group > 0:
            return "\\" + str(self._of_group)
        
        if self._from != "":
            return "[" + str(self._from) + "]"
        
        if self._not_from != "":
            return "[^" + str(self._not_from) + "]"
        
        if self._like != "":
            return str(self._like)
        
    def getLiteral(self):
        """
        Flush, and return the joined literal.
        """
        self.flush()
        return "".join(self._literal)

    def combineGroupNumberingAndGetLiteral(self, regex):
        """

        """

        literal = self.incrementGroupNumbering(regex.getLiteral(), self._groups_used)
        self._groups_used = self._groups_used + regex._groups_used
        return literal

    def incrementGroupNumbering(self, literal, increment):
        """
        """
        if increment > 0:
            def repl(groupReference):
                groupNumber = int(groupReference[2:]) + increment;
                return int(groupReference[0:2]) + groupNumber;

            subbed = re.sub(r'/[^\\]\\\d+/g', repl, literal)
            return subbed
        return literal

    def getRegex(self):
        self.flush()
        joined =  "".join(self._literal)

        if self.flags != "":
            if 'm' in self.flags:
                flags = re.M
            if 'i' in self.flags:
                flags = re.I
            if 'g' in self.flags:
                flags = re.G
            compiled = re.compile(joined, flags)
        else:
            compiled = re.compile(joined)
        return compiled

    def addFlag(self, flag):
        """
        If we don't have the flag already, add it.
        """
        if self.flags.find(flag) == -1:
            self.flags = self.flags + flag
        return self

    def ignoreCase(self):
        """
        """
        self.addFlag('i')
        return self

    def multiLine(self):
        """
        """
        self.addFlag('m')
        return self

    def globalMatch(self):
        """
        """
        self.addFlag('g')
        return self

    def startOfInput(self):
        """
        """
        self._literal.append("(?:^)")
        return self

    def startOfLine(self):
        """
        """
        self.multiLine()
        return self.startOfInput()


    def endOfInput(self):
        """
        """
        self.flush()
        self._literal.append("(?:$)")
        return self

    def endOfLine(self):
        """
        """
        self.multiLine()
        return self.endOfInput()

    def either(self, r):
        """
        """
        if type(r) == type(''):
            return self.eitherLike(Easy().exactly(1).of(r))
        else:
            self.eitherLike(r)

    def eitherLike(self, r):
        """
        """
        self.flush()
        self._either = self.combineGroupNumberingAndGetLiteral(r)
        return self

    def orr(self, r):
        """
        I hate the naming of this, but it chokes with the natural 'or'.

        """
        if type(r) == type(''):
            return self.orLike(Easy().exactly(1).of(r))
        else:
            return self.orLike(r)

    def orLike(self, r):
        """
        """
        either = self._either
        orr = self.combineGroupNumberingAndGetLiteral(r)
        if either == "":
            lastOr = self._literal[-1]
            lastOr = lastOr[:-1]
            self._literal[-1] = lastOr
            self._literal.append("|(?:" + orr + "))");
        else:
            self._literal.append("(?:(?:" + either + ")|(?:" + orr + "))");
        self.clear()
        return self

    def neither(self, r):
        if type(r) == type(""):
            return self.notAhead(Easy().exactly(1).of(r))
        return self.notAhead(r)

    def nor(self, r):
        if (this._min == 0 and self._of_any):
            self._min = -1
            self._of_any = False
        self.neither(r)
        return self.min(0).ofAny()

    def exactly(self, n):
        self.flush()
        self._min = n
        self._max = n
        return self

    def min(self, n):
        self.flush()
        self._min = n
        return self

    def max(self, n):
        self.flush()
        self._max = n
        return self

    def of(self, s):
        self._of = self._sanitize(s)
        return self

    def ofAny(self):
        self._of_any = True
        return self

    def ofGroup(self, n):
        self._of_group = n
        return self

    def From(self, s):
        self._from = self._sanitize(s.join(""))
        return self

    def notFrom(self, s):
        self._notFrom = self._sanitize(s.join(""))
        return self

    def like(self, r):
        self._like = self.combineGroupNumberingAndGetLiteral(r)
        return self

    def reluctantly(self):
        self._reluctant = True
        return self

    def ahead(self):
        self.flush()
        self._literal.append("(?=" + self.combineGroupNumberingAndGetLiteral(r) + ")")
        return self

    def notAhead(self, r):
        self.flush()
        self._literal.append("(?!" + self.combineGroupNumberingAndGetLiteral(r) + ")")
        return self

    def asGroup(self):
        self._capture = True
        self._groups_used = self._groups_used + 1
        return self

    def then(self, s):
        return self.exactly(1).of(s)

    def find(self, s):
        return self.then(s)

    def some(self, s):
        return self.min(1).From(s)

    def maybeSome(self, s):
        return self.min(0).From(s)

    def maybe(self, s):
        return self.max(1).of(s)

    def something(self):
        return self.min(1).ofAny()

    def anything(self):
        return self.min(0).ofAny()

    def anythingBut(self):
        if len(s) == 1:
            return self.min(0).notFrom([s])
        self.notAhead(Easy().exactly(1).of(s))
        return self.min(0).ofAny()

    def any(self):
        return self.exactly(1).ofAny()

    def lineBreak(self):
        self.flush()
        self._literal.append("(?:\\r\\n|\\r|\\n)")
        return self

    def lineBreaks(self):
        return self.like(Easy().lineBreak())

    def whitespace(self):
        if (self._min == -1 and self._max == -1):
            self.flush()
            self._literal.append("(?:\\s")
            return self
        self._like = "\\s"
        return self

    def notWhitespace(self):
        if (self._min == -1 and self._max == -1):
            self.flush()
            self._literal.append("(?:\\S)")
            return self
        self._like = "\\S"
        return self

    def tab(self):
        self.flush()
        self._literal.append("(?:\\t)")
        return self

    def tabs(self):
        return self.like(Easy().tab())

    def digit(self):
        self.flush()
        self._literal.append("(?:\\d)")
        return self

    def notDigit(self):
        self.flush()
        serlf._literal.append("(?:\\D)")
        return self

    def digits(self):
        return self.like(Easy().digit())

    def notDigits(self):
        return self.like(Easy().notDigit())

    def letter(self):
        self.exactly(1)
        self._notFrom = "A-Za-z"
        return self

    def notLetter(self):
        self.exactly(1)
        self._notFrom = "A-Za-z"
        return self

    def lowerCaseLetter(self):
        self.exactly(1)
        self._from = "a-z"
        return self

    def lowerCaseLetters(self):
        self._from = "a-z"
        return self

    def upperCaseLetter(self):
        self.exactly(1)
        self._from = "A-Z"
        return self

    def upperCaseLetters(self):
        self._from = "A-Z"
        return self

    def append(self, r):
        self.exactly(1)
        self._like = self.combineGroupNumberingAndGetLiteral(r)
        return self

    def optional(self, r):
        self.max(1)
        self._like = self.combineGroupNumberingAndGetLiteral(r)
        return self

    def _sanitize(self, s):
        """
        Escape special chars.

        I'm not sure if this is a satisfactory approach compared to the original: "/([.*+?^=!:${}()|\[\]\/\\])/g

        """
        return re.escape(s)
