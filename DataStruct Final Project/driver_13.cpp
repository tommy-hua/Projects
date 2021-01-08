#include <iostream>
#include <fstream>

using namespace std;

//this driver is used to get values from data sets

void fillArray(string fileName, int arr[]){ //fill testData array
    ifstream myfile(fileName);
    string line;
    int index = 0;

    while(getline(myfile, line, ',')){
        arr[index] = stoi(line);
        index++;
    }
}

int main(int argc, char* argv[]){
    int testDataA[40000]; //two data set arrays one for each data set
    int testDataB[40000];
    
    fillArray(argv[1], testDataA); //fill both data set arrays
    fillArray(argv[2], testDataB);

    ofstream myfile("DataSet_Summary.csv"); //write to output file 

    int count = 0; //index counter
    for(int i=0;i<40000;i+=100){ //takes every other 100th value
        
        myfile << count << "," << testDataA[i] << "," << testDataB[i] << endl; //write to file
        count++; //update index counter
    }
    myfile.close();
    
}