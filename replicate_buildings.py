
# Murakami
murakami3L = open("./src/houses/apartments/murakami/murakami_3L.pnml", "rt")
murakami4L = open("./src/houses/apartments/murakami/murakami_4L.pnml", "wt")
for line in murakami3L:
	murakami4L.write(line.replace('3L', '4L'))
murakami3L.close()
murakami4L.close()

murakami3L = open("./src/houses/apartments/murakami/murakami_3L.pnml", "rt")
murakami5L = open("./src/houses/apartments/murakami/murakami_5L.pnml", "wt")
for line in murakami3L:
	murakami5L.write(line.replace('3L', '5L'))
murakami3L.close()
murakami5L.close()

murakami3L = open("./src/houses/apartments/murakami/murakami_3L.pnml", "rt")
murakami6L = open("./src/houses/apartments/murakami/murakami_6L.pnml", "wt")
for line in murakami3L:
	murakami6L.write(line.replace('3L', '6L'))
murakami3L.close()
murakami6L.close()

# Nakamura
nakamura3L = open("./src/houses/apartments/nakamura/nakamura_3L.pnml", "rt")
nakamura4L = open("./src/houses/apartments/nakamura/nakamura_4L.pnml", "wt")
for line in nakamura3L:
	nakamura4L.write(line.replace('3L', '4L'))
nakamura3L.close()
nakamura4L.close()

nakamura3L = open("./src/houses/apartments/nakamura/nakamura_3L.pnml", "rt")
nakamura5L = open("./src/houses/apartments/nakamura/nakamura_5L.pnml", "wt")
for line in nakamura3L:
	nakamura5L.write(line.replace('3L', '5L'))
nakamura3L.close()
nakamura5L.close()

nakamura3L = open("./src/houses/apartments/nakamura/nakamura_3L.pnml", "rt")
nakamura6L = open("./src/houses/apartments/nakamura/nakamura_6L.pnml", "wt")
for line in nakamura3L:
	nakamura6L.write(line.replace('3L', '6L'))
nakamura3L.close()
nakamura6L.close()

# Temple
temple01 = open("./src/houses/landmarks/temple/temple_01.pnml", "rt")
temple02 = open("./src/houses/landmarks/temple/temple_02.pnml", "wt")
for line in temple01:
	temple02.write(line.replace('temple_01', 'temple_02'))
temple01.close()
temple02.close()
