#from ConfigParser import SafeConfigParser
#
#config = SafeConfigParser()
#config.read('config.ini')
#
#try:
#    print config.get('first','ugh')
#except:
#    print "Ini file parsing error!"

words = ["tes 123T ","ABC","tTeS"]
for word in words:
    word = word.strip().lower()
    print(word)
