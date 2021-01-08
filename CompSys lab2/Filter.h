//-*-c++-*-
#ifndef _Filter_h_
#define _Filter_h_

using namespace std;

class Filter {
    
public: //make everything public and change data types to reduce memory overhead
    short divisor;
    short dim;
    short *data;
    Filter(short _dim);
    short get(short r, short c);
    void set(short r, short c, short value);
    short getDivisor();
    void setDivisor(short value);
    short getSize();
    void info();
    
};

#endif
