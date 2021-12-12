import os

#edit here, you project url
projectname = "https://github.com/vanhohen/ADNinja/"


#todo
#how depth the script since it is inside folder directy -1, is goes -2 -3 -4
filepath = os.path.abspath(__file__).split("\\")[:-2]

tmp = ""

for i in (filepath):
    tmp = tmp + str(i) + "\\"


given_path = (tmp)

print (given_path)

ignore_folders = []

ignore_folders.append(given_path)
ignore_folders.append(".git")
print (ignore_folders)

with open(given_path + "\\README.md", "w") as file:
    for path, dirs, files in os.walk(given_path):
        folder_name = path.split("\\")[-1]
        

        #will make a list about it, if inside list ignore
        #inside folder .git contains github files so we will ignore those and skip this 
        if ".git" in path:
            continue
        
        #i dont want README inside README xD
        if not folder_name:
            continue
        
        print (folder_name)
        file.writelines("# %s\n" % (str(folder_name)))
        
        for f in files:
            folder_name_edited = str(folder_name.replace(" ", "%20"))
            f2 = str(f.replace(" ", "%20"))
            link = "[%s](%s)" % (f.replace(".md", ""),str(projectname + "blob/main/" + folder_name_edited + "/" + f2))
            file.writelines(str(link) + "\n\n")



