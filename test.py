file_path = f"test_text.csv"
lines = ""
with open(file_path, 'r') as f:
    lines = f.readlines()

"""
for x in range(len(lines)-1):
    line = lines[x+1].split(",")
    biome = line[0]
    percentage = line[1][:len(line[1])-1]
    #print(f"{biome}: {percentage}")
    print(f"{percentage}")
"""