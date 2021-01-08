#include <iostream>
#include <string>
using namespace std;

struct node
{
    int key;
    struct node* next;
};

class HashTable
{
private:
    int tableSize;  // No. of buckets (linked lists)
   
    node* *table;  // Pointer to an array containing buckets

    int numOfcolision;

    node* createNode(int key, node* next){
        node* newNode = new node;
        newNode->key = key;
        newNode->next = next;
        return newNode;
    }

public:
    HashTable(int bsize){ // Constructor
        tableSize = bsize;
        table = new node* [tableSize];
    }  

    // inserts a key into hash table w/ chaining
    bool insertChain(int key);

    //insert with linear probing
    bool insertLine(int key);

    //insert with quadratic probing
    bool insertQuad(int key);

    // hash function to map values to key
    unsigned int hashFunction(int key);

    void printTable();

    int getNumOfCollision();

    //search for linear probing
    node* searchLine(int key);

    //search for chaining
    node* searchChain(int key);

    //search for quadratic probing
    node* searchQuad(int key);
};

unsigned int HashTable::hashFunction(int key){ //hash function that gives index for table
    return (key % tableSize); 
}

bool HashTable::insertChain(int key){ 
    unsigned int index = hashFunction(key); //finds index
    node* ptr = createNode(key, NULL); //creates node
    ptr -> next = table[index]; //put node at head of table at that index linked list
    table[index] = ptr;
    return true; //return true for succesful insertion
}

bool HashTable::insertLine(int key){
    unsigned int index = hashFunction(key); //finds index 
    int i = 0; //counter for number of collisions
    while(table[index] != NULL){ //if the table at that index is already filled use linear probing
        index = hashFunction(index + 1); //linear probing formula for new index
        if(index >= tableSize){ //if index reaches end of the table go back to the beginning and keep searching 
            index = 0;
        } 
        //everytime function goes through while loop is another collision
        i++; //increase counter for number of collisons
    }
    table[index] = createNode(key, NULL); //exits while loop only when empty spot on table is found
    numOfcolision = i; //update number of collisions
    return true;

}

bool HashTable::insertQuad(int key){ 
    unsigned int index = hashFunction(key); //find index
    int i = 0; //counter for number of collisions
    while(table[index] != NULL){
        index = hashFunction(index + (i*i)); //quadratic probing formula
        if(index >= tableSize){ //go back to beginning of table if end is reached
            index = 0;
        }
        i++;
    }
    table[index] = createNode(key, NULL); //exit when empty spot is found and add a new node there
    numOfcolision = i; 
    return true;

}

node* HashTable::searchLine(int key){ //search for linear probing
    int count = 0;
    unsigned int index = hashFunction(key); //find index for specific key
    while(table[index]->key != key){ //follow algorithim of linear probing 
        index = hashFunction(index + 1); 
        if(index >= tableSize){
            index = 0;
        }
        count++;
    }
    numOfcolision = count; //update search collisions
    return table[index]; //return found node
}


node* HashTable::searchChain(int key){ //search for chaining
    unsigned int index = hashFunction(key); //find index
    node* ptr = table[index];
    while(ptr != NULL && ptr -> key != key){ //search through index's linked list 
        ptr = ptr -> next;
    }
    return ptr; //return found node
}

node* HashTable::searchQuad(int key){ //search for quadratic probing
    int i = 0;
    unsigned int index = hashFunction(key); //find index
    while(table[index]->key != key){ //follow quadratic probing algorithim but exit when key is found
        index = hashFunction(index + (i*i)); 
        if(index >= tableSize){
            index = 0;
        }
        i++;
    }
    numOfcolision = i; //update search collisions
    return table[index];
}

void HashTable::printTable(){ //display the table
    for(int i=0;i<tableSize;i++){ //display each table index
        node* tmp = table[i];
        cout << i << ":";
        while(tmp != NULL){ //if table index has linked list print the nodes in it
            cout << " -> " << tmp->key;
            tmp = tmp -> next;
        }
        cout << endl;
    }
}

int HashTable::getNumOfCollision(){ //number of collisions getter
    return numOfcolision;
}

/* //testing main
int main(){
    HashTable ht(5);
    ht.insertChain(27);
    ht.insertChain(10);
    ht.insertChain(11);
    ht.insertChain(21);
    
    ht.insertChain(29);
    ht.insertChain(23);
    ht.printTable();
    node* n = ht.searchChain(29);
    cout << "ffl " << n->key << endl;
    //cout << ht.getNumOfCollision() << endl;
}
*/