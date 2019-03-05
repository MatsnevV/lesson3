def dozapis(new_ln):
    with open('referat2.txt', 'a', encoding='utf-8') as referat2:
        referat2.write(new_ln, '\n')
        #referat2.write('\n')

with open('referat.txt', 'r', encoding='utf-8') as referat:
    ln = referat.read()

a = str(len(ln))
b = str(len(ln.replace(" ", ",").split(',')))
c = str(ln.replace(".", "!"))

dozapis(a)
dozapis(b)
dozapis(c)


