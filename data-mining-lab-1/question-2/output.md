QUESTION 2 — SETUBID DEDUPLICATION
 Section A
 A(a) Initial labelled-pair inspection

PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> Get-Content .\labelled_pairs.csv -TotalCount 10
notice_id_a,notice_id_b,label,adjudicated_by,adjudicated_on
N010018,N010020,same,ops6,2025-03-28
N007876,N008565,different,ops1,2025-04-30
N005451,N005452,same,ops2,2025-03-24
N008464,N010231,different,ops6,2025-08-20
N000420,N001104,different,ops2,2025-08-23
N004781,N005219,different,ops5,2025-06-26
N007021,N010547,different,ops1,2025-07-20
N004413,N008734,different,ops4,2025-04-08
N007783,N007784,same,ops1,2025-03-14

Label distribution

PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> python -c "import pandas as pd; df=pd.read_csv('labelled_pairs.csv'); print('Total labelled pairs:',len(df)); print(); print('Label counts:'); print(df['label'].value_counts()); print(); print('Label percentages:'); print((df['label'].value_counts(normalize=True)*100).round(2))"
Total labelled pairs: 900

Label counts:
label
different    621
same         279
Name: count, dtype: int64

Label percentages:
label
different    69.0
same         31.0
Name: proportion, dtype: float64

 Notice corpus inspection

PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> python -c "import pandas as pd, glob; f=glob.glob('notices/*.csv')[0]; df=pd.read_csv(f); print('File:',f); print('Shape:',df.shape); print(); print('Columns:'); print(df.columns.tolist()); print(); print('First 3 rows:'); print(df.head(3).to_string())"
File: notices\part-000.csv
Shape: (1500, 7)

Columns:
['notice_id', 'portal_id', 'published_at', 'title', 'body', 'estimated_value', 'closing_date']

First 3 rows:
  notice_id portal_id published_at                                                                             title                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               body  estimated_value closing_date
0   N000001      P136   2024-03-03  Procurement and commissioning of CCTV surveillance infrastructure for Dausa city  Name of work: Procurement and commissioning of CCTV surveillance infrastructure for Dausa city.\nTender reference number: ref-2024-85467.\nProcuring entity: Water Resources Department, Dausa district.\nEstimated cost put to tender: Rs. 7,60,00,000/-.\nEarnest money deposit: Rs. 15,20,000/-.\nCost of tender document: Rs. 1,000/-.\nPeriod of completion: 29 months from the date of the work order.\nEligibility: registered contractors of Class AA and above in the appropriate category are eligible to participate.\nMinimum average annual turnover in the last three financial years: Rs. 16,53,83,771/-.\nExperience of at least one similar completed work of value not less than Rs. 3,73,01,337/-.\nBid validity: 120 days from the date of opening.\n\nSCOPE OF WORK\nThe work comprises procurement and commissioning of cctv surveillance infrastructure for dausa city including all associated earthwork, sub-base and base courses, cross drainage structures, protective works, road furniture and incidental items as detailed in the bill of quantities and the approved drawings.\nThe contractor shall execute 430 units of earthwork in excavation in ordinary soil including disposal of surplus spoil in reach 35 between chainage 2+172 and 84+922 of the alignment at Dausa.\nThe contractor shall execute 389 units of providing anti-termite treatment to plinth and foundation in reach 18 between chainage 36+508 and 51+672 of the alignment at Dausa.\nThe contractor shall execute 895 units of construction of rcc hume pipe culvert np3 class in reach 16 between chainage 13+247 and 82+944 of the alignment at Dausa.\nThe contractor shall execute 105 units of bituminous macadam grade ii using vg-30 bitumen in reach 28 between chainage 27+735 and 68+507 of the alignment at Dausa.\n\nABSTRACT BILL OF QUANTITIES\n  Providing rain water harvesting structure with recharge pit -- 55,553 MT at Rs. 8,062 per MT.\n  Wet mix macadam laid in layers with mechanical paver finisher -- 10,261 each at Rs. 2,544 per each.\n  Supplying and fixing HYSD reinforcement bars conforming to IS 1786 -- 25,369 litre at Rs. 5,955 per litre.\n  Construction of RCC overhead service reservoir with staging -- 92,532 quintal at Rs. 2,892 per quintal.\n  Supplying and fixing LED luminaires of 60 W with driver -- 62,502 litre at Rs. 6,806 per litre.\n  Supplying and installing submersible pumpset with control panel -- 33,986 litre at Rs. 248 per litre.\n  Earthwork in excavation in ordinary soil including disposal of surplus spoil -- 43,641 sqm at Rs. 1,055 per sqm.\n  Providing anti-termite treatment to plinth and foundation -- 82,640 rmt at Rs. 2,808 per rmt.\n  Providing and laying M-25 grade cement concrete in foundation -- 8,570 quintal at Rs. 6,164 per quintal.\n  Supplying and fixing vitrified tile flooring 600x600 mm -- 47,234 litre at Rs. 951 per litre.\n  Providing and fixing MS crash barrier of approved section -- 84,524 each at Rs. 6,194 per each.\n\nKEY DATES\nPublication of notice: Mar 01, 2024.\nLast date and time for online submission of bids: Mar 20, 2024 at 17:00 hours.\nDate of opening of technical bids: Mar 21, 2024 at 11:00 hours.\n\nCONTACT\nProject Director Rajeshwari Pillai, Water Resources Department, Dausa. Telephone 02052-367005. Electronic mail pillai.dausa@water.gov.in.\n\nGENERAL CONDITIONS\nThe undersigned reserves the right to accept or reject any or all bids without assigning any reason.\nThe successful bidder shall execute the agreement within fifteen days of issue of the work order.\nConditional bids shall be summarily rejected.         76000000   2024-03-20
1   N000009      P011   2024-06-18                  Desilting and lining of the bus terminal at Osmanabad [00083536]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Name of work: Desilting and lining of the bus terminal at Osmanabad.\nTender reference number: 00083536.\nProcuring entity: Department of School Education, Osmanabad district.\nEstimated cost put to tender: 4530000.\nEarnest money deposit: 91000.\nCost of tender document: 2000.\nPeriod of completion: 8 months from the date of the work order.\nEligibility: registered contractors of Class A and above in the appropriate category are eligible to participate.\nMinimum average annual turnover in the last three financial years: 9287619.\nExperience of at least one similar completed work of value not less than 2923338.\nBid validity: 90 days from the date of opening.\n\nSCOPE OF WORK\nThe work comprises desilting and lining of the bus terminal at osmanabad including all associated earthwork, sub-base and base courses, cross drainage structures, protective works, road furniture and incidental items as detailed in the bill of quantities and the approved drawings.\nThe contractor shall execute 733 units of construction of rcc overhead service reservoir with staging in reach 34 between chainage 24+663 and 65+631 of the alignment at Osmanabad.\nThe contractor shall execute 608 units of plastering with cement mortar 1:4 on internal and external surfaces in reach 15 between chainage 36+019 and 41+062 of the alignment at Osmanabad.\nThe contractor shall execute 61 units of bituminous macadam grade ii using vg-30 bitumen in reach 21 between chainage 3+530 and 78+190 of the alignment at Osmanabad.\n\nABSTRACT B          4530000   2024-07-13
2   N000017      P238   2024-07-28                 Upgradation of CCTV surveillance infrastructure for Fatehpur city                                                                                                                                                         Name of work: Upgradation of CCTV surveillance infrastructure for Fatehpur city.\nTender reference number: URBA/2024/87664.\nProcuring entity: Urban Development Authority, Fatehpur district.\nEstimated cost put to tender: Rs. 39,65,00,000/-.\nEarnest money deposit: Rs. 79,30,000/-.\nCost of tender document: Rs. 1,000/-.\nPeriod of completion: 4 months from the date of the work order.\nEligibility: registered contractors of Class A and above in the appropriate category are eligible to participate.\nMinimum average annual turnover in the last three financial years: Rs. 89,55,02,683/-.\nExperience of at least one similar completed work of value not less than Rs. 31,35,79,922/-.\nBid validity: 150 days from the date of opening.\n\nSCOPE OF WORK\nThe work comprises upgradation of cctv surveillance infrastructure for fatehpur city including all associated earthwork, sub-base and base courses, cross drainage structures, protective works, road furniture and incidental items as detailed in the bill of quantities and the approved drawings.\nThe contractor shall execute 243 units of earthwork in excavation in ordinary soil including disposal of surplus spoil in reach 22 between chainage 34+709 and 64+034 of the alignment at Fatehpur.\nThe contractor shall execute 439 units of providing thermoplastic road marking paint with glass beads in reach 24 between chainage 8+855 and 88+320 of the alignment at Fatehpur.\nThe contractor shall execute 265 units of construction of rcc overhead service reservoir with staging in reach 38 between chainage 1+400 and 65+433 of the alignment at Fatehpur.\nThe contractor shall execute 35 units of supplying and erecting cautionary and informatory road signs in reach 29 between chainage 6+976 and 44+939 of the alignment at Fatehpur.\n\nABSTRACT BILL OF QUANTITIES\n  Dense bituminous concrete wearing course 40 mm thick -- 42,194 rmt at Rs. 2,916 per rmt.\n  Supplying and erecting cautionary and informatory road signs -- 68,827 sqm at Rs. 6,461 per sqm.\n  Providing and fixing aluminium framed glazed windows -- 64,171 quintal at Rs. 5,061 per quintal.\n  Providing rain water harvesting structure with recharge pit -- 55,598 MT at Rs. 8,804 per MT.\n  Providing and fixing 200 mm dia DI K9 pipe including jointing -- 940 sqm at Rs. 3,656 per sqm.\n  Providing and laying M-25 grade cement concrete in foundation -- 65,664 rmt at Rs. 4,263 per rmt.\n  Laying of 11 kV XLPE underground cable including trenching -- 29,533 rmt at Rs. 3,912 per rmt.\n  Construction of RCC overhead service reservoir with staging -- 5,422 litre at Rs. 4,168 per litre.\n  Wet mix macadam laid in layers with mechanical paver finisher -- 61,364 sqm at Rs. 1,499 per sqm.\n\nKEY DATES\nPublication of notice: 26-07-2024.\nLast date and time for online submission of bids: 13-08-2024 at 17:00 hours.\nDate of opening of technical bids: 14-08-2024 at 11:00 hours.\n\nCONTACT\nSuperintending Engineer Ramakrishna Parulekar, Urban Development Authority, Fatehpur. Telephone 09013-704307. Electronic mail parulekar.fatehpur@urban.gov.in.\n\nGENERAL CONDITIONS\nThe bidder shall be responsible for obtaining all statutory clearances required for the work.\nNo claim for enhancement of rates shall be entertained during the currency of the contract.\nThe defect liability period shall commence from the date of completion certificate.\nConditional bids shall be summarily rejected.        396500000   2024-08-13
 



 Corpus-specific observations from portal_profiles.md



 PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> Get-Content .\portal_profiles.md
# Portal notes (scraping team, informal)

These are working notes, not a specification. They were written by three
different people over two years. Where they contradict the data, trust
the data -- but they will usually tell you *why* the data looks like it does.

## The nodal aggregators -- read this one first

`P001` `P002` `P003` `P004` `P005` `P006` are not procuring entities. They
are aggregation services that re-publish notices on behalf of departments,
and between them they account for a large fraction of everything we scrape.

Two things about them that have bitten us:

1. **They paste the same legal preamble onto every single notice.** P001,
   P002 and P005 use the ~1,400 character 'NATIONAL PROCUREMENT AGGREGATION
   SERVICE' block. P003, P004 and P006 use the 'STATE PROCUREMENT CELL'
   block, which is about the same size. We strip nothing -- the body column
   is exactly what the page contained.
2. **A short notice from one of these portals is mostly preamble.** We have
   entries where the actual tender text is under 600 characters sitting
   under 1,400 characters of boilerplate. Somebody on the ops team once
   complained that 'everything on P001 looks like everything else on P001'.
   They were not wrong.

P001, P002 and P005 also append a disclaimer footer.

## Reference numbers

Every portal invents its own. We have seen `NPAS-2024-0001234`,
`SPC/2024-25/004512`, `PWD/2024/00871`, bare `00048213`, `ref-2024-00912`,
`MC/2025/W/00311`, and `TN-000412/2024`. The same tender on three portals
has three unrelated reference numbers. There is no cross-walk table and
we have asked.

## Dates

`dd-mm-yyyy`, `dd/mm/yyyy`, `dd.mm.yyyy`, `yyyy-mm-dd`, `12 Mar 2024`,
`Mar 12, 2024`, `12-Mar-24`. The `published_at` column we store is our own
scrape timestamp normalised to ISO, but the dates *inside the body text*
are whatever the portal wrote.

## Money

The same estimated cost appears as `Rs. 4,50,00,000/-`, `Rs. 450.00 lakh`,
`INR 4.500 Cr`, `45000000`, and `RUPEES 4,50,00,000 ONLY`. The
`estimated_value` column is our parse of it and is usually right.

## Other habits

* A few portals publish everything in **UPPER CASE**.
* At least two truncate long notices -- one at about 1,200 characters, one
  at about 2,500. You get the head of the notice and nothing else.
* Corrigenda are published as **new notices**, not as edits. The title
  usually starts with 'Corrigendum' but not always, and the body repeats
  the original notice with a CORRIGENDUM section bolted on the end and a
  new closing date.
* Nodal agencies re-publish a notice days or weeks after the origin portal,
  so `published_at` ordering does not tell you which copy came first.

## Volume, top 15 portals

| portal | notices |
|---|---:|
| `P094` | 1,426 |
| `P002` | 800 |
| `P006` | 792 |
| `P001` | 778 |
| `P003` | 772 |
| `P005` | 768 |
| `P004` | 755 |
| `P020` | 384 |
| `P240` | 377 |
| `P044` | 224 |
| `P215` | 153 |
| `P181` | 133 |
| `P013` | 110 |
| `P227` | 107 |
| `P088` | 97 |

Total: 12,000 notices across 260 portals.

### A(a) Similarity representation experiment

The first experiment compared word-level and character-level TF-IDF representations using cosine similarity.

| Representation | Same pair | Different pair | Separation |
|---|---:|---:|---:|
| Word TF-IDF — raw | 0.7323 | 0.8280 | -0.0957 |
| Word TF-IDF — normalized | 0.7386 | 0.8300 | -0.0914 |
| Character TF-IDF — raw | 0.6057 | 0.3690 | +0.2367 |
| Character TF-IDF — normalized | 0.6246 | 0.3735 | +0.2511 |

Observation:

The word-level representation does not separate the selected labelled same/different examples: the different pair has a higher cosine similarity than the same pair.

The character-level representation separates the examples in the expected direction. Normalization improves the separation from 0.2367 to 0.2511.

The experiment therefore provides corpus-specific evidence for investigating normalized character n-grams as the primary text representation. This is not yet treated as the final choice; the representation will be evaluated across the full 900 labelled pairs before finalizing A(a).

PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> python .\scripts\a_similarity_experiment.py
Total notices: 12000

============================================================
WORD TF-IDF — RAW
============================================================
Features: 780
Same pair N010018-N010020: 0.7323
Different pair N007876-N008565: 0.828
Separation: -0.0957

============================================================
WORD TF-IDF — NORMALIZED
============================================================
Features: 763
Same pair N010018-N010020: 0.7386
Different pair N007876-N008565: 0.83
Separation: -0.0914

============================================================
CHARACTER TF-IDF — RAW
============================================================
Features: 14406
Same pair N010018-N010020: 0.6057
Different pair N007876-N008565: 0.369
Separation: 0.2367

============================================================
CHARACTER TF-IDF — NORMALIZED
============================================================
Features: 13858
Same pair N010018-N010020: 0.6246
Different pair N007876-N008565: 0.3735
Separation: 0.2511

### A(a) Full labelled-pair evaluation

The labelled sample contains 900 pairs:
- Same: 279 (31%)
- Different: 621 (69%)


PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> python .\scripts\a_similarity_experiment.py
Total notices: 12000

============================================================
WORD TF-IDF — RAW
============================================================
Features: 780
Same pair N010018-N010020: 0.7323
Different pair N007876-N008565: 0.828
Separation: -0.0957

============================================================
WORD TF-IDF — NORMALIZED
============================================================
Features: 763
Same pair N010018-N010020: 0.7386
Different pair N007876-N008565: 0.83
Separation: -0.0914

============================================================
CHARACTER TF-IDF — RAW
============================================================
Features: 14406
Same pair N010018-N010020: 0.6057
Different pair N007876-N008565: 0.369
Separation: 0.2367

============================================================
CHARACTER TF-IDF — NORMALIZED
============================================================
Features: 13858
Same pair N010018-N010020: 0.6246
Different pair N007876-N008565: 0.3735
Separation: 0.2511
PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> python .\scripts\a_labelled_evaluation.py
Total notices: 12000
Labelled pairs: 900
Same: 279
Different: 621
TF-IDF matrix shape: (12000, 131018)

============================================================
SIMILARITY BY LABEL
============================================================
           count      mean       std       min    median       max
label                                                             
different    621  0.424352  0.275698  0.096330  0.365522  0.970775
same         279  0.680784  0.283302  0.175535  0.724388  1.000000

============================================================
QUANTILES
============================================================

same
0.01    0.191081
0.05    0.255502
0.10    0.284782
0.25    0.390825
0.50    0.724388
0.75    0.975325
0.90    0.993766
0.95    0.997729
0.99    0.999519
Name: similarity, dtype: float64

different
0.01    0.103524
0.05    0.115495
0.10    0.130763
0.25    0.164396
0.50    0.365522
0.75    0.671988
0.90    0.916432
0.95    0.932968
0.99    0.947721
Name: similarity, dtype: float64

============================================================
THRESHOLD PERFORMANCE
============================================================
threshold=0.30 TP=246 FP=370 FN=33 TN=251 precision=0.399 recall=0.882 FPR=0.596
threshold=0.35 TP=227 FP=329 FN=52 TN=292 precision=0.408 recall=0.814 FPR=0.530
threshold=0.40 TP=204 FP=269 FN=75 TN=352 precision=0.431 recall=0.731 FPR=0.433
threshold=0.45 TP=186 FP=214 FN=93 TN=407 precision=0.465 recall=0.667 FPR=0.345
threshold=0.50 TP=179 FP=189 FN=100 TN=432 precision=0.486 recall=0.642 FPR=0.304
threshold=0.55 TP=176 FP=181 FN=103 TN=440 precision=0.493 recall=0.631 FPR=0.291
threshold=0.60 TP=170 FP=176 FN=109 TN=445 precision=0.491 recall=0.609 FPR=0.283
threshold=0.65 TP=160 FP=166 FN=119 TN=455 precision=0.491 recall=0.573 FPR=0.267
threshold=0.70 TP=148 FP=143 FN=131 TN=478 precision=0.509 recall=0.530 FPR=0.230
threshold=0.75 TP=134 FP=102 FN=145 TN=519 precision=0.568 recall=0.480 FPR=0.164
PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> 


### A(b) MinHash dependency

Command:
python -m pip install datasketch

Result:
Successfully installed datasketch-2.0.0
PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> python -m pip install datasketch
Defaulting to user installation because normal site-packages is not writeable
Collecting datasketch
  Downloading datasketch-2.0.0-py3-none-any.whl.metadata (10 kB)
Requirement already satisfied: numpy>=1.11 in C:\Users\ub02-glab-033\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages (from datasketch) (2.5.2)
Requirement already satisfied: scipy>=1.0.0 in C:\Users\ub02-glab-033\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages (from datasketch) (1.18.1)
Downloading datasketch-2.0.0-py3-none-any.whl (107 kB)
Installing collected packages: datasketch
Successfully installed datasketch-2.0.0

[notice] A new release of pip is available: 26.1.2 -> 26.2.1
[notice] To update, run: C:\Users\ub02-glab-033\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe -m pip install --upgrade pip


### A(b) Fixed-size representation and estimation accuracy

I reduced the normalized 5-character-shingle representation to a fixed-size MinHash signature.

The labelled corpus contained 900 pairs and 1,644 notices involved in those pairs. Exact Jaccard similarity had mean 0.520911, median 0.489195, minimum 0.205716 and maximum 1.0.


PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> python .\scripts\a_minhash_evaluation.py
Loading labelled pairs...
Notices used: 1644
Labelled pairs: 900

EXACT JACCARD
Mean: 0.520911
Median: 0.489195
Min: 0.205716
Max: 1.0

Unique shingles: 81428
Signatures: 300 / 1644
Signatures: 600 / 1644
Signatures: 900 / 1644
Signatures: 1200 / 1644
Signatures: 1500 / 1644

============================================================
SIGNATURE SIZE: 32
============================================================
Mean signed error: -0.001293
Mean absolute error: 0.058147
Median absolute error: 0.045966
90th percentile absolute error: 0.12938
95th percentile absolute error: 0.15557
Maximum absolute error: 0.261513
Within +/-0.05: 53.33 %
Within +/-0.10: 80.67 %

============================================================
SIGNATURE SIZE: 64
============================================================
Mean signed error: 0.016172
Mean absolute error: 0.044331
Median absolute error: 0.03957
90th percentile absolute error: 0.085787
95th percentile absolute error: 0.106364
Maximum absolute error: 0.182301
Within +/-0.05: 60.33 %
Within +/-0.10: 93.67 %

============================================================
SIGNATURE SIZE: 128
============================================================
Mean signed error: 0.011649
Mean absolute error: 0.029486
Median absolute error: 0.023506
90th percentile absolute error: 0.064365
95th percentile absolute error: 0.076104
Maximum absolute error: 0.129318
Within +/-0.05: 80.89 %
Within +/-0.10: 99.22 %

============================================================
SIGNATURE SIZE: 256
============================================================
Mean signed error: 0.019201
Mean absolute error: 0.02482
Median absolute error: 0.020296
90th percentile absolute error: 0.05317
95th percentile absolute error: 0.061041
Maximum absolute error: 0.099156
Within +/-0.05: 87.44 %
Within +/-0.10: 100.0 %

DONE
PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> 


### A(c) Sublinear candidate retrieval

I used MinHash LSH on the 128-permutation signatures to generate a candidate list before expensive pairwise comparison.

The candidate stage has a work/recall trade-off: using more bands with fewer rows per band increases the probability that a pair becomes a candidate, but also increases the number of candidate comparisons.

For the selected 16-bands × 8-rows configuration, empirical candidate survival increased strongly with true Jaccard similarity:


PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> python .\scripts\a_lsh_evaluation.py
Loading data...
Signatures created: 1644
C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2\scripts\a_lsh_evaluation.py:123: RuntimeWarning: Mean of empty slice
  "candidate_recall_same": survivors[pairs["label"].values == 1].mean(),
C:\Users\ub02-glab-033\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\numpy\_core\_methods.py:142: RuntimeWarning: invalid value encountered in scalar divide
  ret = ret.dtype.type(ret / rcount)
C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2\scripts\a_lsh_evaluation.py:123: RuntimeWarning: Mean of empty slice
  "candidate_recall_same": survivors[pairs["label"].values == 1].mean(),
C:\Users\ub02-glab-033\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\numpy\_core\_methods.py:142: RuntimeWarning: invalid value encountered in scalar divide
  ret = ret.dtype.type(ret / rcount)
C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2\scripts\a_lsh_evaluation.py:123: RuntimeWarning: Mean of empty slice
  "candidate_recall_same": survivors[pairs["label"].values == 1].mean(),
C:\Users\ub02-glab-033\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\numpy\_core\_methods.py:142: RuntimeWarning: invalid value encountered in scalar divide
  ret = ret.dtype.type(ret / rcount)
C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2\scripts\a_lsh_evaluation.py:123: RuntimeWarning: Mean of empty slice
  "candidate_recall_same": survivors[pairs["label"].values == 1].mean(),
C:\Users\ub02-glab-033\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\numpy\_core\_methods.py:142: RuntimeWarning: invalid value encountered in scalar divide
  ret = ret.dtype.type(ret / rcount)

LSH RESULTS
============================================================
Bands=32, Rows/band= 4, All-pair survival=0.6922, Same-pair recall=nan
Bands=16, Rows/band= 8, All-pair survival=0.2344, Same-pair recall=nan
Bands= 8, Rows/band=16, All-pair survival=0.1089, Same-pair recall=nan
Bands= 4, Rows/band=32, All-pair survival=0.0933, Same-pair recall=nan

SURVIVAL BY TRUE JACCARD
============================================================
0.2-0.3: survival=0.0000, pairs=82
0.3-0.4: survival=0.0000, pairs=195
0.4-0.5: survival=0.0217, pairs=184
0.5-0.6: survival=0.1313, pairs=198
0.6-0.7: survival=0.5351, pairs=114
0.7-0.8: survival=0.7200, pairs=25
0.8-0.9: survival=1.0000, pairs=6
0.9-1.0: survival=1.0000, pairs=95

Saved plot: lsh_survival_curve.png
PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> 


### B(d) Relational retrieval structure and physical access path

The retrieval structure was persisted as relational data in PostgreSQL.

Schema:
- `notice_lsh(notice_id, band_no, band_hash)`
- Primary key: `(notice_id, band_no)`
- B-tree index: `(band_no, band_hash)`
- `opportunity_card(card_id, created_at)`
- `notice_card_membership(notice_id, card_id)`
- `card_alias(old_card_id, new_card_id)`

The B-tree index was selected because retrieval queries constrain both `band_no` and `band_hash`, making an indexed equality lookup appropriate.

Measured indexed query:

- LSH rows stored: 192,000
- Planner path: `Index Scan using idx_notice_lsh_band_hash`
- Indexed execution time: 0.010 ms
- Indexed wall-clock time: 0.305 ms
- Buffers hit: 4

PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> docker exec -it exam-postgres psql -U postgres -d annapurna
psql (16.15 (Debian 16.15-1.pgdg13+2))
Type "help" for help.

annapurna=# CREATE TABLE IF NOT EXISTS notice_lsh (
    notice_id VARCHAR(50) NOT NULL,
    band_no INTEGER NOT NULL,
    band_hash BIGINT NOT NULL,
    PRIMARY KEY (notice_id, band_no)
);

CREATE INDEX IF NOT EXISTS idx_notice_lsh_band_hash
ON notice_lsh (band_no, band_hash);

CREATE TABLE IF NOT EXISTS opportunity_card (
    card_id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notice_card_membership (
    notice_id VARCHAR(50) PRIMARY KEY,
    card_id BIGINT REFERENCES opportunity_card(card_id)
);

CREATE TABLE IF NOT EXISTS card_alias (
);  new_card_id BIGINT REFERENCES opportunity_card(card_id)
CREATE TABLE
CREATE INDEX
CREATE TABLE
CREATE TABLE
CREATE TABLE
annapurna=# \q


PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> python .\scripts\b_retrieval_measurement.py
Preparing LSH records...
Prepared: 1000 / 12000
Prepared: 2000 / 12000
Prepared: 3000 / 12000
Prepared: 4000 / 12000
Prepared: 5000 / 12000
Prepared: 6000 / 12000
Prepared: 7000 / 12000
Prepared: 8000 / 12000
Prepared: 9000 / 12000
Prepared: 10000 / 12000
Prepared: 11000 / 12000
Prepared: 12000 / 12000
Inserting records...
Rows inserted: 192000

INDEXED RETRIEVAL
============================================================
Index Scan using idx_notice_lsh_band_hash on notice_lsh  (cost=0.42..8.44 rows=1 width=8) (actual time=0.006..0.006 rows=1 loops=1)
  Index Cond: ((band_no = 5) AND (band_hash = '6350469822547380905'::bigint))
  Buffers: shared hit=4
Planning:
  Buffers: shared hit=6
Planning Time: 0.040 ms
Execution Time: 0.010 ms

Indexed query results: 1
Indexed wall-clock time: 0.305 ms

FORCED SEQUENTIAL SCAN
============================================================
Gather  (cost=1000.00..3917.22 rows=1 width=8) (actual time=4.154..5.276 rows=1 loops=1)
  Workers Planned: 1
  Workers Launched: 1
  Buffers: shared hit=1223
  ->  Parallel Seq Scan on notice_lsh  (cost=0.00..2917.12 rows=1 width=8) (actual time=2.726..2.978 rows=0 loops=2)
        Filter: ((band_no = 5) AND (band_hash = '6350469822547380905'::bigint))
        Rows Removed by Filter: 96000
        Buffers: shared hit=1223
Planning Time: 0.023 ms
Execution Time: 5.287 ms

Sequential query results: 1
Sequential wall-clock time: 5.4663 ms

SUMMARY
============================================================
Total notices: 12000
Bands per notice: 16
Total LSH rows: 192000
Indexed time (ms): 0.305
Sequential time (ms): 5.4663
Speedup: 17.92 x

DONE
PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> 


#### Retrieval-quality cost of boilerplate mitigation

The mitigation was also evaluated against all 900 labelled pairs.

| Measure | Before | After |
|---|---:|---:|
| Same-pair mean Jaccard | 0.7002 | 0.7076 |
| Different-pair mean Jaccard | 0.4330 | 0.4330 |
| Same-pair recall at Jaccard >= 0.60 | 67.38% | 69.89% |
| Different-pair rate at Jaccard >= 0.60 | 7.41% | 6.28% |

The mitigation did not reduce same-pair retrieval quality on the labelled corpus. Instead, same-pair mean similarity increased by 0.0075 and same-pair recall at the 0.60 threshold increased by 2.51 percentage points. The different-pair rate decreased from 7.41% to 6.28%.


PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> python .\scripts\b_workload_analysis.py
Loading corpus...
Total notices: 12000
Total portals: 260

BEFORE MITIGATION
============================================================
Total comparisons: 3102498
Maximum workload: 1016025
Median workload: 72.0

Boilerplate removal time: 1.258 seconds

AFTER BOILERPLATE MITIGATION
============================================================
Total candidate comparisons: 1832268
Maximum bucket workload: 318003
Median bucket workload: 0.0
Mean bucket workload: 454.21

LARGEST REMAINING BUCKETS
P002_standard terms and c: notices=798, comparisons=318003
P006_-- consolidated tend: notices=792, comparisons=313236
P001_standard terms and c: notices=777, comparisons=301476
P003_-- consolidated tend: notices=772, comparisons=297606
P005_standard terms and c: notices=768, comparisons=294528
P004_-- consolidated tend: notices=755, comparisons=284635
P094_tender notice: corri: notices=64, comparisons=2016
P094_nit for corrigendum : notices=54, comparisons=1431
P094_electrification of t: notices=42, comparisons=861
P094_desilting and lining: notices=42, comparisons=861
P094_e-tender - corrigend: notices=42, comparisons=861
P094_periodic renewal coa: notices=41, comparisons=820
P094_construction of the : notices=41, comparisons=820
P094_supply and installat: notices=39, comparisons=741
P094_repair and renovatio: notices=38, comparisons=703

WORKLOAD REDUCTION
============================================================
Before: 3102498
After: 1832268
Reduction: 40.94 %

DONE
PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> 


PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> python .\scripts\b_final_quality.py
Loading labelled pairs...

BOILERPLATE MITIGATION QUALITY
============================================================
Same pairs: 279
Different pairs: 621

RAW JACCARD
Same mean: 0.7002
Different mean: 0.433

CLEANED JACCARD
Same mean: 0.7076
Different mean: 0.433

CHANGE
Same-pair mean change: 0.0075
Different-pair mean change: -0.0

AT JACCARD THRESHOLD = 0.6
Raw same-pair recall: 67.38 %
Cleaned same-pair recall: 69.89 %
Raw different-pair rate: 7.41 %
Cleaned different-pair rate: 6.28 %

DONE
PS C:\Users\ub02-glab-033\Desktop\suhita_labexam\data_2\data_2> 