#include <iostream>

using namespace std;

struct Node{ //node struct for linked list
    int key;
    Node* next;
};

class LL{
    private:
        Node* head;
    public:
        LL();
        ~LL();
        void insert(int key);
        Node* search(int key);
        void deleteNode(int key);
        void display();
};

LL::LL(){ //constructor
    head = NULL;
}

LL::~LL(){ //destructor
    while(head != NULL){
        Node* tmp = head;
        head = tmp -> next;
        delete tmp;
    }
}

void LL::insert(int key){ //insert every node at head of linked list
    Node* newNode = new Node;
    newNode -> key = key;
    newNode -> next = head;
    head = newNode; 
}

Node* LL::search(int key){ //search through linked list
    Node* tmp = head;
    while(tmp != NULL && tmp -> key != key){
        tmp = tmp -> next;
    }
    return tmp; //return pointer to node 
}

void LL::deleteNode(int key){ //delete node, didn't really need this
    Node* tmp = head;
    Node* prev = new Node;
    while(tmp != NULL && tmp -> key != key){
        prev = tmp; //move along previous node to use to redirect pointers
        tmp = tmp -> next;
    }
    prev -> next = tmp -> next; //connect over node to be deleted
    delete tmp; //delete node
}

void LL::display(){ //displays linked list
    Node* tmp = head; 
    while(tmp -> next != NULL){ //print from head to second to last node
        cout << tmp -> key << " -> ";
        tmp = tmp -> next;
    }
    cout << tmp -> key << endl; //print last node at end so no extra arrow at the end
}
/* main for testing
int main(){
    LL l;
    l.insert(NULL, 1);
    l.insert(l.search(1), 2);
    l.insert(l.search(2), 3);
    l.display();
    l.deleteNode(2);
    l.display();
}
*/