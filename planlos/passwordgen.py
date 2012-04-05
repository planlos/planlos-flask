# coding: utf-8


import random

class Password_Generator(object):
    def __init__(self, oldstyle=False, length=10, lang='ngerman'):
        self.r = random.Random()
        self.length = length
        self.oldstyle = oldstyle
        self.lang = lang
        self.wordlist = None

    def get_random_word_from_wordlist(self):
        if not self.wordlist:
            f = open('/usr/share/dict/%s' % self.lang, 'r')
            self.wordlist = f.readlines()
            f.close()

        num_lines = len(self.wordlist)
        pick = self.r.randrange(10, num_lines)
        return self.wordlist[pick]

    def gen(self):
        if self.oldstyle:
            passwd = ''.join([chr(self.r.randrange(33,126))
                            for x in range(0,self.length)])
        else:
            passwd = ''
            for i in range(4):
                passwd += self.get_random_word_from_wordlist()
                passwd += chr(self.r.randrange(33,47))
        return passwd
