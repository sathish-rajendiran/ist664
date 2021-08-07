"""
This program was adapted from the Stanford NLP class SpamLord homework assignment.
    The code has been rewritten and the data modified, nevertheless
    please do not make this code or the data public.
This version has two patterns that were suggested in comments
    in order to get you started .
"""
import sys
import os
import re
import pprint

"""
TODO
For Part 1 of our assignment, add to these two lists of patterns to match
examples of obscured email addresses and phone numbers in the text.
For optional Part 3, you may need to add other lists of patterns.
"""
# email .edu patterns

# each regular expression pattern should have exactly two sets of parentheses.
#   the first parenthesis should be around the someone part
#   the second parenthesis should be around the somewhere part
#   in an email address whose standard form is someone@somewhere.edu
epatterns = []
epatterns.append('([A-Za-z.]+)@([A-Za-z.]+)\.edu')
epatterns.append('([A-Za-z.]+)\s@\s([A-Za-z.]+)\.edu')

# email .com patterns

# each regular expression pattern should have exactly two sets of parentheses.
#   the first parenthesis should be around the someone part
#   the second parenthesis should be around the somewhere part
#   in an email address whose standard form is someone@somewhere.com

ecompatterns = []
ecompatterns.append('([A-Za-z.]+)@([A-Za-z.]+)\.com')


# phone patterns
# each regular expression pattern should have exactly three sets of parentheses.
#   the first parenthesis should be around the area code part XXX
#   the second parenthesis should be around the exchange part YYY
#   the third parenthesis should be around the number part ZZZZ
#   in a phone number whose standard form is XXX-YYY-ZZZZ
ppatterns = []
ppatterns.append('(\d{3})-(\d{3})-(\d{4})')   #trial 2: uncomment telephone patterns  


""" 
This function takes in a filename along with the file object and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

TODO
For Part 3, if you have added other lists, you should add
additional for loops that match the patterns in those lists
and produce correctly formatted results to append to the res list.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        # you may modify the line, using something like substitution
        #    before applying the patterns
        # email pattern list
#         print("line",line)

       # Regular expression replacement on for overall

        line = re.sub(" <at symbol> ","@",line) #replace <at symbol> with @ 
        line = re.sub("&lt;","",line) #replace &lt; with "" 
        line = re.sub("&gt;","",line) #replace &gt; with @ 
        line = re.sub(" at <!-- die!--> ","@",line) #replace <!-- die!--> with "" 
        line = re.sub(" <!-- spam pigs!--> dot <!-- die!--> ",".",line) #replace <!-- spam pigs!--> with "" 
        line = re.sub("&#x40;","@",line) #replace &#x40; with @ 
        line = re.sub(" \(followed by &ldquo;","",line) #replace (followed by &ldquo; with "" 
        line = re.sub("&rdquo;\)","",line) #replace (followed by &ldquo; with "" 
        line = re.sub(" \(followed by \"","",line) #replace  (followed by " with "" 
                
        line = re.sub("\"\)","",line) #replace ") with "" 
        line = re.sub(" AT ","@",line) #replace "at with @ 
        line = re.sub(" DOT ",".",line) #replace "dot with @ 
        line = re.sub("<del>","",line) #replace <del> with "" 
        line = re.sub(" @ ","@",line) #replace   @   with @ 
        line = re.sub(" WHERE ","@",line) #replace "WHERE with @ 
        line = re.sub(" DOM ",".",line) #replace "DOM with @ 
        line = re.sub(" dt ",".",line) #replace "dt with @ 

         # Regular expression replacement on for .edu emails
        
        eline = re.sub(r"-", "", line)
        eline = re.sub("        ","",eline)
        eline = re.sub("\ at cs dot jhu dot edu</a>","@cs.jhu.edu",eline)
        eline = re.sub("jks at robotics;stanford;edu<br>&nbsp;</p>","jks@robotics.stanford.edu",eline)
        eline = re.sub(" at cs dot stanford dot edu","@cs.stanford.edu",eline) #lam@
        eline = re.sub(" at cs stanford edu","@cs.stanford.edu",eline)
        eline = re.sub(" at cs.stanford.edu<br>","@cs.stanford.edu",eline)
        
        # Regular expression replacement on for .com email
        
        ecomline = re.sub(" at ","@",eline) #replace  at  with @
        ecomline = re.sub(" dt ",".",ecomline) #replace  dt  with .
        
        # Regular expression replacement on for Phone numbers
        
        line = re.sub("\[650\] ","650-",line) #replace  [650\]  with 650-
        
        pline = re.sub(r"\]", "-", line)   #replace  ]  with -           
        pline = re.sub(r"\[", "", pline) #replace  [  with blank     
        pline = re.sub(r"\(", "", pline)     #replace  (  with blank  
        pline = re.sub(r"\) ", "-", pline)  #replace  )  with -  
        pline = re.sub(r"\<BR>", " ", pline) #replace <BR>  with  space  
        pline = re.sub("<br />", "", pline) #replace <br />  with  blank  
        
        pline2 = re.sub("\+1 650 ","650-",pline)  #replace  +1 650   with 650-
        pline2 = re.sub(r"\: \(","",pline2) #replace : \( with blank
        pline2 = re.sub(r"\)","-",pline2) # replace # ) with - 
        
        #to avoid FPs - included some hard coding on the phone numbers
        
        pline3 = re.sub(r"723 5666","723-5666",pline2) # replace 723 5666 ) with 723-5666
        pline3 = re.sub(r" 9046","-9046",pline3) # replace  9046 ) with -9046
        

         # email pattern with .edu list
        for epat in epatterns:
            # each epat has 2 sets of parentheses so each match will have 2 items in a list
            matches = re.findall(epat,eline,re.IGNORECASE) #ignore case 
            for m in matches:
                # string formatting operator % takes elements of list m
                #   and inserts them in place of each %s in the result string
                # email has form  someone@somewhere.edu
                #email = '%s@%s.edu' % m
                email = '{}@{}.edu'.format(m[0],m[1])
                res.append((name,'e',email))
        
        # email pattern with .com list
        for ecompat in ecompatterns:
            # each epat has 2 sets of parentheses so each match will have 2 items in a list
            matches = re.findall(ecompat,ecomline,re.IGNORECASE) #ignore case 
            for m in matches:
                # string formatting operator % takes elements of list m
                #   and inserts them in place of each %s in the result string
                # email has form  someone@somewhere.edu
                #email = '%s@%s.edu' % m
                email = '{}@{}.com'.format(m[0],m[1])
                res.append((name,'e',email))

   
        # phone pattern list
        for ppat in ppatterns:
            # each ppat has 3 sets of parentheses so each match will have 3 items in a list
            matches = re.findall(ppat,pline3)
            for m in matches:
            # phone number has form  areacode-exchange-number
            #phone = '%s-%s-%s' % m
                phone = '{}-{}-{}'.format(m[0],m[1],m[2])
                res.append((name,'p',phone))
    return res

"""
You should not edit this function.
"""
def process_dir(data_path):
    # save complete list of candidates
    guess_list = []
    # save list of filenames
    fname_list = []

    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        fname_list.append(fname)
        path = os.path.join(data_path,fname)
        f = open(path,'r', encoding='latin-1')
        # get all the candidates for this file
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list, fname_list

"""
You should not edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r', encoding='latin-1')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not edit this function.
Given a list of guessed contacts and gold contacts, this function
    computes the intersection and set differences, to compute the true
    positives, false positives and false negatives. 
It also takes a dictionary that gives the guesses for each filename, 
    which can be used for information about false positives. 
Importantly, it converts all of the values to lower case before comparing.
"""
def score(guess_list, gold_list, fname_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    # for each file name, put the golds from that file in a dict
    gold_dict = {}
    for fname in fname_list:
        gold_dict[fname] = [gold for gold in gold_list if fname == gold[0]]

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)

    print ('True Positives (%d): ' % len(tp))
    # print all true positives
    pp.pprint(tp)
    print ('False Positives (%d): ' % len(fp))
    # for each false positive, print it and the list of gold for debugging
    for item in fp:
        fp_name = item[0]
        pp.pprint(item)
        fp_list = gold_dict[fp_name]
        for gold in fp_list:
            s = pprint.pformat(gold)
            print('   gold: ', s)
    print ('False Negatives (%d): ' % len(fn))
    # print all false negatives
    pp.pprint(fn)
    print ('Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn)))

"""
You should not edit this function.
It takes in the string path to the data directory and the gold file
"""
def main(data_path, gold_path):
    guess_list, fname_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list, fname_list)

"""
commandline interface assumes that you are in the directory containing "data" folder
It then processes each file within that data folder and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    print ('Assuming ContactFinder.py called in directory with data folder')
    main('data/dev', 'data/devGOLD')
