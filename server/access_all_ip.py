path = "exec/"
for i in range(15):
	open(path + "192.168." + str(i+1) + ".254", "w").write("NEW")

