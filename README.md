# A script to search the DVRA members spreadsheet for a mailing address by name or callsign

## Usage:
* first, download the spreadsheet to the same directory as the script as 'spreadsheet.xlsx'
* then to query, run 
    lookup-member-address.py <criteria>

  the script will attempt a partial match on first name, last name, and callsign

* if there is a single match, or multiple matches all with the same address, the match will be printed
and copied to the clipboard

* if there are multiple non-unique matches, they will be listed, but nothing will be copied to the clipboard
  