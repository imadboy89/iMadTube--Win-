import re

patt_func = "^function(\s[a-zA-Z]+\([^\)]+\))"
dict_tr = {"\.slice\(([0-9]+)\)":"[\\1:]","\.reverse\(\)":"[::-1]","\s([a-zA-Z])\.join\(\"\"\)":" \"\".join(\\1)","([a-zA-Z])\.length":"len(\\1)",patt_func:"def\\1:","\{":":","\}":"\n",}

str = """function bz(a){a=a.split("");a=cz(a,61);a=cz(a,5);a=a.reverse();a=a.slice(2);a=cz(a,69);a=a.slice(2);a=a.reverse();return a.join("")}function cz(a,b){var c=a[0];a[0]=a[b%a.length];a[b]=c;return a};"""

str_ = re.split(";|\{|\}",str)

#str_ = str.split(";")
new_func = []
spaces_4 = False
for s in str_:
    #print s
    is_ok = False
    for pattern,new in dict_tr.items():
        if re.search(pattern,s):
            if patt_func == pattern:
                spaces_4= False
            new_s = re.sub(pattern,new,s)
            if spaces_4:new_s="%s%s"%(" "*4,new_s)
            new_func.append(new_s)
            is_ok = True
            if patt_func == pattern:
                spaces_4= True
            break
    if spaces_4:s="%s%s"%(" "*4,s)
    if not is_ok : new_func.append(s)
print "\n".join(new_func)