#!/usr/bin/env python3

import yara
import os
import timeout_decorator 

@timeout_decorator.timeout(20)
def main():
    rule = []
    print('rule:')
    
    while True:
        l = input()
        if len(l) == 0:
            break
        rule.append(l)
    
    rule = '\n'.join(rule)
    try:
        
        print(f'OK. Now I find the malware from this rule:\n{rule}')
        
        compiled = yara.compile(source=rule)
        
        for root, d, f in os.walk('.'):
            for p in f:
                file = os.path.join(root, p)
                matches = compiled.match(file, timeout=60)
                if matches:
                    print(f'Found: {file}, matched: {matches}')
                else:
                    print(f'Not found: {file}')
    
    except:
        print('Something wrong')

if __name__ == '__main__':
    try:
        main()
    except timeout_decorator.timeout_decorator.TimeoutError:
        print("Timeout")
