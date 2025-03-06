from collections import deque

# Initialize an empty deque
d = deque()
print(f"Initial state: {d}")

# Step 1: Append to the right (rear)
d.append(10)
print(f"After append(10): {d}")

# Step 2: Append to the right again
d.append(20)
print(f"After append(20): {d}")

# Step 3: Append to the left (front)
d.appendleft(30)
print(f"After appendleft(30): {d}")

# Step 4: Remove from the left (front)
removed = d.popleft()
print(f"After popleft(): {d}, Removed: {removed}")

# Step 5: Append to the right
d.append(40)
print(f"After append(40): {d}")

# Step 6: Remove from the right (rear)
removed = d.pop()
print(f"After pop(): {d}, Removed: {removed}")

# Step 7: Append to the left
d.appendleft(50)
print(f"After appendleft(50): {d}")

# Step 8: Append to the right
d.append(60)
print(f"After append(60): {d}")

# Additional operations
print(f"Length of deque: {len(d)}")
print(f"First element: {d[0]}")
print(f"Last element: {d[-1]}")

# Iterate through the deque
print("Iterating through the deque:")
for item in d:
    print(item, end=" ")
print()

# Clear the deque
d.clear()
print(f"After clear(): {d}")
