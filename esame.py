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
            
                #se manca qualche dato relativo al numero di passeggeri per qualche mese faccio in modo da considerare 0
                if elements[1] == '':
                    elements[1] = elements[1].replace('', '0')
                        
                 
                #converto la stringa corrispondente al numero di passeggeri in floating point(numero intero) e la associo al suo valore
                elements[1] = int(elements[1])
                passengers = elements[1] 

                #verifico se la serie è ordinata in senso crescente con le variabili d'appoggio prima inizializzate
                if int(data_split[0]) > last_year:
                    last_month = 0

                if not (int(data_split[0]) >= last_year and int(data_split[1]) > last_month):
                    raise ExamException('Errore nella data: mese o anno non consecutivo.')                    

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

        
    #inizializzo una lista per salvare tutti gli anni presenti nel file
    tot_years = []
    #ricavo dalle liste di time_series i vari anni presenti e di conseguenza presenti all'interno del file
    for list in time_series:
        tot_years.append(list[0][0:4])
    #print(tot_years) 
        
    #pongo che se il primo e l'ultimo anno non appartengono alla lista degli anni viene alzata un'eccezione
    if ((first_year not in tot_years) and (last_year not in tot_years)):
        raise ExamException('Errore: first_year e last_year non appartengono ai dati del file inserito.')
    
    #se uno dei due esiste controllo più nello specifico anche first_year e last_year singolarmente
    elif (first_year not in tot_years):
        raise ExamException('Errore: first_year non appartiene ai dati del file inserito.')
    elif (last_year not in tot_years):
        raise ExamException('Errore: last_year non appartiene ai dati del file inserito.')

   
    #provo a convertire first_year e last_year in valore numerico intero
    try:
        first_year = int(first_year)
        last_year = int(last_year)
    #se non è possibile alzo un'eccezione    
    except ValueError as e:
        raise ExamException(e)

    #controllo che gli anni inseriti in input non siano lo stesso
    if first_year == last_year:
        raise ExamException('Errore: first_year e last_year corrispondono allo stesso anno.')
        
    #controllo se gli anni sono in ordine crescente
    if (last_year < first_year):
        raise ExamException('Errore: le date non sono in ordine crescente.')

        
    #creo una nuova lista per salvare gli anni da prendere in considerazione
    years_list = []
        
    #per facilitare le cose assegno la variabile f al primo anno dell'intervallo preso in considerazione
    f = first_year
    
    #aggiungo alla lista gli anni considerati
    while f <= last_year:
        years_list.append(f)
        f = f + 1
    #opzionale se voglio vedere la lista stampata: 
    #print('Lista anni: {}'.format(years_list))

    #inzializzo una lista per salvare i valori di tutti i mesi divisi per anni
    passengers_number = []
    for year in years_list:

        specific_year = []
        
        for list in time_series:
            #isolo i primi quattro caratteri di ciascuna lista, ovvero l'anno
            if list[0][0:4] == str(year):
                specific_year.append(list[1])

        passengers_number.append(specific_year)
                
    #print(passengers_number)       
                

    #inizializzo la lista dove salvare i valori dell'incremento medio richiesti
    #questa è la lista che, dopo essere stata modificata, verrà ritornata dalla funzione
    result = []

    #prendo in considerazione un range di 12 posizioni che corrispondono ai 12 mesi (0=gennaio, 1=febbraio, ..., 11=dicembre)    
    for i in range(0, 12):
        #scrivo 12 perché l'estremo superiore viene considerato escluso 
        
        #inizializzo una variabile per salvare la variazione di ogni mese
        v_month = 0

        
        #assegno la lunghezza della lista precedente ad una variabile d'appoggio
        m = len(passengers_number)
        
        #inizializzo una variabile che mi salva la differenza dei vari mesi
        differenza = [0]*12

        #calcolo la differenza del numero di passeggeri per ciascun mese dei vari anni considerati
        for item in range(1, m):           
            differenza[i] += passengers_number[item][i] - passengers_number[item-1][i]
           

        #faccio la media, dividendo la differenza ottenuta precedentemente per la lunghezza della lista - 1
        v_month = differenza[i]/(m-1)

        #salvo il risultato sulla lista
        result.append(v_month)

    
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
