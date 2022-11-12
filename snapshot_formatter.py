# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 17:08:20 2022

@author: NewAdmin
"""

"""Formatting snapshot string
"""
snapshotformatted = ""

""" function that replaces the nth occurrence of a substring within a string
"""
def nth_repl(s, sub, repl, n):
    find = s.find(sub)
    # If find is not -1 we have found at least one match for the substring
    i = find != -1
    # loop util we find the nth or we find no match
    while find != -1 and i != n:
        # find + 1 means we start searching from after the last match
        find = s.find(sub, find + 1)
        i += 1
    # If i is equal to n we found nth match so replace
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s


def string_formatter(ssoriginal):

    ss1 = ssoriginal
    ss1 = ss1.replace("{'map': ","", 1)
    ss1 = nth_repl(ss1," 'round': ", "", 2)
    ss1 = ss1.replace(" 'allplayers': ","", 1)
    ss1 = ss1.replace(" 'phase_countdowns': ","", 1)
    ss1 = ss1.replace(" 'auth': ","", 1)
    ss1 = ss1.replace("True","true")
    ss1 = ss1.replace("False","false")
    ss1 = ss1[:-1]
    ss1 = ss1.replace("'", '"')
    
    #splitting map and round
    string = ss1
    temp = string.split('}')
    splt_char = "}"
    res = splt_char.join(temp[:3]), splt_char.join(temp[3:])
    res = list(res)
    string1 = str(res[0]) + '}'
    res[0] = str(string1)
    ss1 = res
    string1 = str(ss1[-1])[1:]
    ss1[-1] = str(string1)
    
    #splitting round and allplayers
    string = str(ss1[-1])
    string = string.split("}", 1)
    del ss1[-1]
    string1 = str(string[0]) + '}'
    string[0] = str(string1)
    ss1 = ss1 + string
    string1 = str(ss1[-1])[1:]
    ss1[-1] = str(string1)
    
    #splitting allplayers and phase_countdowns
    string = str(ss1[-1])
    temp = string.split('}')
    res = splt_char.join(temp[:-3]), splt_char.join(temp[-3:])
    del ss1[-1]
    res = list(res)
    string1 = str(res[0]) + '}'
    res[0] = str(string1)
    ss1 = ss1 + res
    string1 = str(ss1[-1])[1:]
    ss1[-1] = str(string1)
    
    #splitting phase_countdowns & auth
    string = str(ss1[-1])
    string = string.split('}', 1)
    del ss1[-1]
    string1 = str(string[0]) + '}'
    string[0] = str(string1)
    ss1 = ss1 + string
    string1 = str(ss1[-1])[1:]
    ss1[-1] = str(string1)

    return ss1
