import random

create_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
print(create_code)
