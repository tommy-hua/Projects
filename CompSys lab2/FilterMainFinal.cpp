#include <stdio.h>
#include "cs1300bmp.h"
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include "Filter.h"

using namespace std;

#include "rdtsc.h"

//
// Forward declare the functions
//
Filter * readFilter(string filename);
double applyFilter(Filter *filter, cs1300bmp *input, cs1300bmp *output);

int
main(int argc, char **argv)
{

  if (argc < 2) {
    fprintf(stderr,"Usage: %s filter inputfile1 inputfile2 .... \n", argv[0]);
  }

  //
  // Convert to C++ strings to simplify manipulation
  //
  string filtername = argv[1];

  //
  // remove any ".filter" in the filtername
  //
  string filterOutputName = filtername;
  string::size_type loc = filterOutputName.find(".filter");
  if (loc != string::npos) {
    //
    // Remove the ".filter" name, which should occur on all the provided filters
    //
    filterOutputName = filtername.substr(0, loc);
  }

  Filter *filter = readFilter(filtername);

  double sum = 0.0;
  int samples = 0;

  for (int inNum = 2; inNum < argc; inNum++) {
    string inputFilename = argv[inNum];
    string outputFilename = "filtered-" + filterOutputName + "-" + inputFilename;
    struct cs1300bmp *input = new struct cs1300bmp;
    struct cs1300bmp *output = new struct cs1300bmp;
    int ok = cs1300bmp_readfile( (char *) inputFilename.c_str(), input);

    if ( ok ) {
      double sample = applyFilter(filter, input, output);
      sum += sample;
      samples++;
      cs1300bmp_writefile((char *) outputFilename.c_str(), output);
    }
    delete input;
    delete output;
  }
  fprintf(stdout, "Average cycles per sample is %f\n", sum / samples);

}

class Filter *readFilter(string filename){
    ifstream input(filename.c_str());
    if ( ! input.bad() ) {
        short size = 0;
        input >> size;
        Filter *filter = new Filter(size); //dim
        short div;
        input >> div;
        filter -> divisor = div; //bc everything public we can skip call of setDiv
        short value;
        for (int i = 0; i < size; i++) {
            for(int j = 0; j < size; j++){
                input >> value;
                filter -> set(i, j, value);
            }
        }
        return filter;
    } else {
        cerr << "Bad input in readFilter:" << filename << endl;
        exit(-1);
    }
}


double applyFilter(class Filter *filter, cs1300bmp *input, cs1300bmp *output){
    long long cycStart, cycStop;
    
    cycStart = rdtscll();

    output -> width = input -> width;
    output -> height = input -> height;
    
    //make variable for to alleviate method calls
    float div = (float) (1 / (float)filter -> getDivisor()); //must cast to float for this to work (recitation)
    short h = input -> height;
    short w = input -> width;
    
    short filterArray[] = { //array with data values to alleviate filter -> get (i, j)
        filter -> data[0],
        filter -> data[1],
        filter -> data[2],
        filter -> data[3],
        filter -> data[4],
        filter -> data[5],
        filter -> data[6],
        filter -> data[7],
        filter -> data[8],
    };
    //pragma from openMP, allows for parallel processing
    //splits thread into multiple teams of threads based and divides the work of the for loop amongst the team of threads
    #pragma omp parallel for
    //reorder loops to minimize cache misses
    for(int plane = 0; plane < 3; plane++) { //all filters have a size of 3
        for(int row = 1; row < h - 1 ; row++) {
            for(int col = 1; col < w - 1; col++) { 
                //unroll both i and j loops
                short acc = 0;  //an accumulator
                output -> color[plane][row][col] = 0;
                
                acc += (input -> color[plane][row + 0 - 1][col + 0 - 1] * filterArray[0] ); 
                acc += (input -> color[plane][row + 0 - 1][col + 1 - 1] * filterArray[1] );
                acc += (input -> color[plane][row + 0 - 1][col + 2 - 1] * filterArray[2] );

                acc += (input -> color[plane][row + 1 - 1][col + 0 - 1] * filterArray[3] );
                acc += (input -> color[plane][row + 1 - 1][col + 1 - 1] * filterArray[4] );
                acc += (input -> color[plane][row + 1 - 1][col + 2 - 1] * filterArray[5] );

                acc += (input -> color[plane][row + 2 - 1][col + 0 - 1] * filterArray[6] );
                acc += (input -> color[plane][row + 2 - 1][col + 1 - 1] * filterArray[7] );
                acc += (input -> color[plane][row + 2 - 1][col + 2 - 1] * filterArray[8] );
                
                acc = acc * div; //computer better at multiplication than division
                
                if ( acc < 0 ) {
                    acc = 0;
                }
                if ( acc > 255 ) { 
                    acc = 255;
                }
                
                output -> color[plane][row][col] = acc;
            }
        }
    }
    cycStop = rdtscll();
    double diff = cycStop - cycStart;
    double diffPerPixel = diff / (output -> width * output -> height);
    fprintf(stderr, "Took %f cycles to process, or %f cycles per pixel\n",diff, diffPerPixel);
    return diffPerPixel;
}
