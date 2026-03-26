# RemoveDuplicatesFromVCF

A simple python script who removes duplicate contacts from a vcf file. 

It's a vibecoded fork of a vibecode tool because

![Alt Text](https://media1.tenor.com/m/ESyxZedT-kEAAAAd/perch%C3%A9a-noi-la-qualita-c-ha-rotto-er-cazzo.gif)

## Features:
- Removes duplicate contacts based on phone numbers
- Cleans & formats numbers automatically (+39 for 10-digit numbers)
- Merges duplicate contacts, even if fields are reordered
- Eliminates duplicate phone numbers within the same contact

## Usage:
python .\RemoveDuplicateVCF.py input.vcf output