import socket
import threading
import mysql.connector
from mysql.connector import FieldType as Ft
import facilities as F

def leggi_tabella(cr,listac,nt,j):
    query = f"SELECT * FROM {nt}"
    cr.execute(query)
    dati = cr.fetchall()
    F.send_a_list(dati,listac,j)

def controllo_tipo(column,cur,field_names,incr):
    field_types = [i[1] for i in cur.description]
    print(field_types)
    print(field_names)
    for i in range(0,len(field_names)):
        if field_names[i] == column:
            result = Ft.get_info(field_types[i+incr])
            if result=='VAR_STRING':
                return('1')
            elif result =='LONG':
                return('2')
            elif result =='DATE':
                return('3')
            elif result =='FLOAT':
                return('4')
            else:
                print('Errore')


def crea_condizione(lista_conn,cur,j,nt):
    query = f"SELECT * FROM {nt}"
    cur.execute(query)
    dati = cur.fetchall()
    field_names = [i[0] for i in cur.description]
    F.send_a_list(field_names,lista_conn,j)

    lista_conn[j][0].send("inserisci la colonna su cui applicare la condizione: ".encode())
    scelta_cl=lista_conn[j][0].recv(1024).decode()
    
    tipo=controllo_tipo(scelta_cl,cur,field_names,0)

    if tipo=="1":
        lista_conn[j][0].send("inserisci la stringa con cui confrontare il contenuto della colonna scelta: ".encode())
        scelta_val=lista_conn[j][0].recv(1024).decode()
        condizione = f"{scelta_cl} = '{scelta_val}'"
    else:
        lista_conn[j][0].send("inserisci il valore con cui confontare quello della colonna scelta: ".encode())
        scelta_val=lista_conn[j][0].recv(1024).decode()
        scelta_op = -1
        while scelta_op<1 or scelta_op>5:
            lista_conn[j][0].send("come deve essere il valore della colonna rispetto al valore imposto nella condizione (1: maggiore,2: minore,3: uguale,4: maggiore o uguale,5: minore o uguale)".encode())
            scelta_op=int(lista_conn[j][0].recv(1024).decode())
        if scelta_op==1:
            condizione = f"{scelta_cl}>{scelta_val}"
        elif scelta_op==2:
            condizione = f"{scelta_cl}<{scelta_val}"
        elif scelta_op==3:
            condizione = f"{scelta_cl}={scelta_val}"
        elif scelta_op==4:
            condizione = f"{scelta_cl}>={scelta_val}"
        else:
            condizione = f"{scelta_cl}<={scelta_val}"
        
    return condizione
    
    


'''
================FUNZIONI QUERY===========================
'''

def update_query(tab,nt,listac,cur,cn,j):
    leggi_tabella(cur,listac,nt,j)
    listac[j][0].send("inserisci l'id dell'istanza da modificare: ".encode())
    id_mod=listac[j][0].recv(1024).decode()
    cur.execute(f"SELECT * FROM {nt}")
    cur.fetchall()
    field_names = [i[0] for i in cur.description]
    F.send_a_list(field_names,listac,j)
    listac[j][0].send("inserisci il nome del campo da modificare: ".encode())
    campo_mod=listac[j][0].recv(1024).decode()
    listac[j][0].send("inserisci la modifica da effettuare al campo inserito: ".encode())
    mod=listac[j][0].recv(1024).decode()
    if tab==1:
        query=f"UPDATE {nt} SET {campo_mod}={mod}  WHERE id_zona={id_mod}"
    else:
        query=f"UPDATE {nt} SET {campo_mod}={mod}  WHERE id={id_mod}"
    
    lock.acquire()
    cur.execute(query)
    cn.commit()
    leggi_tabella(cur,listac,nt,j)
    lock.release()

def delete_query(tab,nt,listac,cur,cn,j):
    leggi_tabella(cur,listac,nt,j)
    listac[j][0].send("inserisci il codice dell'istanza da eliminare: ".encode())
    id_del = listac[j][0].recv(1024).decode()
    if tab==1:
        query = f"DELETE FROM dipendenti_filippo_sacchetti WHERE id_zona={id_del}"
    else:
        query = f"DELETE FROM dipendenti_filippo_sacchetti WHERE id={id_del}"
    cur.execute(query)
    cn.commit()
    leggi_tabella(cur,listac,nt,j)

def create_query(tab,nt,listac,cur,cn,j):
    if tab==1:
        listac[j][0].send("inserisci il nome della zona di lavoro: ".encode())
        nz=listac[j][0].recv(1024).decode()
        listac[j][0].send("inserisci il numero di clienti della zona di lavoro: ".encode())
        nc=listac[j][0].recv(1024).decode()
        listac[j][0].send("inserisci il codice del dipendente che gestisce la zona di lavoro: ".encode())
        id_dip=listac[j][0].recv(1024).decode()
        query = "INSERT INTO zone_di_lavoro(nome_zona,numero_clienti,id_dipendente) VALUES (%s,%s,%s)"
        values = (nz,nc,id_dip)
    else:
        listac[j][0].send("inserisci il nome dell'impiegato': ".encode())
        nd=listac[j][0].recv(1024).decode()
        listac[j][0].send("inserisci l'indirizzo del dipendente: ".encode())
        ind=listac[j][0].recv(1024).decode()
        listac[j][0].send("inserisci il numero di telefono del dipendente: ".encode())
        tel=listac[j][0].recv(1024).decode()
        listac[j][0].send("inserisci l'agente del dipendente: ".encode())
        ag=listac[j][0].recv(124).decode()
        query = "INSERT INTO zone_di_lavoro(nome,indirizzo,telefono,agente) VALUES (%s,%s,%s,%s)"
        values = (nd,ind,tel,ag)
    lock.acquire()
    cur.execute(query,values)
    cn.commit()
    leggi_tabella(cur,listac,nt,j)
    lock.release()

def read_query(nome_tab,lista_conn,cur,j):
    sc = -1
    while sc<1 or sc>2:
        lista_conn[j][0].send("Cosa vuoi visualizzare? (1: visualizza tutta la tabella ; 2: applica condizioni)".encode())
        sc = int(lista_conn[j][0].recv(1024).decode())
            
    if sc==1:
        leggi_tabella(cur,lista_conn,nome_tab,j)
    else:
        cond = crea_condizione(lista_conn,cur,j,nome_tab)
        '''
        lista_conn[j][0].send("vuoi applicare un'altra condizione? (1: si,2: no  )".encode())
        scelta_cond = lista_conn[j][0].recv(1024).decode()
        if scelta_cond==1:
            cond2 = crea_condizione(lista_conn,cur,j,nome_tab)
            lista_conn[j][0].send("scegli la porta logica da utilizzare: (1: AND,2: OR)".encode())        #ho provato a fare in modo che si potesse applicare una seconda condizione,
            porta_logica = lista_conn[j][0].recv(1024).decode()                                            ma ho riscontrato problemi che non sono riuscito a risolvere
            if porta_logica==1:
                query=f"SELECT * FROM {nome_tab} WHERE {cond} AND {cond2}"
            else:
                query=f"SELECT * FROM {nome_tab} WHERE {cond} OR {cond2}"   
        elif scelta_cond==2:
            query=f"SELECT * FROM {nome_tab} WHERE {cond}"
            cur.execute(query)
            dati=cur.fetchall()
            F.send_a_list(dati,lista_conn,j)
        '''
        query=f"SELECT * FROM {nome_tab} WHERE {cond}"
        cur.execute(query)
        dati=cur.fetchall()
        F.send_a_list(dati,lista_conn,j)


'''
==========================FUNZIONE PRINCIPALE MENU================================0
'''

def db_get(lista_conn,lock,j):
    cn = mysql.connector.connect(
        host="127.0.0.1", 
        user="root",
        password="",
        database="azienda",
        port=3306, 
        )


    cur = cn.cursor()

    
    tab=-1
    while tab<1 or tab>2: 
        lista_conn[j][0].send("su quale tabella vuoi agire? (1: zone_di_lavoro , 2: dipendenti_filippo_sacchetti)".encode())
        tab=int(lista_conn[j][0].recv(1024).decode())


    if tab==2:
        nome_tab="dipendenti_filippo_sacchetti"
        lista_conn[j][0].send("Cosa vuoi fare? (C: creare/L: leggere/M: modificare/E: eliminare)".encode())
        scelta = lista_conn[j][0].recv(1024).decode()
        
        if scelta=='L':
            read_query(nome_tab,lista_conn,cur,j)
        elif scelta=='C':
            create_query(tab,nome_tab,lista_conn,cur,cn,j)
        elif scelta=='E':
            delete_query(tab,nome_tab,lista_conn,cur,cn,j)
        elif scelta=='M':
            update_query(tab,nome_tab,lista_conn,cur,cn,j)


    elif tab==1:
        nome_tab="zone_di_lavoro"
        lista_conn[j][0].send("Cosa vuoi fare? (C: creare/L: leggere/M: modificare/E: eliminare)".encode())
        scelta = lista_conn[j][0].recv(1024).decode()
        
        if scelta=='L':
            read_query(nome_tab,lista_conn,cur,j)
        elif scelta=='C':
            create_query(tab,nome_tab,lista_conn,cur,cn,j)
        elif scelta=='E':
            delete_query(tab,nome_tab,lista_conn,cur,cn,j)
        elif scelta=='M':
            update_query(tab,nome_tab,lista_conn,cur,cn,j)

           
#==============================MAIN========================================


PASSWORD = "password"
HOST = 'localhost'                 
PORT = 50007             
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)
lista_conn = []
thread = []
lock = threading.Lock()

print("server avviato, in ascolto...")

i = 0
j = 0
ins = ""

while True:
    lista_conn.append(s.accept())
    print('Connected by', lista_conn[j][1])
    while(i<3 and ins != PASSWORD):
        dati = "inserisci password, " + str(3-i) + "tentativi rimasti"
        lista_conn[j][0].send(dati.encode())
        i+=1
        ins = lista_conn[j][0].recv(1024).decode()
    i=0
    scelta=""

    if(ins == PASSWORD):
        lista_conn[j][0].send("password corretta, iniza la comunicazione. premi enter per continuare".encode())
        ins = ""
        thread.append(threading.Thread(target=db_get,args=(lista_conn,lock,j)))
        thread[j].start()
    else:
        lista_conn[j][0].send("tentativi massimi raggiunti. Chiudo la connessione".encode())
        lista_conn[j][0].close()

    j=j+1

