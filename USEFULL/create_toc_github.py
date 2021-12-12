import os

#edit here
projectname = "https://github.com/vanhohen/ADNinja/"

filepath = os.path.abspath(__file__).split("\\")[:-2]

tmp = ""

for i in (filepath):
    tmp = tmp + str(i) + "\\"


given_path = (tmp)

with open("ADNinja\\README.md", "w") as file:
    for path, dirs, files in os.walk(given_path):
        folder_name = path.split("\\")[-1]

        #inside folder .git contains github files so we will ignore those and skip this 
        if ".git" in path:
            continue

        file.writelines("# %s\n" % (str(folder_name)))
        
        for f in files:
            folder_name_edited = str(folder_name.replace(" ", "%20"))
            f2 = str(f.replace(" ", "%20"))
            link = "[%s](%s)" % (f.replace(".md", ""),str(projectname + "blob/main/" + folder_name_edited + "/" + f2))
            file.writelines(str(link) + "\n\n")



