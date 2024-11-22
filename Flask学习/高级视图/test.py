dic = {
    'a': 'A'
}


# b = 'b'

# dic.b = 'B'

def test():
    print('test')


dic['fn'] = test

dic['fn']()
print(dic)

res = dic.pop('a')
print('res', res)
print('dic', dic)
