#definisco la classe per le eccezioni
class ExamException(Exception):
    pass

#definisco la classe
class CSVTimeSeriesFile():

    def __init__(self, name):
       
        #setto il nome del file
        self.name = name
        

    def get_data(self):
        
        #alzo un'eccezione per assicurarmi che il file esista provando a leggere la prima riga del file
        try:
            time_series_file = open(self.name, 'r')
            time_series_file.readline()
        except:
            raise ExamException('Errore in apertura file')
            

        #creo una lista su cui salverò tutte le liste
        time_series = []
            
        #apro il file
        time_series_file = open(self.name, 'r')

        #faccio un controllo per assicurarmi la serie sia ordina in senso crescente
        #inizializzo due variabili per farlo
        last_year = 0
        last_month = 0

        #leggo il file linea per linea
        for line in time_series_file:
                
            #faccio lo split ad ogni linea del file 
            #ogni riga la divido in due stringhe (della stessa lista), la prima corrisponde alla data e la seconda al numero di passeggeri
            elements = line.split(',')

            #pulisco dal carattere newline ed eventuali spazi ad inizio o a fine stringa con la funzione strip
            elements[-1] = elements[-1].strip()

            #se non sto processando l'intestazione...
            if elements[0] != 'date':
                #...associo gli elementi
                date = elements[0]

                #faccio lo split della data
                data_split = elements[0].split('-')


                #provo a convertire il numero di passeggeri ad intero, se non è possibile non viene accettato, ma passa avanti
                try:
                    elements[1] = int(elements[1])
                except ValueError:
                    continue

                #stessa cosa di prima se il valore è negativo, passo avanti
                if elements[1] < 0:
                    continue
                 
                #converto la stringa corrispondente al numero di passeggeri in floating point(numero intero) e la associo al suo valore
                elements[1] = int(elements[1])
                passengers = elements[1] 

                #verifico se la serie è ordinata in senso crescente con le variabili d'appoggio prima inizializzate
                if int(data_split[0]) > last_year:
                    last_month = 0

                if not (int(data_split[0]) >= last_year and int(data_split[1]) > last_month):
                    print('Errore nella data: mese o anno non consecutivo.')
                    return None

                #setto le variabili usate
                last_year = int(data_split[0])
                last_month = int(data_split[1])    

                #aggiungo alla lista gli elementi della linea
                time_series.append(elements)
   

        #chiudo il file
        time_series_file.close()

        #ritorno la lista dopo aver considerato tutte le righe
        return time_series
                

#creo una funzione per poter calcolare la differenza media del numero di passeggeri mensile tra anni consecutivi
def compute_avg_monthly_difference(time_series, first_year, last_year):
    #first_year e last_year le inserisco manuelmente nel corpo del programma e corrispondono al primo e all'ultimo anno dell'intervallo preso in considerazione

    #controllo che first_year e last_year siano inseriti in input come stringhe
    if not isinstance(first_year, str):
        raise ExamException('Errore: first_year deve essere una stringa e non "{}".'.format(type(first_year)))
    if not isinstance(last_year, str):
        raise ExamException('Errore: last_year deve essere una stringa e non "{}".'.format(type(last_year)))


    
    #provo a convertire first_year e last_year in valore numerico intero
    try:
        first_year = int(first_year)
        last_year = int(last_year)
    #se non è possibile alzo un'eccezione    
    except ValueError as e:
        raise ExamException('"{}"'.format(e))
    
    #creo una nuova lista per salvare gli anni da prendere in considerazione
    years_list = []
        
    #per facilitare le cose assegno la variabile f al primo anno dell'intervallo preso in considerazione
    f = int(first_year)
    
    #aggiungo alla lista gli anni considerati
    while f <= int(last_year):
        years_list.append(f)
        f = f + 1
    #opzionale se voglio vedere la lista stampata: 
    #print('Lista anni: {}'.format(years_list))


    #inizializzo una lista per salvare i dati in numero intero
    data_int = []

    #provo a leggere la prima riga per vedere se si apre
    try:
        time_series_file = open('data.csv', 'r')
        time_series_file.readline()
    #alzo un'eccezione nel caso non si apra    
    except:
        raise ExamException('Errore in apertura file')
    
        #apro il file
    time_series_file = open('data.csv', 'r')

    for line in time_series_file:
        #faccio lo split ad ogni linea del file 
        #ogni riga la divido in due stringhe (della stessa lista), la prima corrisponde alla data e la seconda al numero di passeggeri
        elements = line.split(',')

        #pulisco il carattere newline ed eventuali spazi ad inizio o a fine stringa con la funzione strip
        elements[-1] = elements[-1].strip()

        #se non sto processando l'intestazione...
        if elements[0] != 'date':

            #creo una lista vuota per salvare i valori interi corrispondenti rispettivamente ad: anno, mese, numero passeggeri
            list_int = []
            
            #associo gli elementi della prima stringa alla data
            date = elements[0]
            #divido la stringa in due: anno e mese
            date = date.split('-')

            
            #associo la prima stringa di 'date' all'anno e la seconda al mese, convertendole in valore numerico
            year = int(date[0])
            month = int(date[1])

            #aggiungo alla lista i valori della data
            list_int.append(year)
            list_int.append(month)

                
            #associo la seconda stringa al numero di passeggeri ed aggiungo alla lista il valore convertendolo in numero intero
            passengers = int(elements[1])
            list_int.append(passengers)

            
            #se manca qualche dato relativo al numero di passeggeri per qualche mese faccio in modo da considerare 0
            if passengers == '':
                passengers = passengers.replace('', '0')
                        
               
            #aggiungo tutte le liste di valori interi create alla lista
            data_int.append(list_int)
      
    #se voglio visualizzare tutte le liste in valore intero:
    #for item in data_int:
        #print(item)

    #inizializzo una lista dove salvare i valori numerici corrispondenti agli anni
    years = []
    #aggiungo alla lista gli anni 
    for item in data_int:
        years.append(item[0])


    #pongo che se il primo e l'ultimo anno non appartengono alla lista degli anni viene alzata un'eccezione
    if ((first_year not in years) and (last_year not in years)):
            raise ExamException('Errore: first_year e last_year non appartengono ai dati del file inserito.')
    
    #se uno dei due esiste controllo più nello specifico anche first_year e last_year singolarmente
    elif (first_year not in years):
            raise ExamException('Errore: first_year non appartiene ai dati del file inserito.')
    elif (last_year not in years):
            raise ExamException('Errore: last_year non appartiene ai dati del file inserito.')

    #controllo che gli anni inseriti in input non siano lo stesso
    if first_year == last_year:
        raise ExamException('Errore: first_year e last_year corrispondono allo stesso anno.')
        
    #controllo se gli anni sono in ordine crescente
    for item in years:
        if (last_year < first_year):
            raise ExamException('Errore: le date non sono in ordine crescente.')
        
        

    #inizializzo la lista dove salvare i valori dell'incremento medio richiesti
    #questa è la lista che, dopo essere stata modificata, verrà ritornata dalla funzione
    result = []

    #prendo in considerazione un range di 12 posizioni che corrispondono ai 12 mesi (1=gennaio, 2=febbraio, ..., 12=dicembre)    
    for i in range(1, 13):
        #scrivo 13 perché l'estremo superiore viene considerato escluso 
        
        #inizializzo una variabile per salvare la variazione di ogni mese
        v_month = 0

        #inizializzo una lista di liste corrispondenti al numero di passeggeri di mese dei vari anni presi in condiderazione
        #esempio: prima lista = numero di passeggeri del mese di gennaio per ogni anno dell'intervallo considerato
        values = []

        #aggiungo alla lista appena inizializzata il numero di passeggeri divisi per mese di ogni anno dell'intervallo considerato
        for item in data_int:
            if (item[1] == i) and item[0] in years_list:
                values.append(item[2])

        
        #assegno la lunghezza della lista precedente ad una variabile d'appoggio
        m = len(values)
        
        #inizializzo una variabile che mi salva la differenza dei vari mesi
        differenza = 0

        #calcolo la differenza del numero di passeggeri per ciascun mese dei vari anni considerati
        while m > 1:
            differenza += values[m - 1] - values [m - 2]
            m = m - 1

        #faccio la media, dividendo la differenza ottenuta precedentemente per la lunghezza della lista - 1
        v_month = differenza/(len(values)-1)

        #salvo il risultato sulla lista
        result.append(v_month)

        #procedo e calcolo l'incremento medio per tutti i 12 mesi
        i += 1
    
    #ritorno il risultato
    return result
                

#====================    
#CORPO DEL PROGRAMMA:
#====================    
    
#assegno la classe al file
time_series_file = CSVTimeSeriesFile(name = 'data.csv')

#assegno il file alla lista
time_series = time_series_file.get_data()
#time_series = CSVTimeSeriesFile.get_data(time_series_file)

#opzionale, se voglio stampare l'indirizzo in memeoria dell'oggetto creato: print(time_series_file)

#stampo il nome del file, dato dalla funzione __init__
#print('Nome del file: "{}"'.format(time_series_file.name))

#se voglio visualizzarli, stampo il contenuto del file, dato dalla funzione get_data
#print('Dati contenuti nel file: "{}"'.format(time_series))

result = compute_avg_monthly_difference(time_series, "1949", "1951") 
print('La variazione media del numero di passeggeri per ogni mese è: {}'.format(result))
