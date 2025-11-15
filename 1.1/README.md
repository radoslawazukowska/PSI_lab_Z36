## Zadanie 1.1
Klient wysyła, a serwer odbiera datagramy oraz odsyła ustaloną odpowiedź. Klient powinien wysyłać kolejne datagramy o przyrastającej wielkości, tj. 2, 4, 8, 16, 32, itd. bajtów. Ustalić eskperymentalnie z dokładnością do jednego bajta jak duży datagram jest obsługiwany. Wyjaśnić. Zmierzyć czas pomiędzy wysłaniem wiadomości a odebraniem odpowiedzi po stronie klienta i zestawić wyniki na wykresie.

## Uruchamianie
1. Log into bigubu `ssh <yourname>@bigubu.ii.pw.edu.pl`
2. Clone the repository `git clone https://github.com/radoslawazukowska/PSI_lab_Z36.git`
3. Go to directory of this task `cd PSI_lab_Z36/1.1`
4. Run the server
5. Run the client
`cd Client`
`docker build -t pclient1 .`
`docker run -it --network z36_network pclient1 cserver1 8001`