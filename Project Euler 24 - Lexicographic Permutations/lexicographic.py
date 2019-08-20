import math

palette_digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ordered_digits = []

# We use 999,999 because 0 would be the first permutation
# in lexicographic order
current_location = 999999
for i in range(0, len(palette_digits)):
    a = math.factorial(len(palette_digits) - 1)
    b = current_location // a
    ordered_digits.append(palette_digits.pop(b))
    current_location -= a * b

for i in ordered_digits:
    print(i, end="")
print()
