# Yanagi
hayashi3L = open("./src/houses/apartments/hayashi/hayashi_3L.pnml", "rt")
hayashi4L = open("./src/houses/apartments/hayashi/hayashi_4L.pnml", "wt")
for line in hayashi3L:
	hayashi4L.write(line.replace('_xL_', '5L'))
hayashi3L.close()
hayashi4L.close()

hayashi3L = open("./src/houses/apartments/hayashi/hayashi_3L.pnml", "rt")
hayashi5L = open("./src/houses/apartments/hayashi/hayashi_5L.pnml", "wt")
for line in hayashi3L:
	hayashi5L.write(line.replace('3L', '5L'))
hayashi3L.close()
hayashi5L.close()

hayashi3L = open("./src/houses/apartments/hayashi/hayashi_3L.pnml", "rt")
hayashi6L = open("./src/houses/apartments/hayashi/hayashi_6L.pnml", "wt")
for line in hayashi3L:
	hayashi6L.write(line.replace('3L', '6L'))
hayashi3L.close()
hayashi6L.close()
