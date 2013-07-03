#! /bin/python

import math
import random

#Bit usati per l'Hash 
#Usare 16 per l'hash cracking
BIT = 16

def MCD(a,b):
	t=0;
	if(b==0 or a==0):
		return 0
	if(a<b):
		t=b
		b=a
		a=t
	while(b != 0):
		t=b;
		b=a%b;
		a=t
		
	return a

def euclideEsteso(a, b):
    if b == 0:
        return (a, 1, 0)
    (d, ap, bp) = euclideEsteso(b , a%b)
    return (d, bp, ap - a/b * bp)

#Usando euclide esteso abbiamo "1 = ap + bd"
#Allora " ap = 1 mod(b) " con "p"  l'inverso di a mod b
def inv_modulo(a,m):
    (d, x, ml) = euclideEsteso(a, m)
    if d == 1:
        return x % m
    return 0

#inefficiente
def rootsGenerator(p):
	o = 1
	roots = range(p-1)
	for r in range(p-1):
		roots[r]=0
	z = 0
	for  r in range(2,p):
		k = (r**o)%p
		while (k > 1):
			o=o+1
			k = ((k%p) * (r%p))
		if (o == (p-1)) :
			roots[z] = r
			z=z+1
		o = 1
	return roots
	
#efficiente
def generatorFinder(p):
	if(p==2):
		return 1
	#Fattorizzo P-1 con pollardRho
	#uso una lista di 20 elementi
	#per esser sicuro che ci entrino
	#tutti i fattori
	b = range(20)
	b = [0]*20
	counter = 0
	tofactorize = (p-1)

	#prima di fattorizzare provo a 
	#dividere per 2
	while tofactorize%2 == 0:
		tofactorize = tofactorize/2
		b[0] = 2
	if b[0]!=0:
		counter = counter+1
	#trovo i fattori primi controllando
	#di non avere duplicati
	for i in range (1,20):
		t = pollardRho(tofactorize)
		if t not in b:
			b[i] = pollardRho(tofactorize)
			counter = counter+1
	a=2
	#metto i fattori distinti in un'altra lista
	factors = range(counter)
	i=0
	for x in b:
		if x!=0:
			factors[i] = x
			i=i+1
	#eseguo l'algoritmo
	for c in range(p-1):
		for x in range(counter):
			res = (a**((p-1)/factors[x]))%p
			if res == 1:
				break
			if (x==counter-1):
				return a
		a = a+1
		
#fattorizzazione
def pollardRho(N):
        if N%2==0:
                return 2
        x = random.randint(1, N-1)
        y = x
        c = random.randint(1, N-1)
        g = 1

	#uso come funzione (x^2 + c)
        while g==1:             
                x = ((x*x)%N+c)%N
                y = ((y*y)%N+c)%N
                y = ((y*y)%N+c)%N
                g = MCD(abs(x-y),N)
	
	#G = n vale come un failure 
        return g

#usato per il test di miller-rabin
def factorizebytwo(n):
	t=n
	if(n%2 == 0): 
		return [0,0,0,0]
	n = n-1
	i=0
	r=0
	while(n%2 == 0):
		n = n/2
		i=i+1
	#print str(t-1)+' = 2^'+str(i)+' * '+str(n)
	return [t-1,2,i,n]

#test di miller-rabin
def millerRabin(p,t):
	if(p%2 == 0):
		return [0,p]

	#Scrivo p come (2^S)*K
	fact = factorizebytwo(p)

	#Eseguo t round decisi a priori
	for i in range (0,t):
		#scelgo una base
		a = random.randrange(2,p-2)
		#primo tentativo. Se va a 
		#buon fine non entro nel ciclo
		y = (a**fact[3])
		y=y%p
		if (y != 1 and y!=p-1):
			j=1
			#Arrivo fino a S iterazioni
			while (j<= fact[2] and y!=p-1):
				y=(y**2)%p
				if(y==1):
					return [0,p]
				j=j+1
			#Dopo S iterazioni se non 
			#trovo -1, N non primo
			if(y != p-1):
				return [0,p]	
	#se non sono mai uscito dai cicli allora
	#N viene considerato primo
	return [1,p]

def generateLargePrimeNumber():
	x=[0,0]
	while(x[0]==0):
		x = millerRabin( random.randrange(10**3,10**4), 5 )
	return x

def generateElGamalRandomNumber(p):
	k=random.randrange(10**2,10**3)
	while(MCD(k,p-1)!=1):
		k=random.randrange(10**2,10**3)
	return k

def hashing(message):
	m = convertMessageBin(message)
	m = m + '0'*(BIT - (len(m)%BIT))
	numRighe = int(math.ceil(len(m)/float(BIT)))
	x = [[0 for i in range(BIT)] for i in range(numRighe)]
	result = range(BIT)
	tmp = '0'

	#Divisione in blocchi del messaggio di lunghezza BIT
	for riga in range(numRighe):
		x[riga] = m[BIT*riga:BIT*(riga+1)]
	
	#XOR delle colonne
	for i in range(BIT):
		for riga in range(numRighe):
			tmp = int(tmp)  ^ int(x[riga][i]) 
		result[i]=int(tmp)

	#Conversione in esadecimale del digest
	k = int(''.join(str(i) for i in result))
	k = "0b"+str(k)
	k = hex(int(k,2))
	k=k.replace("0x",'')
	k=k.replace("L",'')
	return k

def convertMessageBin(m):
	l = m.encode("hex")
	l = bin(int(l,16))
	l = l.replace("0b",'')
	return l

def convertMessageDec(m):
	l = m.encode("hex")
	l = int(l,16)
	return l

#fattorizzazione di brent (non mia)
def brent(N):
        if N%2==0:
                return 2
        y,c,m = random.randint(22, N-1),random.randint(23, N-1),random.randint(25, N-1)
        g,r,q = 1,1,1
        while g==1:             
                x = y
                for i in range(r):
                        y = ((y*y)%N+c)%N
                k = 0
                while (k<r and g==1):
                        ys = y
                        for i in range(min(m,r-k)):
                                y = ((y*y)%N+c)%N
                                q = q*(abs(x-y))%N
                        g = MCD(q,N)
                        k = k + m
                r = r*2
        if g==N:
                while True:
                        ys = ((ys*ys)%N+c)%N
                        g = MCD(abs(x-ys),N)
                        if g>1:
                                break        
        return g  

def computePublicKey():
	#Calcolo P,alfa,beta e stampo la chiave pubblica
	p = generateLargePrimeNumber()
	a = random.randrange(1,(p[1]-2))
	alfa = generatorFinder(p[1])
	beta = (alfa**a)%p[1]
	print "Public Key is: [ "+str(p[1])+" , "+str(alfa)+" , "+str(beta)+" ]"
	return [p[1],alfa,beta,a]

def signMessage(m,p,alfa,a,k):
	#prendo il digest del messaggio
	mess = hashing(m)
	#lo converto in decimale 
	mex = int(mess,16)%p
	#k = generateElGamalRandomNumber(p)
	#calcolo (r,s) che definiscono la firma
	r = (alfa**k)%p
	inversok = inv_modulo(k,p-1)
	s =  ( inversok * (mex- (a*r) ) )%(p-1) 
	print "Messaggio inviato da Alice:\n"+m
	print "Message signed: ["+str(mess)+" , "+str(r)+" , "+str(s)+" ]\n"
	return[mex,r,s]

def checkSign(pk,sm):
	v1 =( ((pk[2]**sm[1]))%pk[0] * ((sm[1]**sm[2])%pk[0]) )%pk[0]
	v2 = ( pk[1]**sm[0] )%pk[0]
	if(v1==v2):
		print "Firma verificata"	

#i parametri sono le 2 firme e la chiave pubblica (p,alfa,beta)
def crack(s1,s2,p,m1,m2,alfa,beta):
	print "\nTentativo di cracking della firma da parte di Eva:" 
	y = MCD(s1[2]-s2[2],p-1)
	#controllo il num. di soluzioni possibili
	y=abs(y)
	mn1=int(hashing(m1),16)%p
	mn2=int(hashing(m2),16)%p
	#calcolo la prima soluzione
	x = inv_modulo( (s1[2]-s2[2])/y , (p-1)/y )
	k = x*((mn1-mn2)/y)%((p-1)/y)
	t=y-1
	if (alfa**k%p)==s1[1]:	
		print "Valore di K recuperato: "+str(k)	
	#se non va bene calcolo tutte le altre
	else:
		while(t!=0):
			value = ( k+(t*(p-1)/y) )%(p-1) 
			if (alfa**value%p)==s1[1]:
				print "Valore di K recuperato: "+str(value)	
				k=value
				break		
			t=t-1
	#Lo stesso procedimento lo uso per il calcolo
	#di A, conoscendo K
	y =MCD(s1[1],p-1)
	y = abs(y)
	x = inv_modulo(s1[1]/y,(p-1)/y)
	a = x*((mn1-s1[2]*k)/y)%((p-1)/y)
	t=y-1
	if(alfa**a%p == beta):
		print "Valore di A recuperato: "+str(a)	
	else:
		while(t!=0):
			value = ( a+(t*(p-1)/y) )%(p-1) 
			if (alfa**value%p)==beta:
				print "Valore di A recuperato: "+str(value)	
				break	
			t=t-1
 
def crackHash(m):
	counter=0
	for i in range(len(m)):
		if m[i].isdigit():
			counter=counter+1
		else:
			counter = 0

		#se trovo un a serie di 3 numeri (probabilmente
		#una somma in denaro) mi fermo
		if (counter==3):
			break

	#Aumento di 4 la lunghezza del messaggio
	mex=range(len(m)+4)
	mex = m[:i]

	#Accodo alle cifre 4 zeri. Lavorando a 16 bit, 4 zeri 
	#producono esattamente 2 nuove righe nella matrice
	#di hashing
	mex = mex + "0000"
	mex = mex + m[i:]
	return [hashing(mex),mex]
	
		


def init():
	pk = computePublicKey()
	print "La A selezionata e': "+str(pk[3])
	m1 = "Con il presente contratto Bob si impegna all\'acquisto di una vecchia moto usata non funzionante al costo di 200 euro, entro la data xxx."
	m2 = "Attesa conferma"
	k = generateElGamalRandomNumber(pk[0])
	print "Il K selezionato e': "+str(k)+"\n"
	signed = signMessage(m1,pk[0],pk[1],pk[3],k)
	signed1 = signMessage(m2,pk[0],pk[1],pk[3],k)
	checkSign(pk,signed)
	checkSign(pk,signed1)
	print "\nAlice tenta di imbrogliare Bob trovando uno stesso hash con un messaggio leggermente differente:"
	ch = crackHash(m1)
	print "\nTrovato hash \""+ch[0]+"\" corrispondente a\n"+ch[1]
	crack(signed,signed1,pk[0],m1,m2,pk[1],pk[2])
	

init()
	
