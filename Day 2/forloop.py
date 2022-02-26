i = []
count = 1
sum = 0
avg = 0

sum = float(sum)
avg = float(avg)

num = int(input(print("How many students are there?")))

for score in range(1, num + 1):
	score = float(input(print("Enter score for student ", count, ":")))
	count = count + 1
	i.append(score)
	sum = sum + score

avg = sum/num

print(i)
print(sum)
print(avg)