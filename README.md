# DZ PHAMRA DATA

This is an attempt to collect all medications in algeria.<br>

- the data is formatted as follows:

```text
{
  "A": [medications that begin with the letter A],
  ....
  "Z": [medications that begin with the letter Z]
}
```

- this is an example of the data collected for a single medication:

```JSON
{
  "name": "ABASAGLAR 100UI/ML (3,64MG/ML) SOL. INJ. EN STYLO PREREMPLI KWIKPEN  B/05 STYLOS PREREMLIS DE 3 ML",
  "link": "https://pharmnet-dz.com/m-5866-abasaglar-100ui-ml-3-64mg-ml-sol-inj-en-stylo-prerempli-kwikpen-b-05-stylos-preremlis-de-3-ml",
  "img": "https://pharmnet-dz.com/ImageHandler.ashx?imageurl=/img/medics/5866.png",
  "notice": "https://pharmnet-dz.com/notice.ashx?id=5866",
  "lab": {
      "name": "ELI LILLY",
      "link": "https://pharmnet-dz.com/l-84-eli-lilly"
  },
  "class": {
      "pharmacological": "INSULINES",
      "therapeutic": "METABOLISME NUTRITION DIABETE"
  },
  "generic": "INSULINE GLARGINE",
  "Liste": "Liste II",
  "Pays": "AUTRICHE",
  "Tarif de reference": "6708.11 DA",
  "PPA": "6708.11 DA",
  "Num Enregistrement": "034/14B215/17",
  "Nom Commercial": "ABASAGLAR",
  "Code DCI": "14B215",
  "Forme": "SOL. INJ",
  "Dosage": "100UI/ML (3,64MG/ML)",
  "Conditionnement": "B/05 STYLOS PREREMLIS DE 3 ML",
  "Commercialisation": true,
  "Remboursable": true
}
```

- the labs that released the drugs are included in the data too, in this format:

```JSON
{
  "name": "PHARMA IVAL",
  "link": "https://pharmnet-dz.com/l-221-pharma-ival",
  "img": "https://pharmnet-dz.com/ImageHandler.ashx?imageurl=img/labos/221.png",
  "address": "8, rue d\u00e2\u0080\u0099Alep, Delmonte, Oran - Route de Bouchaoui, Ouled Fayet, Alger",
  "tel": "+213 (0) 21 38 82 03 - +213 (0) 41 43 60 70",
  "web": "www.ivalpharma.com"
}
```
