#include <iostream>
#include <string>
#include <cmath>
using namespace std;

int letNum(char letter)
{
    if (letter > 64)
        return letter - 55;
    else
        return letter - 48;
}

char numLet(int num)
{
    if (num < 10)
        return num + 48;
    else
        return num + 55;
}

string hexToDec(string hex)
{
    int num = 0;
    for (int i = 0; i < hex.length(); i++)
        num += (letNum(hex[i]) * pow(16, hex.length() - i - 1));
    return to_string(num);
}

string decToHex(string dec)
{
    string out = "";
    long long num = stoll(dec);    
    if(num<0)
        num += 4294967296;    
    while (num > 0) {
        out = numLet(num % 16) + out;
        num /= 16;
    }
    return out;
}

string decToBinary(string dec){
    int num = stoi(dec);
    string out = "";    
    while (num > 0) {
        out = to_string(num % 2) + out;
        num /= 2;
    }
    return out;
}

string biToDec(string bi){
    int num = 0;
    for(int i=bi.length()-1,c=1;i>=0;i--,c*=2)      
        num+=letNum(bi[i])*c;   
    return to_string(num);
}

int main(int argc, char **argv){
    if (argc != 4 || (string(argv[1]) != "hex" && string(argv[1]) != "dec" && string(argv[1]) != "bi")) {
        cout << "invalid input"<<endl;
        return 0;
    }
    string from = argv[1];
    string to = argv[2];
    string num = argv[3];    
    if (from == "hex")
        if(to=="dec")
            cout << hexToDec(num);
        else
            cout<< decToBinary(hexToDec(num));
    if (from == "dec")
        if(to=="hex")
            cout << decToHex(num);
        else
            cout<< decToBinary(num);
    if(from == "bi")
        if(to=="dec")
            cout << biToDec(num);
        else
            cout << decToHex(biToDec(num));
    cout << endl; 
}
