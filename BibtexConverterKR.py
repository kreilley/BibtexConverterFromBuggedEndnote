"""
BibtexConverterKR.py

Converts fullFields.txt (ENL RTF File Export) to outfile.bib (BIBTEX formatting)

Run from terminal or cmd using "python BibtexConverterKR.py" in the same directory as fullFields.txt and outfile.bib

This file was thrown together quickly for a specific purpose; unless you have the same issue in the same environment (mac osx endnote export), many changes will have to be made for it to be useful.

The class defined below stores the metadata for a single bibtex database entry.  To record the entry, use the outString parameter as seen in __name__=="__main__". Alternatively, you could dump a dictionary of entries (e.g., json.dump(enlDict)) to json to store all data, but you would still need to compile the .bib file somehow.

%author:  kreilley

"""


import re


class BibTexDictionaryEntry:
    def __init__(self):
        self.bibtexTypes = ["article","book","booklet","conference","inbook","incollection","inproceedings","manual","mastersthesis","misc","phdthesis","proceedings","techreport","unpublished"]
        self.bibtexFields = ["ENTRYTYPE","address","annote","author", "booktitle","chapter","crossref","edition", "editor", "howpublished", "institution", "journal", "key", "month", "note", "number", "organization", "pages", "publisher", "school", "series", "title", "type", "volume", "year", "URL", "ISBN", "ISSN", "LCCN", "abstract", "keywords", "price", "copyright", "language", "contents", "doi","label","Date-Added","file"]
        self.numFields = len(self.bibtexFields)
        self.dictionaryArray = [{} for ndx in range(self.numFields)]
        self.outString = ""
        self.inString = []
        self.individualInputElements = ""
    
    def updateField(self, aToken, aValue):
        if "Reference Type" in aToken:
            jdx = self.bibtexFields.index("ENTRYTYPE")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Record Number" in aToken:
            jdx = self.bibtexFields.index("key")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Author" in aToken:
            jdx = self.bibtexFields.index("author")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Year" in aToken:
            jdx = self.bibtexFields.index("year")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Title" in aToken:
            jdx = self.bibtexFields.index("title")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Conference Name" in aToken:
            jdx = self.bibtexFields.index("booktitle")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Pages" in aToken:
            jdx = self.bibtexFields.index("pages")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Label" in aToken:
            jdx = self.bibtexFields.index("label")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Research Notes" in aToken:
            jdx = self.bibtexFields.index("annote")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "University" in aToken:
            jdx = self.bibtexFields.index("school")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Date" in aToken:
            jdx = self.bibtexFields.index("year")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Short Title" in aToken:
            jdx = -1
            print "Skipped setting field:  ",aToken," in dictionary\n"
        elif "URL" in aToken:
            jdx = self.bibtexFields.index("URL")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Access Date" in aToken:
            jdx = self.bibtexFields.index("Date-Added")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Volume" in aToken:
            jdx = self.bibtexFields.index("volume")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "DOI" in aToken:
            jdx = self.bibtexFields.index("doi")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif """'File' Attachments""" in aToken:
            jdx = self.bibtexFields.index("file")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue

        elif "Institution" in aToken:
            jdx = self.bibtexFields.index("institution")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue
        elif "Publisher" in aToken:
            jdx = self.bibtexFields.index("publisher")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue
        elif "Issue" in aToken:
            jdx = self.bibtexFields.index("number")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue
        elif "Editor" in aToken:
            jdx = self.bibtexFields.index("editor")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue
        elif "Conference Location" in aToken:
            jdx = self.bibtexFields.index("address")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue
        elif "Place Published" in aToken:
            jdx = self.bibtexFields.index("address")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue
        elif "Series Title" in aToken:
            jdx = self.bibtexFields.index("series")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue
        elif "Journal" in aToken:
            jdx = self.bibtexFields.index("journal")
            self.dictionaryArray[jdx][self.bibtexFields[jdx]] = aValue
        else:
            jdx = -2
            print "The field ",aToken," is currently unknown\n"
       
    def makeString(self):
        IndexerValues = range(self.numFields)
        self.jET = self.bibtexFields.index("ENTRYTYPE")
        eType = self.dictionaryArray[self.jET][self.bibtexFields[self.jET]]
        self.jLL = self.bibtexFields.index("label")
        eLabel = self.dictionaryArray[self.jLL][self.bibtexFields[self.jLL]]
        self.outString = self.outString+"@"+eType+"{"+eLabel+",\n"
        
        for k in IndexerValues :
            if ((k != self.jET) and (k != self.jLL) and (self.dictionaryArray[k] != {})):
                self.outString = self.outString + self.bibtexFields[k] + " = {" + str(self.dictionaryArray[k][self.bibtexFields[k]]) + "},\n"
            else:
                print "no entry for:  " + self.bibtexFields[k]+"\n"
        self.outString = self.outString + "}\n\n"
        print self.outString
    def fixType(self):
        currType = self.dictionaryArray[self.bibtexFields.index("ENTRYTYPE")][self.bibtexFields[self.bibtexFields.index("ENTRYTYPE")]]
        if not (currType in self.bibtexFields):
            if "Conference Paper" in currType:
                self.dictionaryArray[self.bibtexFields.index("ENTRYTYPE")][self.bibtexFields[self.bibtexFields.index("ENTRYTYPE")]]=self.bibtexTypes[self.bibtexTypes.index("inproceedings")]
            elif "Thesis" in currType:
                self.dictionaryArray[self.bibtexFields.index("ENTRYTYPE")][self.bibtexFields[self.bibtexFields.index("ENTRYTYPE")]]=self.bibtexTypes[self.bibtexTypes.index("phdthesis")]
            elif "Electronic Book Section" in currType:
                self.dictionaryArray[self.bibtexFields.index("ENTRYTYPE")][self.bibtexFields[self.bibtexFields.index("ENTRYTYPE")]]=self.bibtexTypes[self.bibtexTypes.index("inbook")]
            elif "Journal Article" in currType:
                self.dictionaryArray[self.bibtexFields.index("ENTRYTYPE")][self.bibtexFields[self.bibtexFields.index("ENTRYTYPE")]]=self.bibtexTypes[self.bibtexTypes.index("article")]
            elif "Report" in currType:
                self.dictionaryArray[self.bibtexFields.index("ENTRYTYPE")][self.bibtexFields[self.bibtexFields.index("ENTRYTYPE")]]=self.bibtexTypes[self.bibtexTypes.index("techreport")]
            elif ("Book Section" in currType) and not ("Electronic" in currType):
                self.dictionaryArray[self.bibtexFields.index("ENTRYTYPE")][self.bibtexFields[self.bibtexFields.index("ENTRYTYPE")]]=self.bibtexTypes[self.bibtexTypes.index("inbook")]
            elif "Conference Proceedings" in currType:
                self.dictionaryArray[self.bibtexFields.index("ENTRYTYPE")][self.bibtexFields[self.bibtexFields.index("ENTRYTYPE")]]=self.bibtexTypes[self.bibtexTypes.index("proceedings")]
            elif "Book" in currType and not ("Section" in currType):
                self.dictionaryArray[self.bibtexFields.index("ENTRYTYPE")][self.bibtexFields[self.bibtexFields.index("ENTRYTYPE")]]=self.bibtexTypes[self.bibtexTypes.index("book")]
            elif "Web Page" in currType:
                self.dictionaryArray[self.bibtexFields.index("ENTRYTYPE")][self.bibtexFields[self.bibtexFields.index("ENTRYTYPE")]]=self.bibtexTypes[self.bibtexTypes.index("misc")]
            elif "Electronic Book" in currType and not ("Section" in currType):
                self.dictionaryArray[self.bibtexFields.index("ENTRYTYPE")][self.bibtexFields[self.bibtexFields.index("ENTRYTYPE")]]=self.bibtexTypes[self.bibtexTypes.index("book")]
            else:
                print "error on type fix\n"
        else:
            print "Current Type is Valid\n"

    def collapseEntry(self,startPoint,endPoint,allTextList):
        var = allTextList[startPoint:endPoint]
        for l in var:
            self.inString.append(l)


    def classMain(self):

        for someItem in self.inString:
            chunks = someItem.strip().split(':')
            print "Chunk is:  ",chunks,"\n"
            if len(chunks)>1 and (("Reference Type" in chunks[0]) or ("Record Number" in chunks[0]) or ("Author" in chunks[0]) or ("Year" in chunks[0]) or ("Title" in chunks[0]) or ("Conference Name" in chunks[0]) or ( "Pages" in chunks[0]) or ( "Label" in chunks[0]) or ( "Research Notes" in chunks[0]) or ( "University" in chunks[0]) or ( "Date" in chunks[0]) or ( "Short Title" in chunks[0]) or ( "URL" in chunks[0]) or ( "Access Date" in chunks[0]) or ( "Volume" in chunks[0]) or ( "DOI" in chunks[0]) or ( """'File' Attachments""" in chunks[0]) or ( "Institution" in chunks[0]) or ( "Publisher" in chunks[0]) or ( "Issue" in chunks[0]) or ( "Editor" in chunks[0]) or ( "Conference Location" in chunks[0]) or ( "Place Published" in chunks[0]) or ( "Series Title" in chunks[0]) or ( "Journal" in chunks[0])):
                key = chunks[0]
                #print "key is:  ",key,"\n"
                try:
                    val = int(chunks[1])
                except ValueError:
                    try:
                        val = float(chunks[1])
                    except ValueError:
                        val = chunks[1]
                #.strip("none")
                self.updateField(key,val)
                    #print "this value is:  ",val,"\n"
            else:
                val = val+someItem
                self.updateField(key,val)
                #print "updated key ",key," value to:  ",val,"\n"

        # print "...Finished chunking\n\n"
        self.fixType()
        self.makeString()
    #    if "Conference Paper" in item
    #        aType = entryType[7]
    #        print aType,"\n"
    #    if "Record Number" in item
    #        val = re.search('[0-9]',item).group(0)
    
    
        self.individualInputElements = [re.split(":  |: ", someItem, 2) for someItem in self.inString]
        #print individualInputElements,"\n"


# Conference Paper, Thesis, Electronic Book Section, Journal Article, Report, Book Section, Conference Proceedings, Book, Web Page, Electronic Book,

if __name__ == '__main__':
    
    with open('fullFields.txt','r') as f:
        fileText = list(f)
    entryCount = 0
    currIndex = 0
    indexLocations = []
    for l in fileText:
        if 'Reference Type' in l:
            entryCount +=1
            indexLocations.append(currIndex)
            currIndex += 1
        else:
            currIndex += 1
    print "\nnumber of entries {} at:\n".format(entryCount)
    print indexLocations
    print "\n"
    print len(indexLocations)
    print "\n"
    
    enlDict = dict.fromkeys(indexLocations)
    f = open('outfile.bib','a')
    for k in enlDict.iterkeys():
        enlDict[k] = BibTexDictionaryEntry()
        ndx = indexLocations.index(k)
        if ndx < (len(indexLocations)-1):
            ep = indexLocations[ndx+1]-1
        else:
            ep = len(fileText)-1
        enlDict[k].collapseEntry(k,ep,fileText)
        enlDict[k].classMain()
        f.write(enlDict[k].outString)
    f.close()
    
    print "...End Program\n\n"

#Sample data



#Reference Type:  Conference Paper
#Record Number: 4
#Author: Andrade, Ermeson, Maciel, Paulo, Callou, Gustavo and Nogueira, Bruno
#Year: 2009
#Title: A methodology for mapping sysml activity diagram to time petri net for requirement validation of embedded real-time systems with energy constraints
#Conference Name: Digital Society, 2009. ICDS'09. Third International Conference on
#Pages: 266--271
#Label: AndradeMacielCallouEtAl2009




















