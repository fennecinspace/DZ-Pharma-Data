# DZ PHAMRA DATA
This is an attempt to collect all medications in algeria.<br>
`result_formated.json` is a prettified version of `result.json`, which contains data for 4849 different medications

- the data is formatted as follows:

```
{
  "A": [medications that begin with the letter A],
  ....
  "Z": [medications that begin with the letter Z]
}
```
- this is an example of the data collected for a single medication:

```JSON
{
  "Nom": "ABASAGLAR 100UI/ML (3,64MG/ML) SOL. INJ. EN STYLO PREREMPLI KWIKPEN  B/05 STYLOS PREREMLIS DE 3 ML",
  "Img": "https://pharmnet-dz.com//img/medics/5866.png",
  "Notice": "https://pharmnet-dz.com/notice.ashx?id=5866",
  "Laboratoire": " ELI LILLY",
  "C.Pharmacologique": " INSULINES",
  "C.Therapeutique": " METABOLISME NUTRITION DIABETE",
  "Info": " INSULINE GLARGINE",
  "Liste": "Liste II",
  "Pays": "AUTRICHE",
  "Nom Commercial": "ABASAGLAR",
  "Tarif de reference": "- DA",
  "PPA": " DA",
  "Code DCI": "14B215",
  "Forme": "SOL. INJ.",
  "Dosage": "100UI/ML (3,64MG/ML)",
  "Conditionnement": "B/05 STYLOS PREREMLIS DE 3 ML",
  "Commercialisation": true,
  "Remboursable": true
}
```
