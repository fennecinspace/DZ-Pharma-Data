# DZ PHAMRA DATA

This is an attempt to collect all medications in algeria.<br>
`result_formated.json` is a prettified version of `result.json`, which contains data for 4849 different medications

- the data is formatted as follows:

```JSON
{
  "A": [medications that begin with the letter A],
  ....
  "Z": [medications that begin with the letter Z]
}
```

- this is an example of the data collected for a single medication:

```JSON
{
  "nom": "PROTON 20MG GLES. A MICROG. GASTRORESIST.  B/28",
  "link": "https://pharmnet-dz.com/medic.aspx?id=6102",
  "Img": "https://pharmnet-dz.com/ImageHandler.ashx?imageurl=/img/medic.png",
  "Laboratoire": " PHARMALLIANCE",
  "C.Pharmacologique": " ANTI-ULCEREUX & ANTI-H2",
  "C.Therapeutique": " GASTRO-ENTEROLOGIE",
  "Info": " OMEPRAZOLE",
  "Liste": "Liste II",
  "Pays": "ALGERIE",
  "Tarif de reference": "392.00 DA",
  "PPA": "311.70 DA",
  "Num Enregistrement": "035/ 10 A 001 /97/08",
  "Nom Commercial": "PROTON",
  "Code DCI": "10A001",
  "Forme": "GLES",
  "Dosage": "20MG",
  "Conditionnement": "B/28",
  "Commercialisation": true,
  "Remboursable": true
}
```
