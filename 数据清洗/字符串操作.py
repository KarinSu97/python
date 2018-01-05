import string

#去除空格
s='  abf aS  '
print(s.strip())   #去除字符串两端的空格
print(s.lstrip())   #去除字符串左端的空格
print(s.rstrip())   #去除字符串右端的空格

#大小写转换
s='hello worlD'
print(s.upper())   #转换为大写字母
print(s.lower())   #转换为小写字母
print(s.capitalize())   #首字母大写,其他字母小写

#字符串位置索引
print(s.index("ll"))

#字符串比较
s1='abcdef'
s2='ghijkl'
print(s1==s2)
print(s1<s2)
print(s1>s2)

#字符串的分割与连接
s='abc,def,hij'
s1=s.split(',')
print(''.join(s1))   #字符串连接
print('\n'.join(s1))

#常用判断
print('1234abc'.isalnum())   #判断是否只出现字母和数字
print('\t1234abc'.isalnum())   #若出现特殊字符则返回false
print('123'.isdigit())   #判断是否是纯数字
print('abc'.isalpha())   #判断是否是纯字母
print('abc'.islower())   #判断是否是小写字母
print('ABC'.isupper())   #判断是否是大写字母
print('Hello World'.istitle())   #判断首字母是否是大写,每个单词首字母必须都是大写
print('   '.isspace())   #判断是否是空格

#格式化字符串输出
'''
%s   #字符串
%d   #整数
%u   #无符号整数
%o   #八进制
%x   #十六进制
%f   #浮点数
%e   #科学计数
'''

#字符串替换
val = 'a,b,  guido'
val.replace(',','::')

###正则表达式
#1
import re
text = "foo    bar\t baz  \tqux"
re.split('\s+', text)

regex = re.compile('\s+')
regex.split(text)

regex.findall(text)

#2
text = """Dave dave@google.com
Steve steve@gmail.com
Rob rob@gmail.com
Ryan ryan@yahoo.com
"""
pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'

# re.IGNORECASE 的作用是使正则表达式对大小写不敏感
regex = re.compile(pattern, flags=re.IGNORECASE)

regex.findall(text)

m = regex.search(text)
m

text[m.start():m.end()]

print(regex.match(text))

print(regex.sub('REDACTED', text))

#3
pattern = r'([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})'
regex = re.compile(pattern, flags=re.IGNORECASE)

m = regex.match('wesm@bright.net')
m.groups()

regex.findall(text)

print(regex.sub(r'Username: \1, Domain: \2, Suffix: \3', text))

#4
regex = re.compile(r"""
    (?P<username>[A-Z0-9._%+-]+)
    @
    (?P<domain>[A-Z0-9.-]+)
    \.
    (?P<suffix>[A-Z]{2,4})""", flags=re.IGNORECASE|re.VERBOSE)

m = regex.match('wesm@bright.net')
m.groupdict()


###pandas中矢量化的字符串函数
data = {'Dave': 'dave@google.com', 'Steve': 'steve@gmail.com',
        'Rob': 'rob@gmail.com', 'Wes': np.nan}
data = Series(data)

data

data.isnull()

data.str.contains('gmail')

pattern

data.str.findall(pattern, flags=re.IGNORECASE)

matches = data.str.match(pattern, flags=re.IGNORECASE)
matches

matches.str.get(1)

matches.str[0]

data.str[:5]



