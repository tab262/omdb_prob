import sys
import json
import urllib2
#import requests



class Movie:
    def __init__(self, title_and_year_line):
        [title, year] = self.processInput(title_and_year_line)
        self.title = title
        self.year = year
        self.movie_dict = {}
       
        # Make the query call
        self.queryOmdbApi()



    def queryOmdbApi(self):
        if(self.year is not ''):
            api_url = "http://www.omdbapi.com/?t="+self.title.replace(" ","%20")+"&y="+self.year
        else:
            api_url = "http://www.omdbapi.com/?t="+self.title.replace(" ","%20")


        self.movie_dict = json.load(urllib2.urlopen(api_url))


        if(self.movie_dict['Response'] == 'False'):
            print "PROBLEM WITH: " + self.title + "@" + api_url
           # Temp solution is to assign rating of not found
            self.movie_dict['imdbRating'] = 'Movie Not Found'
        


    def processInput(self,line):
        commas = self.findCharOccurences(line,",")

        # TODO: The following line here does some string manipulation work to make sure the URL
        # will not have any characters in it that are invalid for URL. A more robust
        # solution is to use urllib to encode the url.
        movie_title = line[0:commas[-1]].replace('"','')
        year = line[commas[-1]+1:]
        return [movie_title, year]
        


    def findCharOccurences(self,string,char):
        return [c for c, letter in enumerate(string) if letter == char]

        

    def __str__(self):
        if(self.movie_dict['Response'] == "True"):
            return ((self.title.replace("%20"," ")).decode('ascii','ignore') + " -- " + self.movie_dict['imdbID'])

def main(argv):
    lofm = [Movie("True Grit,1969"),
            Movie("Mission Impossible,2000"),
            Movie("The Yearling,1946"),
            Movie("Yesterday, Today and Tomorrow,1964"),
        ]


    

    for x in lofm:
        print x

    print "Sorting..."
    print "-" * 30
    lofm2 = sorted(lofm, key=lambda movie: movie.movie_dict['imdbRating'], reverse=True)

    for x in lofm2:
        print(x)


if __name__=="__main__":main(sys.argv)
