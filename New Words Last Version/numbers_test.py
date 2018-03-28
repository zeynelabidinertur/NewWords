import random
x = []
for a in range(20):
    x.append(random.randrange(-1,2))
x = [0, 0, -1, 1, 1, 0, 0, 1, -1, 1, 0, -1, 0, 0, 0, 1, -1, 1, 1, 0]
print x, sum(x)
total_num = 0
final_range = [0,0]
for a in range (len(x)):
    #if final_range[1]-final_range[0]:
    if x[a]+total_num >= 0:
        final_range[1] = a
    else:
        final_range[0] = a
    print final_range
