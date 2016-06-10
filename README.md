# scopus_tools

Takes list of articles titles, searches title as phrase in title field in Scopus w/ the scopus search API
if there is exactly 1 result, find the ID of that article
call back the Scopus abstrace API to retrieve the text of the abstract
write the retrieved title & retrieved abstract to a file
