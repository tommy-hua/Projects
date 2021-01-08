/* 
 * CS:APP Data Lab 
 * 
 * <Please put your name and userid here>
 * 
 * bits.c - Source file with your solutions to the Lab.
 *          This is the file you will hand in to your instructor.
 *
 * WARNING: Do not include the <stdio.h> header; it confuses the dlc
 * compiler. You can still use printf for debugging without including
 * <stdio.h>, although you might get a compiler warning. In general,
 * it's not good practice to ignore compiler warnings, but in this
 * case it's OK.  
 */

#if 0
/*
 * Instructions to Students:
 *
 * STEP 1: Read the following instructions carefully.
 */

You will provide your solution to the Data Lab by
editing the collection of functions in this source file.

INTEGER CODING RULES:
 
  Replace the "return" statement in each function with one
  or more lines of C code that implements the function. Your code 
  must conform to the following style:
 
  int Funct(arg1, arg2, ...) {
      /* brief description of how your implementation works */
      int var1 = Expr1;
      ...
      int varM = ExprM;

      varJ = ExprJ;
      ...
      varN = ExprN;
      return ExprR;
  }

  Each "Expr" is an expression using ONLY the following:
  1. Integer constants 0 through 255 (0xFF), inclusive. You are
      not allowed to use big constants such as 0xffffffff.
  2. Function arguments and local variables (no global variables).
  3. Unary integer operations ! ~
  4. Binary integer operations & ^ | + << >>
    
  Some of the problems restrict the set of allowed operators even further.
  Each "Expr" may consist of multiple operators. You are not restricted to
  one operator per line.

  You are expressly forbidden to:
  1. Use any control constructs such as if, do, while, for, switch, etc.
  2. Define or use any macros.
  3. Define any additional functions in this file.
  4. Call any functions.
  5. Use any other operations, such as &&, ||, -, or ?:
  6. Use any form of casting.
  7. Use any data type other than int.  This implies that you
     cannot use arrays, structs, or unions.

 
  You may assume that your machine:
  1. Uses 2s complement, 32-bit representations of integers.
  2. Performs right shifts arithmetically.
  3. Has unpredictable behavior when shifting an integer by more
     than the word size.

EXAMPLES OF ACCEPTABLE CODING STYLE:
  /*
   * pow2plus1 - returns 2^x + 1, where 0 <= x <= 31
   */
  int pow2plus1(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     return (1 << x) + 1;
  }

  /*
   * pow2plus4 - returns 2^x + 4, where 0 <= x <= 31
   */
  int pow2plus4(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     int result = (1 << x);
     result += 4;
     return result;
  }

FLOATING POINT CODING RULES

For the problems that require you to implent floating-point operations,
the coding rules are less strict.  You are allowed to use looping and
conditional control.  You are allowed to use both ints and unsigneds.
You can use arbitrary integer and unsigned constants.

You are expressly forbidden to:
  1. Define or use any macros.
  2. Define any additional functions in this file.
  3. Call any functions.
  4. Use any form of casting.
  5. Use any data type other than int or unsigned.  This means that you
     cannot use arrays, structs, or unions.
  6. Use any floating point data types, operations, or constants.


NOTES:
  1. Use the dlc (data lab checker) compiler (described in the handout) to 
     check the legality of your solutions.
  2. Each function has a maximum number of operators (! ~ & ^ | + << >>)
     that you are allowed to use for your implementation of the function. 
     The max operator count is checked by dlc. Note that '=' is not 
     counted; you may use as many of these as you want without penalty.
  3. Use the btest test harness to check your functions for correctness.
  4. Use the BDD checker to formally verify your functions
  5. The maximum number of ops for each function is given in the
     header comment for each function. If there are any inconsistencies 
     between the maximum ops in the writeup and in this file, consider
     this file the authoritative source.

/*
 * STEP 2: Modify the following functions according the coding rules.
 * 
 *   IMPORTANT. TO AVOID GRADING SURPRISES:
 *   1. Use the dlc compiler to check that your solutions conform
 *      to the coding rules.
 *   2. Use the BDD checker to formally verify that your solutions produce 
 *      the correct answers.
 */


#endif
         
/* 
 * bitNor - ~(x|y) using only ~ and & 
 *   Example: bitNor(0x6, 0x5) = 0xFFFFFFF8
 *   Legal ops: ~ &
 *   Max ops: 8
 *   Rating: 1
 */
int bitNor(int x, int y) {
//application of DeMorgan's Law         
  return (~x & ~y);
}
/* 
 * fitsShort - return 1 if x can be represented as a 
 *   16-bit, two's complement integer.
 *   Examples: fitsShort(33000) = 0, fitsShort(-32768) = 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 8
 *   Rating: 1
 */
int fitsShort(int x) {
    /*shift x left 16 bits to the left to get rid of any bits that do not fit into 
    *LS 16 bits, which is what we are seeing if it fits into. We shift it back right and then XOR with og x
    *and if it returns anything other than 0 that means that there is a difference in the MS 16 bits, which means that 
    *x did not originally fit into 16 bits. 
    */
    return !(((x<<16)>>16)^x);
}
/* 
 * thirdBits - return word with every third bit (starting from the LSB) set to 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 8
 *   Rating: 1
 */
int thirdBits(void) {
    /*i wrote out 32 0 and then i changed every third bit to 1 and then i broke that up into 8 bits and 
    *then i started with the left most 8 which was decimal 73 by itself and then i shifted it left 8 and then
    *i added then next 8 bits so on and so forth
    */
    return (((((73 << 8) + 36) << 8) + 146) << 8) + 73;
}
/* 
 * anyEvenBit - return 1 if any even-numbered bit in word set to 1
 *   Examples anyEvenBit(0xA) = 0, anyEvenBit(0xE) = 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 2
 */
int anyEvenBit(int x) {
    //i am assuming that the first bit is 0 position.
    /*hexa 55 is 0101. shift that over 8 and then add another 55 until 32 bit mask with even bits as 1. compare with and to x
    *so if there is a 1 in an even bit it will return a value greater than 1, ! that so it becomes single bit 0, then ! again to return 1.
    */
    int mask = ((((((0x55<<8)+0x55)<<8)+0x55)<<8)+0x55);
    return !!(x&mask);
}
/* 
 * copyLSB - set all bits of result to least significant bit of x
 *   Example: copyLSB(5) = 0xFFFFFFFF, copyLSB(6) = 0x00000000
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 5
 *   Rating: 2
 */
int copyLSB(int x) {
    /*isolate LSB of x by shifting to left 31 bits, so MSB is no lSB of x and the rest is 0
    *right shift back 31 and since is arithmetic the MSB of x is now the other 31
    */
    return (x << 31) >>31;
}
/* 
 * implication - return x -> y in propositional logic - 0 for false, 1
 * for true
 *   Example: implication(1,1) = 1
 *            implication(1,0) = 0
 *   Legal ops: ! ~ ^ |
 *   Max ops: 5
 *   Rating: 2
 */
int implication(int x, int y) {
    /*logical equivalent of x -> y is !x | y*/
    return !x | y;
}
/* 
 * bitMask - Generate a mask consisting of all 1's 
 *   lowbit and highbit
 *   Examples: bitMask(5,3) = 0x38
 *   Assume 0 <= lowbit <= 31, and 0 <= highbit <= 31
 *   If lowbit > highbit, then mask should be all 0's
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 16
 *   Rating: 3
 */
int bitMask(int highbit, int lowbit) {
    /*x is a mask of 1s from lowbit up
    *y is a mask of 1s from high bit up plus 1 b/c must include highbit
    *XOR x and y bc the 1s from from y will make the 1s on x above highbit 0s
    *and then check is making sure that lowbit is not greater than highbit 
    *it adds 2s complement of lowbit to highbit bc that is the same as subtracting lowbit
    *and then shift those right 31. if the number is negative than MSB will be 1 and then arithmetic will 
    *make them all 1 and then flip to 0 so that in & it is a false which does not complete &
    */
    int x = ((1 << 31) >> 31) << lowbit;
    int y = (((1 << 31) >> 31) << (highbit) << 1);
    int check = ~((highbit + (~lowbit+1)) >> 31);
    return check & (x^y);
}
/*
 * ezThreeFourths - multiplies by 3/4 rounding toward 0,
 *   Should exactly duplicate effect of C expression (x*3/4),
 *   including overflow behavior.
 *   Examples: ezThreeFourths(11) = 8
 *             ezThreeFourths(-9) = -6
 *             ezThreeFourths(1073741824) = -268435456 (overflow)
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 3
 */
int ezThreeFourths(int x) {
    /*first i multiply x by 4 then subtract one x to get 3x
    *when dividing negative numbers you run into a problem bc the computer wants to round down towards negative infinity but we want to round towards 0
    *for example -27 divided by 4 produces -7 instead of -6 so to combat that we add 1 when necessary
    *to find if addition by 1 is needed, shift x right by 31 to check if its negative and & it with 3 or 0011 to look at last two digits of x which are the remainder when
    *divinding by 4 and if there is a remainder in x than it will return 1 and if it is negative it will also return one and then double ! to make it 1 bit 
    *now time for actual division, shift x right by 2 and then add a, either 1 or 0
    */
    int n = x;
    int a;
    x = (x << 2) + (~n + 1);  
    a = !!((x >> 31) & (0x3 & x));
    x = (x >> 2) + a;
    return x;
}
/*
 * satMul3 - multiplies by 3, saturating to Tmin or Tmax if overflow
 *  Examples: satMul3(0x10000000) = 0x30000000
 *            satMul3(0x30000000) = 0x7FFFFFFF (Saturate to TMax)
 *            satMul3(0x70000000) = 0x7FFFFFFF (Saturate to TMax)
 *            satMul3(0xD0000000) = 0x80000000 (Saturate to TMin)
 *            satMul3(0xA0000000) = 0x80000000 (Saturate to TMin)
 *  Legal ops: ! ~ & ^ | + << >>
 *  Max ops: 25
 *  Rating: 3
 */
int satMul3(int x) {
    /*can't just multiply by 3 bc possible to encounter overflow at multipy by 2 and 3
    *so split it up into 2x and 3x and check for overflow for both by comparing with og x and if there is a sign change 
    * then create a mask out of that. for example if sign change then created will be all 1s else all 0
    *y is creating tMin or tMax based off whether x was positive or negative bc if x was positive and overflowed it will
    *create tMax else it will create tMin
    *return statement is an if else, if it did not overflow, return z which is just 3x, else return y which is either tMax or tMin
    */
    int twoX = x << 1;
    int z = twoX + x;
    int c = ((twoX^x) | (z^x)) >> 31;
    int y = (~(1 << 31)^(x >> 31));
    return (~c & z) | (c & y);
}
/*
 * bitParity - returns 1 if x contains an odd number of 0's
 *   Examples: bitParity(5) = 0, bitParity(7) = 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 20
 *   Rating: 4
 */
int bitParity(int x) {
    /*you take the 32 bit x and XOR the first half with the second half
    *by shifting x to the right by 16 or half. keep doing this until down to comparing
    *one bit to another bit. Because 32 is an even number, if there is an odd number of 1s there is an 
    *odd number of 0s, and by XOR each half you are able to weed out any extra ones. & x by 1 tells you
    *whether the last number left is a 1 or a 0
    */
    x = x^(x >> 16);
    x = x^(x >> 8);
    x = x^(x >> 4);
    x = x^(x >> 2);
    x = x^(x >> 1);
    return x & 0x1;
}
/*
 * ilog2 - return floor(log base 2 of x), where x > 0
 *   Example: ilog2(16) = 4
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 90
 *   Rating: 4
 */
int ilog2(int x) {
    /*finding the leftmost bit, first check the upper half/16
    *create mask out of upper half then & with 16 bc if there is a 1
    *in upper half it is going to be at least 2^16. If mask produced 1s
    *add 16 (which is the index) to log and then shift x over by 16 and then check the upper half again 
    *else keep x the same and then add 8 or half more. keep doing this until last bit
    */
    int x1, x2, x3, x4, x5;
    int shift;
    int log;
    
    x1 = x >> 16;
    shift = 0x10 & (((!!x1) << 31) >> 31);
    log = shift;
    x = x >> shift;
    
    x2 = x >> 8;
    shift = 0x8 & (((!!x2) << 31) >> 31);
    log += shift;
    x = x >> shift;
    
    x3 = x >> 4;
    shift = 0x4 & (((!!x3) << 31) >> 31);
    log += shift;
    x = x >> shift;
    
    x4 = x >> 2;
    shift = 0x2 & (((!!x4) << 31) >> 31);
    log += shift;
    x = x >> shift;
    
    x5 = x >> 1;
    shift = 0x1 & (((!!x5) << 31) >> 31);
    log += shift;
    
    return log;
}
/*
 * trueThreeFourths - multiplies by 3/4 rounding toward 0,
 *   avoiding errors due to overflow
 *   Examples: trueThreeFourths(11) = 8
 *             trueThreeFourths(-9) = -6
 *             trueThreeFourths(1073741824) = 805306368 (no overflow)
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 20
 *   Rating: 4
 */
int trueThreeFourths(int x)
{
    /*
    *divide x by 4 then get remainder by & x with three, isolating last two bits
    *multiply y by three by multiplying two and then adding one y
    *3r/4 used to round to 0, also add 1 depending on whether x is negative
    */
    int y = (x >> 2);
    int r = x & 3;
    return y + (y << 1) + (r + (r << 1) + (x >> 31 & 3) >> 2);
}
/*
 * Extra credit
 */
/* 
 * float_neg - Return bit-level equivalent of expression -f for
 *   floating point argument f.
 *   Both the argument and result are passed as unsigned int's, but
 *   they are to be interpreted as the bit-level representations of
 *   single-precision floating point values.
 *   When argument is NaN, return argument.
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 10
 *   Rating: 2
 */
unsigned float_neg(unsigned uf) {
 return 2;
}
/* 
 * float_i2f - Return bit-level equivalent of expression (float) x
 *   Result is returned as unsigned int, but
 *   it is to be interpreted as the bit-level representation of a
 *   single-precision floating point values.
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 30
 *   Rating: 4
 */
unsigned float_i2f(int x) {
  return 2;
}
/* 
 * float_twice - Return bit-level equivalent of expression 2*f for
 *   floating point argument f.
 *   Both the argument and result are passed as unsigned int's, but
 *   they are to be interpreted as the bit-level representation of
 *   single-precision floating point values.
 *   When argument is NaN, return argument
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 30
 *   Rating: 4
 */
unsigned float_twice(unsigned uf) {
  return 2;
}
