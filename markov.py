import sys, random, argparse, os, re, time
config_name = 'markov_config.txt'
defaults= {'file_name':'male_names.txt','token_len':3, 'max_len':30, 'n_words':10}
_defaults = defaults.copy()
silent = False

def p(*args, **kwargs):
    if not silent:
        print(*args, **kwargs)

def open_config():
    global defaults, config_name
    try:
        with open(config_name, 'r') as config:
            rows = [ x[:-1] for x in config.readlines() ]
            p(rows)
            defaults['file_name'] = rows[0]
            defaults['token_len'] = int(rows[1])
            defaults['max_len']   = int(rows[2])
            defaults['n_words']   = int(rows[3])
    except:
        p('Error in config file, creating a new one')
        edit_config(**defaults)

def edit_config():
    global defaults, config_name
    p(f'Editing {config_name}')
    with open(config_name, 'w') as config:
        config.write(f"{defaults['file_name']}\n")
        config.write(f"{defaults['token_len']}\n")
        config.write(f"{defaults['max_len']}\n")
        config.write(f"{defaults['n_words']}\n")
    p('Config edited')

class MarkovChain(object):
    def __init__(self, list_, char_len):
        self.list_ = set(list_)
        self.char_len = char_len
        self._make_new()
    def from_file(filename, char_len):
        with open(defaults['file_name']) as names:
            ws_pattern = re.compile(r'\s+')
            names = [re.sub(ws_pattern,'',x).lower() for x in names.readlines() if '#' not in x]
            m = MarkovChain(names, defaults['token_len'])
        return m
    def _make_new(self):
        '''Internal method for updating the chain'''
        self.chain = {'_initial':{}} #'_names':set(self.list_)
        for name in self.list_:
            name_d = str(name) + '.'
            # iterate every next character until the end of the word
            for i in range(0, len(name_d) - self.char_len):
                tuple_ = name_d[ i  : i + self.char_len ]
                next_  = name_d[ i+1: i + self.char_len + 1 ]
                if tuple_ not in self.chain:
                    # entry is the character piece in the chain
                    entry = self.chain[tuple_] = {}
                else:
                    entry = self.chain[tuple_]
                if i == 0:
                    # update inits list with ## of cases (autocreate if not present)
                    self.chain['_initial'][tuple_] = self.chain['_initial'].get(tuple_,0) + 1
                # update entry with the next value in the word (sutocreate if missing)
                entry[next_] = entry.get(next_, 0) + 1
    def update(self, list_=None, char_len=None, what='replace'):
        '''Allows to change the chain without rewriting all'''
        changed = False
        if char_len is not None:
            #print('Changed chain length')
            self.char_len = char_len
            changed = True
        if list_ is not None:
            list_ = set(list_)
            #print('Changed chain elements')
            if what == 'replace':
                self.list_ = list_
            elif what == 'add':
                self.list_ = self.list_.union(list_)
            changed = True
        if changed:
            self._make_new()
    def generate_word(self, max_len = 30):
        tuple_ = self._generate_next_letter('_initial')
        result = [tuple_]
        while True:
            #print(f'Tempresult:{result}')
            #print(f'Last_tuple:{tuple_}')
            tuple_ = self._generate_next_letter( tuple_ ) # generate next item from previous tuple
            last_char = tuple_[-1] #check last character from tuple itself
            if last_char == '.' or sum([len(x) for x in result]) >= max_len:
                break #word end
            result.append(last_char) #append last character to list
            #print(result)
        generate = ''.join(result)
        if generate not in self.list_:
            return generate
        else:
            return self.generate_word(max_len=max_len)
    def _generate_next_letter(self, token):
        #print(f'Token is {token}')
        items = self.chain[token]
        rnd = random.randint( 0, sum(items.values()) - 1 ) 
        #print(rnd)
        for item in items:
            rnd -= items[item]
            if rnd < 0:
                #print(item)
                return item

def help_():
    global defaults
    helpstring='''markov.py Markov-Chain Based Name Generator
default file_name    = {fn}
default token_length = {tl}
default name_length  = {nl}
***************************************************
Commands:
***************************************************
 {scr}                  to display this message
 {scr} <n> <modifiers>  to display <n> new words with <modifiers>
Available modifiers (### are not yet implemented):
 ...{scr} -f=<filename>    to use a different file than the default one
 ...{scr} -t=<charlen>     to change the length of the tokens
 ...{scr} -l=<n>           to change the maximum word length
### ...{scr} -u               append changes to default configuration
### ...{scr} -d               to restore default configuration
    '''
    helpstring = helpstring.format(fn = defaults['file_name'],
                                   nl = defaults['max_len'],
                                   tl = defaults['token_len'],
                                   scr=sys.argv[0])
    print(helpstring)

def main():
    global defaults, _defaults
    os.system('cls')
    p(sys.argv)
    if len(sys.argv) == 1:
        help_()
        return
    p('Checking config file')
    open_config()
    # parse arguments; check if theres a variable numeric
    if sys.argv[1].isnumeric():
        n = sys.argv[1]
        argstart = 2
    else:
        n = defaults['n_words']
        argstart = 1
    mods = sys.argv[argstart:]
    for mod in mods:
        #p(mod)
        if '-f=' in mod:
            defaults['file_name'] = mod[3:]
            p(f"Using file {defaults['file_name']}")
        elif '-t=' in mod:
            defaults['token_len'] = int(mod[3:])
            p(f"Using token_len {defaults['token_len']}")
        elif '-l=' in mod:
            defaults['max_len'] == mod[3:]
            p(f"Using max_len {defaults['max_len']}")
        elif '-u' in mod:
            edit_config()
            p("Updating Config File...")
        elif '-d' in mod:
            defaults = _defaults.copy()
            edit_config()
            p("Restoring original config")
        else:
            p(f'Unrecognised parameter {mod}')
    m = MarkovChain.from_file(defaults['file_name'], defaults['token_len'])
    print(f'Printing {n} words...')
    for i in range(int(n)):
        print(f"{i}\t{m.generate_word(max_len=defaults['max_len'])}")
    print('End')
    time.sleep(3)

if __name__ == '__main__':
    main()
