l1 = [1, 2, 3]
l2 = [4, 5, 6]
l1 = l2.copy()
l2.append(7)

print(l1)
print(l2)
del(l2[1:3])
print(l2)
