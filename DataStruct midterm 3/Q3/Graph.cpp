#include "Graph.hpp"
#include <vector>
#include <queue>
#include <iostream>
#include <queue>


using namespace std;

void Graph::addEdge(string source, string target){
    for(unsigned int i = 0; i < vertices.size(); i++){
        if(vertices[i]->name == source){
            for(unsigned int j = 0; j < vertices.size(); j++){
                if(vertices[j]->name == target && i != j){
                    adjVertex av;
                    av.v = vertices[j];
                    vertices[i]->adj.push_back(av);
                }
            }
        }
    }
}

void Graph::addVertex(string vName){
    bool found = false;
    for(unsigned int i = 0; i < vertices.size(); i++){
        if(vertices[i]->name == vName){
            found = true;
            cout<<vertices[i]->name<<" found."<<endl;
        }
    }
    if(found == false){
        vertex * v = new vertex;
        v->name = vName;
        vertices.push_back(v);
    }
}

void Graph::display(){
    cout<<"vertex"<<":"<<"color"<<endl;
    for(unsigned int i = 0; i < vertices.size(); i++){
        cout<<vertices[i]->name<<":"<<vertices[i]->color<<endl;

    }
}

void Graph::color(string source){
//TODO
    vertex* start = new vertex; 
    for(int i=0;i<vertices.size();i++){ //initially set all vertices to unvisited
        vertices[i]->visited = false;
        vertices[i]->color = "white"; //set all vertices to the color white
        if(vertices[i]->name == source){
            start = vertices[i]; //find the starting vertex
        }
    }
    start->visited = true; //set the starting vertex to visited
    start->color = "black"; //set it to the color black

    queue<vertex*>q;
    q.push(start); //push the starting vertex onto the queue

    vertex* n;

    while(!q.empty()){
        n = q.front(); 
        q.pop(); //pop the starting vertex and queue its adjacent vertexes
        for(int j=0;j<n->adj.size();j++){
            if(n -> adj[j].v->visited == false){
                n->adj[j].v->visited = true;
                q.push(n->adj[j].v);
                n->adj[j].v->distance = 1 + n->distance; //update the distance of every vertex from starting vertex
                if(n->adj[j].v->distance % 2 == 0){ //if it is an even distance away make it black
                    n->adj[j].v->color = "black";
                }else{
                    n->adj[j].v->color = "red"; //if it is an odd distance away make it red
                }
            }
        }
    }
}
