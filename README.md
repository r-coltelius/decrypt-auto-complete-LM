#Inledning
Att dekryptera monoalfabetiska substitutionschiffer är inte särskilt svårt men det kräver att man har bra träningsdata (korpus). 
I detta projekt dekrypteras monoalfabetiska substitutionschiffer med hill climbing och simulated annealing genom att att utvärdera 
hur "engelsk" den dekrypterade texten är. Med engelsk menas hur frekvent varje n-gram av bokstavsföljder i den dekrypterade texten är i ens korpus. 
En scorefunktion S(T) bildas för texten T där max{S(T)} sökes efter i iterationer. Vid varje iteration görs ett godtyckligt byte av två 
bokstäver. Därefter utvärderas S(T). Om S(T) ökar görs bytet. Annars görs bytet med en sannolikhet. Se `hill_climbing()`. 

Att generera text, alltså att bygga auto complete, är också relativt lätt såvida en har en stor och varierad korpus. I detta projekt
genereras text genom att beräkna sannolikheten givet k föregående, vad nästkommande ord bör vara. Detta görs genom att skapa nyckel-värde-tabeller
av respektive n-gram av ordföljder. Observera att antalet engelska ord är betydligt fler än antalet engelska bokstäver (26). Därför begränsas nyckel-
värde-tabellerna till 50000 par. 

#Kod
I koden kan en välja mellan att dekryptera eller generera text där `mode = 0` i `main()` anger dekryptering, `mode = 1` anger textgenerering. 
`mode2 = 2` anger att generera text utifrån två föregående ord och `mode2 = 3` anger att generera text utifrån tre föregående ord. 
Observera att filer är korpus är ej uppladdade på grund av dess storlek. Användaren rekommenderas dock att delvis använda korpus från 
Natural Language Toolkit (NLTK). Vänligen se `download_nltk()` i klassen `Main` samt dokumentationen för NLTK. Texter att dekryptera kan 
vara godtyckliga men för variation och enkelhet rekommenderas använda texter från korpuset Reuters som finns tillgängligt i NLTK. I `main()`
anges texten som ska dekrypteras till `text` med `text = rts.raw('test/xxxxx')`. För vidare information hänvisas läsaren till dokumentation för NLTK. 
För att dekryptera monoalfabetiska substitutionschiffer med 1-gram väljs ´n=1´ som parameter i `score_function()` i `decrypt.py`. För att välja parametrar 
`iterations`, `T0`, `a` och `restarts` till hill climbing görs det i `hill_climbing()`. 
