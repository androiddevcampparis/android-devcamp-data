import urllib,csv
import json, time
#import simplejson as json

#http://www.portailsig.org/content/python-geocodage-geolocalisation

#friendly function of geocode_json
def geocode_csv(addr, api_key=''):
	url = "http://maps.google.com/maps/geo?q=%s&output=csv&api_key=%s" % (urllib.quote(addr), urllib.quote(api_key))
	coord = urllib.urlopen(url).read().split(',')
	#coortext = 'lat: %s,long: %s' % (coord[2],coord[3])
	return coord[2:4] # lat / long

#friendly function of geocode_csv
def geocode_json(addr, api_key=''):
	url = "http://maps.google.com/maps/geo?q=%s&output=json&api_key=%s" % (urllib.quote(addr), urllib.quote(api_key))
	data = urllib.urlopen(url).read()
	code = json.loads(data)['Status']["code"]
	if code != 200:
		print " -> bad error code: %d" % code,
		return None
	accuracy = json.loads(data)['Placemark'][0]['AddressDetails']['Accuracy']
	if accuracy < 6:
		print " -> bad accuracy: %d" % accuracy,
		return None

	coord = json.loads(data)['Placemark'][0]['Point']['coordinates']
	coord = [ coord[1], coord[0] ]
	return coord # lat / long


def update_csv(filename='export opendata voies actuelles 2012-01-17_utf8.csv'):
	reader = csv.reader(open(filename, 'rb'), delimiter=';')
	writer = csv.writer(open(filename[:-4] + '_new.csv', 'wb'), delimiter='\t')

	titles = reader.next()
	#print titles
	for row in reader:
		#print row
		typo = row[3]
		hist = row[6]
		for i in range(9,29):
			if row[i] == 'FAUX':
				continue
			postal = '750%02d' % (i-8)
			address = typo + ' ' + postal + ' Paris'
			print "%s" % address,
			coord = geocode_json(address)
			time.sleep(2)
			if not coord:
				print " -> skipped"
				continue #ignore the line
			lat = coord[0]
			lon = coord[1]
			#print typo, hist, lat, lon
			#break
			# titre / desc / adresse / lat / long / categorie
			writer.writerow([address, hist, address, lat, lon, "rue"])
			print " -> done"

def update_csv2(filename='MH-Ile-de-France.txt-fr_utf8.csv'):
	reader = csv.reader(open(filename, 'rb'), delimiter='\t')
	writer = csv.writer(open(filename[:-4] + '_new.csv', 'wb'), delimiter='\t')

	titles = reader.next()
	#print titles
	for row in reader:
		#print row
		monument = row[7]
		address_ = row[8]
		commune = row[5]
		if True:
			address = monument + " " + address_ + " " + commune
			print "%s" % address,
			coord = geocode_json(address)
			time.sleep(2)
			if not coord:
				print " -> skipped"
				continue #ignore the line
			lat = coord[0]
			lon = coord[1]
			# titre / desc / adresse / lat / long / categorie
			writer.writerow([monument, row[11] + '. ' + row[12] + '. ' + row[13], address, lat, lon, "monument"])
			print " -> done"

def update_csv3(filename='Arbres_remarquables_utf8.csv'):
	reader = csv.reader(open(filename, 'rb'), delimiter=';')
	writer = csv.writer(open(filename[:-4] + '_new.csv', 'wb'), delimiter='\t')

	titles = reader.next()
	#print titles
	for row in reader:
		#print row
		arron = row[0]
		address_ = row[7]
		if True:
			postal = '750%02d' % int(arron)
			address = address_ + " " + arron + " Paris"
			print "%s" % address,
			coord = geocode_json(address)
			time.sleep(2)
			if not coord:
				print " -> skipped"
				continue #ignore the line
			lat = coord[0]
			lon = coord[1]
			# titre / desc / adresse / lat / long / categorie
			writer.writerow([row[8], "Genre : " + row[1] + '. Espece : ' + row[2] + '. Famille : ' + row[3] + ". Annee : " + row[4] + ". Hauteur : " + row[5] + ". Circonference : " + row[6], address, lat, lon, "arbre"])
			print " -> done"

def update_csv4(filename='Coordonnees musees de France_data.gouv_IDF_stripped.csv'):
	reader = csv.reader(open(filename, 'rb'), delimiter=';')
	writer = csv.writer(open(filename[:-4] + '_new.csv', 'wb'), delimiter='\t')

	titles = reader.next()
	#print titles
	for row in reader:
		print row
		address_ = row[5]
		postal = row[6]
		ville = row[7]
		ferme_ = row[2]
		ferme = ""
		if ferme_ == "OUI":
			ferme = "Ferme actuellement. "

		if True:
			address = address_ + " " + postal + " " + ville
			print "%s" % address,
			coord = geocode_json(address)
			time.sleep(2)
			if not coord:
				print " -> skipped"
				continue #ignore the line
			lat = coord[0]
			lon = coord[1]
			# titre / desc / adresse / lat / long / categorie
			writer.writerow([row[4], row[10] + ". Fermeture annuelle : " + row[9] + ". " + ferme + row[8], address, lat, lon, "musees"])
			print " -> done"

if __name__ == '__main__':
	#update_csv()
	#update_csv2()
	#update_csv3()
	update_csv4()
	#coordonnees = geocode_json("Place de l'Universite 1, 1348 Louvain-la-Neuve")
	#print coordonnees
