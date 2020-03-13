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
	"name": "BACTIZOL 1G/FL PDRE. ET SOLV.SOL.INJ. IM B/1FL. PDRE. + 1AMP.SOLV. (0,5% LIDOCAINE) DE 4ML",
	"link": "https://pharmnet-dz.com/m-1905-bactizol-1g-fl-pdre-et-solv-sol-inj-im-b-1fl-pdre--1amp-solv--0-5-lidocaine-de-4ml",
	"img": "https://pharmnet-dz.com/ImageHandler.ashx?imageurl=/img/medic.png",
	"notice": "https://pharmnet-dz.com//notice.ashx?id=896",
	"lab": {
		"name": "SAIDAL GROUPE",
		"link": "https://pharmnet-dz.com/l-252-saidal-groupe",
		"img": "https://pharmnet-dz.com/ImageHandler.ashx?imageurl=img/labos/252.png",
		"address": "Route de wilaya n\u00c2\u00b011 BP 141 Dar El Beida - Alger",
		"tel": "+213 23 75 10 28 - +213 23 92 01 76",
		"web": "www.saidalgroup.dz"
	},
	"class": {
		"pharmacological": "CEPHALOSPORINES",
		"therapeutic": "INFECTIOLOGIE"
	},
	"generic": "CEFAZOLINE",
	"commercialisation": true,
	"refundable": null,
	"list": "Liste I",
	"country": "ALGERIE",
	"commercial_name": "BACTIZOL",
	"reference_rate": "129 DA",
	"ppa": null,
	"registration": "003/ 13 B 013 /01/09",
	"dci": "13B013",
	"form": "PDRE. INJ",
	"dosage": "1G/FL",
	"conditioning": "B/1FL. PDRE. + 1AMP.SOLV. (0,5% LIDOCAINE) DE 4ML"
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
