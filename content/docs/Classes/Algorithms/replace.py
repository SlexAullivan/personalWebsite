
onOpen = True

file = open("balancedBST.md", "r")
file2 = open("balancedBST(1).md", "w+")

for line in file:
    for char in line:
        if char == "$":
            if onOpen:
                file2.write("{{<katex>}}")
                onOpen = False
            else:
                file2.write("{{</katex>}}")
                onOpen = True
        else:
            file2.write(char)    

file.close()
file2.close()
