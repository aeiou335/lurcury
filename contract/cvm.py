"""
    Restrictions:
        1) must have "#print(locals())" after each class
        2) must have "return locals()" in each class function
        3) indentation in head and tail cannot be changed!
"""
import pickle

class Contract():

    def __init__(self, contract=None):
        # Contract data members: head, tail, params(to store variables; save to db?)
        self.head = "\ndef main():\n"+"\n\tcls_params = {}\n"
        self.tail = '''
	#cls_params[''] = #function
	return locals()#callback
x = main()
		'''
        self.params = dict()
        # Contract file I/O
        with open(contract) as file:
            self.body = file.read()
        file.close()
    
    def save(self):
        body = self.parse()
        contract = self.head + body + self.tail
        print(contract)
        local_dict = {}
        exec(contract, globals(), local_dict)
        self.params = local_dict['x']
        print(self.params)

    def run(self, func=None):
        contract = self.head + self.body + self.tail
        # TODO: fetch old params from db and replace globals
        contract = contract.replace('#cls_params[\'\']', 'cls_params[\'%s\']' % func)
        contract = contract.replace('#function', '%s()' % func)
        contract = contract.replace('locals()#callback', 'cls_params')
        print(contract)

        local_dict = {}
        exec(contract, globals(), local_dict)
        print(local_dict['x'])		
        # save new params to db: ints, bools....
        #cb = func.split(".")
        for (key, val) in local_dict['x'][func].items():
            try:
                self.params[key] = val
            except KeyError:
                print("Found local params...will ignore.")
        
        print(self.params)

    def parse(self):
        body = self.body
        idx = 0
        while idx < len(body):
            print("searching for class...")
            class_pos = body.find('class', idx, -1)
            if class_pos != -1:
                print("found class!")
                paren_pos = body.find(':', class_pos, -1)
                class_name = body[class_pos+5:paren_pos]
                body = body.replace('#print(locals())', 'cls_params[\'%s\'] = locals()'%(class_name.strip()), 1)
                idx = paren_pos
            else:
                break
        return body

c = Contract("contract.txt")
c.save()
c.run("hop.go")
