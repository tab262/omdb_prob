from Movie import Movie
import sys

def main(argv):
    if(len(argv) < 3):
        printUsage()
        exit(1)

    movie_file = argv[1]
    output_file = argv[2]

    if(len(argv) == 4):
        #user passed a key to sort by
        sort_key = argv[3]
        print "Will sort by " + sort_key + " key"
    else:
        sort_key = 'imdbRating'
    
    movie_list = open(movie_file).read().split("\n")

    log_file = open('error_logs.txt','w')

    ml = []
    movie_not_found = []
    for movie in movie_list:
        #print movie
        m = Movie(movie)
        if m.movie_dict['Response'] == 'True':
            ml.append(m)
            print m
        else:
            movie_not_found.append(m)
            log_file.write("MOVIE NOT FOUND: " + m.title + "\n")



    log_file.close()


    print '-' * 30
    print "SORTING - DESCENDING ORDER"
    print '-' * 30

    sorted_ml = sorted(ml, key=lambda movie: movie.movie_dict[sort_key], reverse=True)

    #out_file = open("output.txt",'w')


    for x in sorted_ml:
        print x


def printUsage():
    print "python main [input csv file] [output destination.txt] [optional: sort key]  "

if __name__=="__main__":main(sys.argv)
