## Zadanie 1.1
Klient wysyła, a serwer odbiera datagramy oraz odsyła ustaloną odpowiedź. Klient powinien wysyłać kolejne datagramy o przyrastającej wielkości, tj. 2, 4, 8, 16, 32, itd. bajtów. Ustalić eskperymentalnie z dokładnością do jednego bajta jak duży datagram jest obsługiwany. Wyjaśnić. Zmierzyć czas pomiędzy wysłaniem wiadomości a odebraniem odpowiedzi po stronie klienta i zestawić wyniki na wykresie.

## Uruchamianie
1. Zaloguj się do bigubu \
`ssh <yourname>@bigubu.ii.pw.edu.pl`
2. Pobierz repozytorium \
`git clone https://github.com/radoslawazukowska/PSI_lab_Z36.git`
3. Przejdź do folder tego zadania \
`cd PSI_lab_Z36/1.1`
4. Uruchom server \
`cd Server` \
`docker build -t server1_docker .` \
`docker run -it --network z36_network --network-alias cserver1 --name cserver1 server1_docker:latest`
5. Na osobnym terminalu uruchom klienta \
`cd Client` \
`docker build -t pclient1 .` \
`docker run -it --network z36_network --name pclient1 pclient1 cserver1 54070`
6. Jeśli chcesz ponownie uruchomić program z punktu 4 i 5, najpierw usuń odpowiednie kontenery Dockerowe \
`docker container rm cserver1` \
`docker container rm pclient1`

### Ewentualne problemy
1. Na bigubu tego nie ma, ale lokalnie upewnij się że masz uruchomiony Docker, inaczej polecenia nie zadziałają.
2. Serwer można opuścić sekwencją klawiszy Ctrl-p/Ctrl-q, jednak przed usunięciem jego potrzebne jest zatrzymanie używając następującego polecenia: `docker stop cserver1`.