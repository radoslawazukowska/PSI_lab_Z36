## Zadanie 1.1

Klient wysyła, a serwer odbiera datagramy oraz odsyła ustaloną odpowiedź. Klient powinien wysyłać kolejne datagramy o przyrastającej wielkości, tj. 2, 4, 8, 16, 32, itd. bajtów. Ustalić eskperymentalnie z dokładnością do jednego bajta jak duży datagram jest obsługiwany. Wyjaśnić. Zmierzyć czas pomiędzy wysłaniem wiadomości a odebraniem odpowiedzi po stronie klienta i zestawić wyniki na wykresie.

# Ważne

z36
create --name z43_serwer_app1 --network z43_network

Sprawdzić czy kontenr jeszcze jest
`docker ps -a --filter name='z36_'`

## Uruchamianie

1. Zaloguj się do bigubu \
   `ssh <yourname>@bigubu.ii.pw.edu.pl`
2. Pobierz repozytorium \
   `git clone https://github.com/radoslawazukowska/PSI_lab_Z36.git`
3. Przejdź do folder tego zadania \
   `cd PSI_lab_Z36/1.1`
4. Uruchom skrypt run.sh \
   `sh run.sh`

### Opis, co robi skrypt lub instrukcja ręcznego uruchomienia:

1. Uruchom server \
   `cd Server` \
   `docker build -t z36_server1_docker .` \
   `docker run -it --network z36_network --network-alias z36_cserver1 --name z36_cserver1 z36_server1_docker:latest`
2. Na osobnym terminalu uruchom klienta \
   `cd Client` \
   `docker build -t z36_pclient1 .` \
   `docker run -it --network z36_network --name z36_pclient1 z36_pclient1 z36_cserver1 54070`
3. Jeśli chcesz ponownie uruchomić program z punktu 4 i 5, najpierw usuń odpowiednie kontenery Dockerowe \
   `docker container rm z36_cserver1` \
   `docker container rm z36_pclient1`

### Ewentualne problemy

1. Na bigubu tego nie ma, ale lokalnie upewnij się że masz uruchomiony Docker, inaczej polecenia nie zadziałają.
2. Serwer można opuścić sekwencją klawiszy Ctrl-p/Ctrl-q, jednak przed usunięciem jego potrzebne jest zatrzymanie używając następującego polecenia: `docker stop z36_cserver1`.
