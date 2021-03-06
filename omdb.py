from Movie import Movie
import sys
import datetime
SUPPORTED_SORT_KEYS = ['imdbRating','imdbID','Year']

def main(argv):
    
    # Basic command line parsing and error checking
    if(len(argv) < 3):
        printUsage()


    movie_file = argv[1]
    output_file = open(argv[2],'w')
    
    sort_key = 'imdbRating'
    if(len(argv) == 4):
        if argv[3] not in SUPPORTED_SORT_KEYS:
            print "Sorting by '" + argv[3] + "' key not supported"
            print "Supported keys: " + str(SUPPORTED_SORT_KEYS)
            exit(1)
        else: 
            #user passed a valid key to sort by
            sort_key = argv[3]
    



    print "Will sort by " + sort_key + " key"
    

    # Opening the .csv file
    movie_list = open(movie_file).read().split("\n")

    # TODO: check that file has valid contents
    
    # Log file is used to keep track of movies that are not found
    log_file = open('error_logs.txt','a')
    log_file.write('-' * 30)
    log_file.write("\n" + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + "\n")

    # instantiate lists for movies and for movies not found
    # The ml list is only list of movies we sort
    ml = []
    movie_not_found = []
    for movie in movie_list:
        if(movie is ''):
            #empty line case
            break
        # instantiate movie object for each line
        m = Movie(movie)
        
        # Logic checking whether movie was found
        if m.movie_dict['Response'] == 'True': 
            # Valid response was receieved
            ml.append(m)
            # Being extra careful with the try-except block here
            try:
                print m
            except e:
                pass
        else:
            # Valid response was not receieved
            movie_not_found.append(m)
            log_file.write("MOVIE NOT FOUND: " + m.title + "\n")


    # Done with the log file
    log_file.close()

    
    print '-' * 30
    print "SORTING - DESCENDING ORDER by " + sort_key + " key"
    print '-' * 30

    # Sorting logic
    sorted_ml = sorted(ml, key=lambda movie: movie.movie_dict[sort_key], reverse=True)


    # Basic write/print logic that is dictated by whether we are sorting by a provided key
    # If a key is provided, the write/print for each movie will include the title, IMDB score 
    # and the value of the provided key. Given the current lack of support for non-ascii characters
    # there are a number of try-except blocks to prevent errors. See TODO in movies.__str__()
    for movie in sorted_ml:
        if(sort_key is not "imdbRating"):
            try:
                string_to_print = str(movie) + " -- " + str(movie.movie_dict[sort_key]).decode('ascii','ignore') + "\n"
            except Exception:
                pass
            #output_file.write(str(movie) + " -- " + str(movie.movie_dict[sort_key]) + "\n")
        else:
            try:
                string_to_print = str(movie) + "\n"
            except Exception:
                pass
            #output_file.write(str(movie) + "\n")

        # TODO: See Movie.__str__. Try-except is current in place since non-ascii character support has
        # not been implemented
        try:
            output_file.write(string_to_print)
            print string_to_print
        except Exception:
            pass


# Helper function to print usage
def printUsage():
    print "python main [input csv file] [output destination.txt] [optional: sort key]  "
    exit(1)


if __name__=="__main__":main(sys.argv)
