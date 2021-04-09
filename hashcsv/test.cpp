#include <iostream>

using namespace std;

struct Bid {
    string bidId; // unique identifier
    string title;
    string fund;
    double amount;
    Bid() {
        amount = 0.0;
    }
};

int main(){
    Bid table[7];

    cout << table[0].amount << endl;

}