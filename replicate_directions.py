

# Kimura
kimuraA = open("./src/houses/apartments/kimura/kimura_a.pnml", "rt")
kimuraB = open("./src/houses/apartments/kimura/kimura_b.pnml", "wt")
for line in kimuraA:
	kimuraB.write(line.replace('_a_', '_b_'))
kimuraA.close()
kimuraB.close()

kimuraA = open("./src/houses/apartments/kimura/kimura_a.pnml", "rt")
kimuraS = open("./src/houses/apartments/kimura/kimura_s.pnml", "wt")
for line in kimuraA:
	kimuraS.write(line.replace('_a_', '_s_'))
kimuraA.close()
kimuraS.close()

kimuraA = open("./src/houses/apartments/kimura/kimura_a.pnml", "rt")
kimuraE = open("./src/houses/apartments/kimura/kimura_e.pnml", "wt")
for line in kimuraA:
	kimuraE.write(line.replace('_a_', '_e_'))
kimuraA.close()
kimuraE.close()

kimuraA = open("./src/houses/apartments/kimura/kimura_a.pnml", "rt")
kimuraW = open("./src/houses/apartments/kimura/kimura_w.pnml", "wt")
for line in kimuraA:
	kimuraW.write(line.replace('_a_', '_w_'))
kimuraA.close()
kimuraW.close()

kimuraA = open("./src/houses/apartments/kimura/kimura_a.pnml", "rt")
kimuraN = open("./src/houses/apartments/kimura/kimura_n.pnml", "wt")
for line in kimuraA:
	kimuraN.write(line.replace('_a_', '_n_'))
kimuraA.close()
kimuraN.close()