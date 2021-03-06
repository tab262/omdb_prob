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
        # Some lines of the input may not have the year. Not DRY for clarity
        if(self.year is not ''):
            api_url = "http://www.omdbapi.com/?t="+self.title.replace(" ","%20")+"&y="+self.year
        else:
            api_url = "http://www.omdbapi.com/?t="+self.title.replace(" ","%20")

            
        # Making the API call
        # TODO: Error catching for cases when the API is down or
        # connection fails
        try:
            self.movie_dict = json.load(urllib2.urlopen(api_url))
        except Exception:
            self.movie_dict = {'Response' : 'False'}

        # In input year was missing, grab it from the movie_dict
        if(self.movie_dict['Response'] == 'True'):
            self.year =self.movie_dict['Year']
        

        # Handling empty response
        if(self.movie_dict == ''):
            self.movie_dict = {'Response' : 'False'}
        
        if(self.movie_dict['Response'] == 'False'):
            # TODO: Explore other options for handling this case
            # In some cases, the year was simply wrong and the movie
            # exists. Other options would be to try the search function of 
            # the API
            print "PROBLEM WITH: " + self.title + "@" + api_url
            # Temp solution is to assign rating of not found
            self.movie_dict['imdbRating'] = 'Movie Not Found'
        


    def processInput(self,line):
        # Main parsing function to extract the title and the year of the input line
        commas = self.findCharOccurences(line,",")

        # TODO: The following line here does some string manipulation work to make sure the URL
        # will not have any characters in it that are invalid for URL. A more robust
        # solution is to use urllib to encode the url.
        movie_title = line[0:commas[-1]].replace('"','')
        year = line[commas[-1]+1:]
        return [movie_title, year]
        


    def findCharOccurences(self,string,char):
        # Helper function for parsing line
        return [c for c, letter in enumerate(string) if letter == char]

        

    def __str__(self):
        # TODO: Support for printing non-ASCII characters
        # the .decode('ascii','ignore') current removes any offending (non-ascii) 
        # characters. 
        if(self.movie_dict['Response'] == "True"):
            return ((self.title.replace("%20"," ")).decode('ascii','ignore') + " -- " + self.movie_dict['imdbRating'])

def main(argv):
    # Basic test case
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
