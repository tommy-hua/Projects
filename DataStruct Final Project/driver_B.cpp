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

//same thing as driver A, just specific to data set B

void fillArray(string fileName, int arr[]){
    ifstream myfile(fileName);
    string line;
    int index = 0;

    while(getline(myfile, line, ',')){
        arr[index] = stoi(line);
        index++;
    }
}

int random(int n){
    //srand(time(NULL));
    return rand() % n;
}

void link(int testData[40000], float insert[400], float search[400]){
    LL ll;
    int i = 0;
    int max = 100;
    int index = 0;

    while(index < 400){
        auto start = high_resolution_clock::now();

        for(i;i<max;i++){
            ll.insert(testData[i]);
        }

        auto end = high_resolution_clock::now();

        auto execTime = duration_cast<nanoseconds>(end - start).count();

        insert[index] = execTime/100;

        auto start2 = high_resolution_clock::now();

        for(int i=0;i<100;i++){
            int n = random(max);
            ll.search(testData[n]);
            
        }

        auto end2 = high_resolution_clock::now();

        auto execTime2 = duration_cast<nanoseconds>(end2 - start2).count();

        search[index] = execTime2/100;

        max += 100;
        index++;
    }    
}

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
    HashTable ht(40009);
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

void hashLine(int testData[40000], float insert[400], float search[400], int colInsert[400], int colSearch[400]){
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
        colInsert[index] = ht.getNumOfCollision();

        auto start2 = high_resolution_clock::now();

        for(int i=0;i<100;i++){
            int n = random(max);
            ht.searchLine(testData[n]);
        }

        auto end2 = high_resolution_clock::now();

        auto execTime2 = duration_cast<nanoseconds>(end2 - start2).count();

        search[index] = execTime2/100;
        colSearch[index] = ht.getNumOfCollision();

        max += 100;
        index++;
    }    
}

void hashQuad(int testData[40000], float insert[400], float search[400], int colInsert[400], int colSearch[400]){
    HashTable ht(40009);
    int i = 0;
    int max = 100;
    int index = 0;
    
    while(index < 400){
        
        auto start = high_resolution_clock::now();

        for(i;i<max;i++){
            ht.insertQuad(testData[i]);
        }
        

        auto end = high_resolution_clock::now();

        auto execTime = duration_cast<nanoseconds>(end - start).count();

        insert[index] = execTime/100;
        colInsert[index] = ht.getNumOfCollision();
        

        auto start2 = high_resolution_clock::now();

        for(int i=0;i<100;i++){
            int n = random(max);
            ht.searchQuad(testData[n]);
        }

        auto end2 = high_resolution_clock::now();

        auto execTime2 = duration_cast<nanoseconds>(end2 - start2).count();

        search[index] = execTime2/100;
        colSearch[index] = ht.getNumOfCollision();
        
        max += 100;
        index++;
    }    

}

int main(int argc, char* argv[]){ //this main specific to Data Set B
    
    int testData[40000];
    float insert[400];
    float search[400];
    int colInsert[400];
    int colSearch[400];
    
    fillArray(argv[1], testData);

    int i = 0;
    string fileName;
    int t = 0;
    while(i != 6){
        cout << "LL(1), BST(2), chain(3), line(4), quad(5), or compile and quit(6)" << endl;
        string input;
        getline(cin, input);
        i = stoi(input);
        
        switch(i){
            case 1:{
                link(testData, insert, search);
                fileName = "LL_B.csv";
                break;
            }
            case 2:{
                bst(testData, insert, search);
                fileName = "BST_B.csv";
                break;
            }
            case 3:{
                hashChain(testData, insert, search);
                fileName = "HashTableChain_B.csv";
                break;
            }
            case 4:{
                hashLine(testData, insert, search, colInsert, colSearch);
                fileName = "HashTableLine_B.csv";
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
            case 5:{
                hashQuad(testData, insert, search, colInsert, colSearch);
                fileName = "HashTableQuad_B.csv";
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
 //g++ -std=c++11 -g driver.cpp -o main