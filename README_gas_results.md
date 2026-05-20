# gas_results — descrizione dei file CSV

## Panoramica del flusso dati

I file CSV sono il prodotto finale di una pipeline a due script:

```
SaveReference.m          →   Reference.mat
GasAnalyzer.m  +  GasResistance.mat   →   gas_results/corr_<variabile>.csv
```

---

## Dati di ingresso

### Stazione di riferimento (`SaveReference.m`)

Il riferimento proviene da un file CSV dello strumento AQM65 con campionamento originale a 1 minuto. Le variabili acquisite sono:

| Variabile | Unità | Descrizione |
|---|---|---|
| `COppm` | ppm | Monossido di carbonio |
| `CO2ppm` | ppm | Biossido di carbonio |
| `NOxppm` | ppm | Ossidi di azoto |
| `O3ppm` | ppm | Ozono |
| `SO2ppm` | ppm | Biossido di zolfo |
| `ITEMPC` | °C | Temperatura interna strumento |
| `TEMPC` | °C | Temperatura ambiente |
| `RH` | % | Umidità relativa |

Prima di essere salvato in `Reference.mat`, il dataset viene:

1. **filtrato** sulla finestra temporale `t_start`–`t_end` definita nello script;
2. **ricampionato** a passo regolare di **30 minuti** tramite `retime(..., 'mean')` — ogni valore rappresenta la media aritmetica dei campioni al minuto caduti nella finestra corrispondente;
3. convertito da `UTC+01:00` a **UTC**.

### Sensori BME (`GasResistance.mat`)

Struttura MATLAB a due livelli: `GasResistance.<gas_index>.<sensore>`, dove ogni foglia è una timetable con colonna `Value` (resistenza in Ω).

---

## File CSV prodotti (`GasAnalyzer.m`)

La cartella `gas_results/` viene generata quando il flag `save_csv = true`. Contiene **un file per ogni variabile numerica del riferimento**:

```
gas_results/
  corr_COppm.csv
  corr_CO2ppm.csv
  corr_NOxppm.csv
  corr_O3ppm.csv
  corr_SO2ppm.csv
  corr_ITEMPC.csv
  corr_TEMPC.csv
  corr_RH.csv
```

### Struttura di ogni CSV

Ogni file è una matrice di **coefficienti di correlazione di Pearson** tra le serie di resistenza dei sensori BME e la variabile di riferimento indicata nel nome del file.

| Dimensione | Contenuto |
|---|---|
| **Righe** | Sensori BME (es. `es3-1-0`, `es3-1-1`, …) |
| **Colonne** | Gas index (es. `gas-index 0`, `gas-index 1`, …) |
| **Valori** | Coefficiente di Pearson *r* ∈ [−1, 1] |

Esempio (layout schematico):

```
Row,gas_index_0,gas_index_1,...
es3-1-0,  0.87,  0.34,...
es3-1-1, -0.12,  0.91,...
...
```

---

## Come viene calcolato ogni coefficiente

1. La serie del sensore e quella del riferimento vengono **sincronizzate per unione** temporale — nessuna interpolazione nearest-neighbour, i gap restano `NaN`.
2. I campioni con `NaN` in almeno una delle due sorgenti vengono **esclusi**.
3. Il coefficiente di Pearson viene calcolato solo se rimangono **almeno 3 punti validi** e se entrambe le serie hanno **varianza non nulla**; altrimenti la cella contiene `NaN`.

---

## Note

- Un valore `NaN` in una cella indica che la correlazione non era calcolabile per quella coppia sensore/gas-index (dati insufficienti o serie costante).
- I timestamp del riferimento sono corretti di +1 ora (UTC → UTC+1) all'interno di `GasAnalyzer.m` prima della sincronizzazione.
- La finestra di mediazione del riferimento (default 30 min) è configurabile tramite il parametro `Wmean_ref` in `SaveReference.m`.
- Ogni matrice è salvata anche nel workspace MATLAB come variabile `corr_<nome_variabile>`.
