from subprocess import call
import os

# def get_size(directory):
# 	start_path = directory
# 	total_size = 0
# 	for dirpath, dirnames, filenames in os.walk(start_path):
# 		for f in filenames:
# 			fp = os.path.join(dirpath, f)
# 			total_size += os.path.getsize(fp)
# 	return total_size


def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    if os.path.isfile(folder):
    	return os.path.getsize(folder)
    else:
    	for item in os.listdir(folder):
        	itempath = os.path.join(folder, item)
        	if os.path.isfile(itempath):
        		total_size += os.path.getsize(itempath)
        	elif os.path.isdir(itempath):
        		total_size += getFolderSize(itempath)
    return total_size
# def get_size(folder):
# 	folder_size = 0
# 	for (path, dirs, files) in os.walk(folder):
#   		for file in files:
#   			filename = os.path.join(path, file)
#     		folder_size += os.path.getsize(filename)
# 		print "Folder = %0.1f MB" % (folder_size/(1024*1024.0))
# 	return  folder_size/(1024*1024.0)

def copyDirectory(dir_name, dest):
	size = getFolderSize (dir_name) / (1024 * 1024)
	print "Directory " + dir_name + " = " + str(size)
	if size < 3000:
		print "hiho"
		call(["cp", "-r", dir_name, dest])
	else:
		if os.path.isfile(dir_name):
			print dir_name + "could not be copied because file is too large"
			return
		else:
			extension = 0
			for item in os.listdir(dir_name):
				itempath = os.path.join(dir_name, item)
				itemSize = getFolderSize(itempath) / (1024*1024)
				print itempath
				if itemSize < 3000:
					call(["cp", "-r", itempath, dest + "/" + item])
				elif os.path.isfile(itempath):
					print dir_name + "could not be copied because file is too large"
				else:
					totalSubSize = 0
					extension = 1
					for subItem in os.listdir(itempath):
						#print subItem + "FUCK"
						subItemPath = os.path.join(itempath, subItem)
						subItemSize = getFolderSize(subItemPath) / (1024*1024)
						#print subItemPath
						#print subItemSize
						#print totalSubSize

						if subItemSize + totalSubSize < 3000:
							totalSubSize += subItemSize
							call(["mkdir", "-p", dest + "/" + item + "-" + str(extension)])
							call([ "cp", "-r", subItemPath, dest + "/" + item + "-" + str(extension) + '/' + subItem])
						elif subItemSize < 3000:
							extension += 1
							totalSubSize = subItemSize
							call(["mkdir", "-p", dest + "/" + item + "-" + str(extension)])
							call([ "cp", "-r", subItemPath, dest + "/" + item + "-" + str(extension) + '/' + subItem])
						else:
							copyDirectory(subItemPath, dest)

dir1 = raw_input("Enter directory1 path: ")
dest = raw_input("Enter destination path: ")
copyDirectory(dir1, dest)