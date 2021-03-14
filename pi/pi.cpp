#include <iostream>
#include <iomanip>
#include <random>
using namespace std;

int main(){
    srand(time(NULL));
    
    int n,numInCircle=0;
    cout << "depth: " << setprecision(100);
    cin >> n;

    for(int i=0;i<n;i++){
        float x = float(rand())/RAND_MAX;
        float y = float(rand())/RAND_MAX;
        if(x*x+y*y<=1)
            numInCircle++;
        cout << 4.f*numInCircle/(i+1) << endl;
    }

    return 0;
}