from PIL import Image

def getSmallPictureTools(file_old, file_new, length=240):
	'''
	压缩图片
	:param file:
	:return:
	'''
	try:
		img = Image.open(file_old)
		width, height = img.size
		if width >= length:
			times = width // length
		else:
			times = 1
		out = img.resize((width // times, height // times))
		out.save(file_new)
		img.close()
		return
	except:
		return