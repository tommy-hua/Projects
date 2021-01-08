#include <iostream>
using namespace std;
#define COUNT 5

struct BSTNode{ //Bst node struct
    int key;
    BSTNode* left;
    BSTNode* right;
};

class BST{ //class for BST
    private:
        BSTNode* root;

    public:
        BST();
        ~BST();
        void insert(int key);
        BSTNode* search(int key);
        void display(int space);
};

BST::BST(){ //constructor
    root = NULL;
}

void destroy(BSTNode* node){ //deconstructor helper
    if(node != NULL){
        destroy(node -> left);
        destroy(node -> right);
        delete node;
        node = NULL;
    }
}

BST::~BST(){ //deconstructoy
    destroy(root);
}

BSTNode* createNode(int key){ //helper for creating a node
    BSTNode* newNode = new BSTNode;
    newNode -> key = key;
    newNode -> left = NULL;
    newNode -> right = NULL;
    return newNode;
}

BSTNode* add(BSTNode* currNode, int data) //helper for the insert, does not need to check every node in tree b/c of the BST format
{
    if(currNode == NULL){
        return createNode(data); //returns when recursion hits a leaf at the right position
    }
    else if(currNode->key < data){ //goes to the right if node->key to be inserted is bigger than the root
        currNode->right = add(currNode->right,data); //checks node to the right recursively
    }
    else if(currNode->key > data){ //goes left if node->key is smaller than root
        currNode->left = add(currNode->left,data); //checks the node to the left and compares keys 
    }
    return currNode;

}

void BST::insert(int key){
    root = add(root, key); //adds new node to the tree
}   

BSTNode* searchHelper(BSTNode* node, int key){ //searching helper, works similar to add
    if(node == NULL) //if node hits leaf return
        return NULL;

    if(node->key == key) //if node that is being searched for is found return that node
        return node;

    if(node->key > key) //go left if root/current node that it is at is bigger
        return searchHelper(node->left, key);

    return searchHelper(node->right, key); //go right if root/current node that it is at is not the case of being bigger
}

BSTNode* BST::search(int key){ //search function, uses search helper
    return searchHelper(root, key);
}

void print2D(BSTNode *root, int space)  //display function helper
{  
    // Base case  
    if (root == NULL)  
        return;  
  
    // Increase distance between levels  
    space += COUNT;  
  
    // Process right child first  
    print2D(root->right, space);  
  
    // Print current node after space  
    // count  
    cout<<endl;  
    for (int i = COUNT; i < space; i++)  
        cout << " ";  
    cout << root->key << "\n";  
  
    // Process left child  
    print2D(root->left, space);  
}  

void BST::display(int space){ //display
    print2D(root, space);
}
/* //main for testing
int main(){
    BST tree;
    tree.insert(5);
    tree.insert(3);
    tree.insert(4);
    tree.insert(7);
    tree.insert(10);
    tree.insert(2);
    //tree.insert(3);
    tree.display(0);
    BSTNode* node = tree.search(2);
    cout << node->key << endl;
}
*/