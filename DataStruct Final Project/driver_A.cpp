#include <iostream>
#include <fstream>
#include <chrono>
#include <ctime>
//#include <array>
#include "BST.cpp"
#include "LL.cpp"
#include "hash.cpp"
using namespace std::chrono;
using namespace std;

void fillArray(string fileName, int arr[]){ //function to fill test data array
    ifstream myfile(fileName); //take file
    string line;
    int index = 0;

    while(getline(myfile, line, ',')){ //split up file at delimiter comma
        arr[index] = stoi(line); //insert each number into a index of array
        index++; //go to next empty index
    }
}

int random(int n){ //function to find random numbers within a given range
    //srand(time(NULL));
    return rand() % n;
}

void link(int testData[40000], float insert[400], float search[400]){ //function to find data for linked list
    LL ll; //declare class
    int i = 0; //keeps trach of test data index, moving 100 at a time
    int max = 100; //cap for test Data index, moves a 100 at a time
    int index = 0; //index for insert and search arrays

    while(index < 400){ //while the insert and search arrays are not full
        auto start = high_resolution_clock::now(); //start timer for insert function into Linked List

        for(i;i<max;i++){ //take 100 values from the testData and insert them into the linked list from i to next 100 values in testData array
            ll.insert(testData[i]);
        }

        auto end = high_resolution_clock::now(); //end timer

        auto execTime = duration_cast<nanoseconds>(end - start).count(); //calculate time it took in nanosecondes

        insert[index] = execTime/100; //divide by a hundred to find average of the 100 times and insert into insert array

        auto start2 = high_resolution_clock::now(); //start second timer for search functions

        for(int i=0;i<100;i++){ //only runs 100 times
            int n = random(max); //find random number between 0 and current max value
            ll.search(testData[n]); //search function for testData at that random index 
            
        }

        auto end2 = high_resolution_clock::now(); //end timer

        auto execTime2 = duration_cast<nanoseconds>(end2 - start2).count(); //find second time in nanoseconds for search times

        search[index] = execTime2/100; //insert average search time into search array

        max += 100; //update max value
        index++; //update index to next empty space in search and insert index
    }    
}

//repeat algorithim for rest of the data structures
void bst(int testData[40000], float insert[400], float search[400]){
    BST bst;
    int i = 0;
    int max = 100;
    int index = 0;

    while(index < 400){
        auto start = high_resolution_clock::now();

        for(i;i<max;i++){
            bst.insert(testData[i]);
        }

        auto end = high_resolution_clock::now();

        auto execTime = duration_cast<nanoseconds>(end - start).count();

        insert[index] = execTime/100;

        auto start2 = high_resolution_clock::now();

        for(int i=0;i<100;i++){
            int n = random(max);
            bst.search(testData[n]);
        }

        auto end2 = high_resolution_clock::now();

        auto execTime2 = duration_cast<nanoseconds>(end2 - start2).count();

        search[index] = execTime2/100;

        max += 100;
        index++;
    }    
}

void hashChain(int testData[40000], float insert[400], float search[400]){
    HashTable ht(40009); //table of 40009 indexes
    int i = 0;
    int max = 100;
    int index = 0;

    while(index < 400){
        auto start = high_resolution_clock::now();

        for(i;i<max;i++){
            ht.insertChain(testData[i]);
        }

        auto end = high_resolution_clock::now();

        auto execTime = duration_cast<nanoseconds>(end - start).count();

        insert[index] = execTime/100;

        auto start2 = high_resolution_clock::now();

        for(int i=0;i<100;i++){
            int n = random(max);
            ht.searchChain(testData[n]);
        }

        auto end2 = high_resolution_clock::now();

        auto execTime2 = duration_cast<nanoseconds>(end2 - start2).count();

        search[index] = execTime2/100;

        max += 100;
        index++;
    }    
}

void hashLine(int testData[40000], float insert[400], float search[400], int colInsert[400], int colSearch[400]){ //new arrays for number of insert and search collisions
    HashTable ht(40009);
    int i = 0;
    int max = 100;
    int index = 0;

    while(index < 400){
        auto start = high_resolution_clock::now();

        for(i;i<max;i++){
            ht.insertLine(testData[i]);
        }

        auto end = high_resolution_clock::now();

        auto execTime = duration_cast<nanoseconds>(end - start).count();

        insert[index] = execTime/100;
        colInsert[index] = ht.getNumOfCollision(); //insert number of collisions into insert collision array

        auto start2 = high_resolution_clock::now();

        for(int i=0;i<100;i++){
            int n = random(max);
            ht.searchLine(testData[n]);
        }

        auto end2 = high_resolution_clock::now();

        auto execTime2 = duration_cast<nanoseconds>(end2 - start2).count();

        search[index] = execTime2/100;
        colSearch[index] = ht.getNumOfCollision(); //insert number of collisions into search collisions array

        max += 100;
        index++;
    }    
}

void hashQuad(int testData[40000], float insert[400], float search[400], int colInsert[400], int colSearch[400]){
    HashTable ht(40009);
    int i = 0;
    int max = 100;
    int index = 0;
    //int c = 0;
    while(index < 400){
        //ht.resetNumCol();
        auto start = high_resolution_clock::now();

        for(i;i<max;i++){
            ht.insertQuad(testData[i]);
        }

        auto end = high_resolution_clock::now();

        auto execTime = duration_cast<nanoseconds>(end - start).count();

        insert[index] = execTime/100;
        colInsert[index] = ht.getNumOfCollision(); //insert number of collisions into insert collision array

        auto start2 = high_resolution_clock::now();

        for(int i=0;i<100;i++){
            int n = random(max);
            ht.searchQuad(testData[n]);
        }

        auto end2 = high_resolution_clock::now();

        auto execTime2 = duration_cast<nanoseconds>(end2 - start2).count();

        search[index] = execTime2/100;
        colSearch[index] = ht.getNumOfCollision(); //insert number of collisions into search collisions array
        
        max += 100;
        index++;
    }    

}

int main(int argc, char* argv[]){ //this main specific to DataSet A
    
    int testData[40000]; //initialize needed arrays
    float insert[400];
    float search[400];
    int colInsert[400];
    int colSearch[400];
    
    fillArray(argv[1], testData); //call function to fill testData array

    int i = 0; //deicision variable
    string fileName; //variable for output file name
    int t = 0;  //variable to distinguish writing to output files with collision values
    while(i != 6){
        cout << "LL(1), BST(2), chain(3), line(4), quad(5), or compile and quit(6)" << endl; //ask what data structure to be used
        string input;
        getline(cin, input);
        i = stoi(input);
        
        switch(i){
            case 1:{
                link(testData, insert, search); //run data structure test
                fileName = "LL_A.csv"; //change file name to ouput file name specific to data structure
                break;
            }
            case 2:{
                bst(testData, insert, search);
                fileName = "BST_A.csv";
                break;
            }
            case 3:{
                hashChain(testData, insert, search);
                fileName = "HashTableChain_A.csv";
                break;
            }
            case 4:{
                hashLine(testData, insert, search, colInsert, colSearch); //linear probing and quadratic probing are only data structures with collisions
                fileName = "HashTableLine_A.csv";
                //seperate output function for output files with different format
                /*
                ofstream myfile(fileName); 
                for(int i=0;i<400;i++){
                    myfile << i << "," << insert[i] << "," << search[i] << "," << colInsert[i] << "," << colSearch[i] << endl;
                }
                myfile.close();
                */
                t++; //add to t variable to make sure output function is not run twice on same data structure
                break;
            }
            case 5:{
                hashQuad(testData, insert, search, colInsert, colSearch); //same for quadratic probing
                fileName = "HashTableQuad_A.csv";
                /*
                ofstream myfile(fileName);
                for(int i=0;i<400;i++){
                    myfile << i << "," << insert[i] << "," << search[i] << "," << colInsert[i] << "," << colSearch[i] << endl;
                }
                myfile.close();
                */
                t++;
                break;
            }
            case 6:{
                cout << "quit" << endl;
                break;
            }
        }
    }
    if(t == 0){
        ofstream myfile(fileName);
        for(int i=0;i<400;i++){
            myfile << i << "," << insert[i] << "," << search[i] << endl;
        }
        myfile.close();
    }else{
        ofstream myfile(fileName);
        for(int i=0;i<400;i++){
            myfile << i << "," << insert[i] << "," << search[i] << "," << colInsert[i] << "," << colSearch[i] << endl;
        }
        myfile.close();
    }  
}
//same exact thing for driver B


 //g++ -std=c++11 -g driver.cpp -o main