#include <bits/stdc++.h>
#include "konstants.h"
#include <thread>
using namespace std;

#define size 32

void SHR(bool* bits,bool* result, int amt){
    for(int i = 0; i<size; i++)
        result[i] = bits[i];

    for(int i = 0; i < amt; i++){
        for(int bit = size-1; bit>0 ; bit--)
            result[bit] = result[bit-1];        
        result[0] = 0;
    }
}

void ROTR(bool* bits,bool* result, int amt){
    for(int i = 0; i < size;i++)
        result[i] = bits[i];
    
    for(int i = 0; i < amt; i++){
        bool carrybit = result[size-1];
        for(int bit = size-1; bit>0 ; bit--)
            result[bit] = result[bit-1];        
        result[0] = carrybit;
    }
}

void XOR(bool* bits,bool* bits1,bool* &result){
    for(int i = 0; i<size; i++)
        result[i] = bits[i] xor bits1[i];    
}

void add(bool* bits, bool* bits1, bool* &result){
    bool carrybit = 0;
    for(int i = size-1; i>=0; i--){
        result[i] = bits[i] xor bits1[i] xor carrybit;
        carrybit = (bits[i] + bits1[i] + carrybit)>1;
    }
}

void sigmaZero(bool* bits,bool* &result){
    bool rotr7 [size], rotr18 [size], shr3 [size];
    bool* temp = new bool [size];  

    ROTR(bits,rotr7,7);
    ROTR(bits,rotr18,18);
    SHR(bits,shr3, 3);

    XOR(rotr7,rotr18,temp);
    XOR(temp,shr3,result);
}

void sigmaOne(bool* bits,bool* &result){
    bool rotr17 [size], rotr19 [size], shr10 [size];
    bool* temp = new bool [size];    

    ROTR(bits,rotr17,17);
    ROTR(bits,rotr19,19);
    SHR(bits,shr10, 10);

    XOR(rotr17,rotr19,temp);
    XOR(temp,shr10,result);
}

void SIGMAzero(bool* bits,bool* &result){
    bool rotr2[size], rotr13 [size], rotr22 [size];
    bool* temp = new bool [size];    

    ROTR(bits, rotr2, 2);
    ROTR(bits, rotr13, 13);
    ROTR(bits, rotr22, 22);

    XOR(rotr2,rotr13,temp);
    XOR(temp,rotr22,result);
}

void SIGMAone(bool* bits,bool* &result){
    bool rotr6 [size], rotr11 [size], rotr25 [size];
    bool* temp = new bool [size];    

    ROTR(bits, rotr6, 6);
    ROTR(bits, rotr11, 11);
    ROTR(bits, rotr25, 25);

    XOR(rotr6,rotr11,temp);
    XOR(temp,rotr25,result);
}

void choice(bool* x, bool* y, bool* z, bool* &result){
    for(int i = 0; i<size;i++){
        if(x[i])
            result[i] = y[i];
        else
            result[i] = z[i];
    }
}

void maj(bool* x, bool* y, bool* z, bool* &result){    
    for(int i = 0; i < size; i++){
        result[i] = (x[i] + y[i] + z[i])>1;
    }
}

void biDec(bool* bits, int n, int dec){
    for(int i = n-1; i>=0; i--){      
        if(dec > 0){
            bits[i] = dec%2;
            dec /= 2;
        }else
            bits[i] = 0;        
    }
}

void Clear(){
    cout << "\x1B[2J\x1B[H";
}

void printWord(bool* bits){
    for(int i = 0; i < size; i++)
        cout << bits[i];
}

string fromFile(string file){
    ifstream in(file);
    char temp;
    string out = "";
    while(in.get(temp)){
        out += temp;
    }

    return out;
}


void convertInputToBinary(bool* &message, int& msgsize, string input){
    unsigned int mlen = input.length();
    unsigned int numBits = mlen*8;
    unsigned int msgCount = numBits/512+1;
    unsigned int msgSize = msgCount*512;


    bool ibits [numBits];
    bool sizebits [64];
    biDec(sizebits,64,numBits);

    bool msgbits [msgSize];
    message = new bool[msgSize];

    for(unsigned int i = 0 ; i < mlen; i++){
        int c = abs(input[i]);

        bool byte [8];

        biDec(byte,8,c);

        for(int bit = 0; bit<8; bit++)            
            ibits[i*8+bit] = byte[bit];

    }  
    
    for(int i = 0; i < numBits; i++)
        msgbits[i] = ibits[i];
    

    msgbits[numBits] = 1; //endbit or whatever (after msg itself before padding)

    for(int i = numBits+1; i < msgSize-64; i++)//padding
        msgbits[i] = 0;

    for(int i = 0; i < 64; i++)
        msgbits[i+msgSize-64] = sizebits[i];
    
    for(int i = 0; i < msgSize; i++)
        message[i] = msgbits[i];

    msgsize = msgSize;
}

void intoBlocks(bool* msg, bool** &blocks, int msgSize, int& numBlocky){
    int numBlocks = msgSize/512;
    numBlocky = numBlocks;
    blocks = new bool*[numBlocks];
    for(int i = 0; i < numBlocks; i++){
        blocks[i] = new bool[512];

        for(int bit = 0; bit < 512; bit++)
            blocks[i][bit] = msg[i*512+bit];
    }
}

void messageSchedule(bool* block, bool** &result){
    result = new bool*[64];
    for(int w = 0, i = 0; w < 16; w++){ //first 16 from block
        result[w] = new bool[size];
        for(int b = 0; b < size; b++,i++){
            result[w][b] = block[i];
        }
    }
    for(int w = 16; w < 64; w++){ //fill da rest
        bool* s1 = new bool[size], *s0 = new bool[size],
         *temp = new bool[size], *temp1 = new bool[size];
        result[w] = new bool[size];

        sigmaOne(result[w-2],s1);
        sigmaZero(result[w-15],s0);
        add(result[w-16],s0,temp);
        add(temp,result[w-7],temp1);
        add(temp1, s1, result[w]);

    }
}

void compression(bool** &H0,bool** W){
    bool** H1 = new bool*[8];
    for(int i = 0; i < 8; i++){
        H1[i] = new bool[size];
        for(int b = 0; b < size; b++){
            H1[i][b] = H0[i][b];
        }
    }

    for(int w = 0; w < 64; w++){
        bool* T1 = new bool[size], *T2 = new bool[size],
        *S1E = new bool[size], *S0A = new bool[size],
        *Chefg = new bool[size], *Majabc = new bool[size],
        *temp = new bool[size], *temp1 = new bool[size],
        *temp2 = new bool[size];

        //T1
        SIGMAone(H1[4], S1E);
        choice(H1[4],H1[5],H1[6],Chefg);

        add(W[w],konstants[w],temp);      
        
        add(Chefg,S1E,temp1);
        add(temp1,H1[7],temp2);

        add(temp,temp2,T1);       
                    

        /*cout << "T1: ";
        printWord(T1);
        cout << endl;*/

        //T2
        SIGMAzero(H1[0], S0A);   
        maj(H1[0],H1[1],H1[2],Majabc);
        add(S0A, Majabc, T2);

        /*cout << "T2: ";
        printWord(T2);
        cout << endl;*/

        /*for(int s = 0; s < 8; s++){
            for(int b = 0; b < size; b++){
                cout << H1[s][b];               
            }
            cout << endl;
        }
        cout << endl;*/

        for(int s = 7; s > 0; s--){
            for(int b = 0; b < size; b++){
                H1[s][b] = H1[s-1][b];                
            }
        }

        bool* tempe = new bool[size];
        for(int i = 0; i < size; i++){
            tempe[i] = H1[4][i];
        }

        add(T1,T2,H1[0]);
        add(T1,tempe,H1[4]);
    }

    for(int i = 0; i < 8; i++){
        bool* tempe = new bool[size];
        for(int b = 0; b < size; b++){
            tempe[b] = H0[i][b];
        }
        add(tempe,H1[i],H0[i]);
    }

    /*for(int s = 0; s < 8; s++){
        for(int b = 0; b < size; b++){
            cout << H0[s][b];               
        }
        cout << endl;
    }
    cout << endl;*/
}

string biHex(bool** bits){
    string ret = "";
    for(int l = 0; l < 8; l++){
        int dec = 0;
        string curr = "";
        for(int b = size-1, i = 1; b >= 0; b--){
            if(bits[l][b])
                dec+=i;

            if(i==8){
                i = 1;
                char c;
                if(dec < 10)
                    c = dec+48;
                else
                    c = dec+55;

                curr = c + curr;
                dec = 0;            
            }else
                i*=2;
        }
        //cout << curr << endl;
        ret = ret + curr;
    }
    return ret;
}

void Sha256(string input, string &output){
    int msgSize, numBlocks;
    bool* msgbits;
    bool** msgblocks;

    convertInputToBinary(msgbits,msgSize,input);

    /*cout << "Message: ("<< msgSize <<" bits)\n";

    for(int i = 0; i < msgSize; i++)
        cout << msgbits[i];

    cout << endl << endl;*/

    intoBlocks(msgbits,msgblocks,msgSize,numBlocks);

    /*cout << "blocks: "<< endl;

    for(int b = 0; b<numBlocks; b++){
        cout << b << ": "<< endl;
        for(int i = 0; i<512; i++){
            cout << msgblocks[b][i];
        }
        cout << endl<<endl;
    }

    cout << endl << endl;*/

    bool*** Words = new bool**[numBlocks];

    for(int bl = 0; bl < numBlocks; bl++)
        messageSchedule(msgblocks[bl],Words[bl]);

    /*for(int bl = 0; bl < numBlocks; bl++){
        cout << "block " << bl << ":" << endl<<endl; 
        for(int w = 0; w < 64; w++){
            cout << "W" << w << ": ";
            for(int b = 0; b < size; b++)
                cout << Words[bl][w][b];
            cout << endl;
        }
        cout << endl;
    }
    cout << endl;*/

    bool** H0 = new bool*[8];
    for(int i = 0; i < 8; i++){ //copies initial hash values
        H0[i] = new bool[size];
        for(int b = 0; b < size; b++){
            H0[i][b] = initial[i][b];
        }
    }

    for(int i = 0; i < numBlocks; i++){
        compression(H0, Words[i]);
    }

    /*for(int s = 0; s < 8; s++){
        for(int w = 0; w < size; w++)
            cout << H0[s][w];
        cout << endl;
    }
    cout << endl;*/

    output = biHex(H0);   
   
}

char genRandom(int stringLength)  // Random string generator function.
{
    return alphanum[rand() % stringLength];
}

string makeRandom(int stringLength){
    string out = "";
    for(int i = 0; i < stringLength; i++)
        out+=genRandom(stringLength);
    return out;
}

int main(int argc, char** argv){
    
    string input;
    int diff;

    if(argc==2){
        input = argv[1];
    }else if (argc == 3){
        input = argv[1];
        diff = stoi(argv[2]);
    }


    if(input == "mine"){
        int stringLength = sizeof(alphanum) - 1;
        int cores = thread::hardware_concurrency();               
        string outputs[cores], inputs [cores];
        vector<thread> threads;
        while(true){

            for(int i = 0; i < cores; i++){
                inputs [i] = makeRandom(stringLength);
                threads.push_back(thread(Sha256,inputs[i],outputs[i]));
            }

            for(auto &th: threads){
                th.join();
            }
            
            for(int i = 0; i < cores; i++)
                cout << inputs[i] << " " << outputs[i] << endl;
            

            for(int i = 0; i<cores; i++){
                if(outputs[i].find_first_not_of('0')>=diff){
                    cout << endl << endl
                    << "found viable hash!" << endl<< endl
                    << "key: " << inputs[i] << endl
                    << "hash: " << outputs[i] << endl << endl;
                }
            }
        }
    }

    if(input.find(".txt")!=string::npos && input.find(".txt")==input.length()-4){ //has .txt at end
        input = fromFile(input);
    }

    if(input.find(".png")!=string::npos && input.find(".png")==input.length()-4){ //has .txt at end
        input = fromFile(input);
    }

    if(input.find(".jpg")!=string::npos && input.find(".jpg")==input.length()-4){ //has .txt at end
       input = fromFile(input);
    }

    string output;

    Sha256(input,output);

    cout << output << endl;

    return 0;

}
