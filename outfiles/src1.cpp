#include <bits/stdc++.h>
using namespace std;
double read(){ double d; cin >> d; return d; }
double write(double d){ cout << d; return 0; }
double expt(double base, double powNum){ return pow(base,powNum);}
double expt(double powNum){ return exp(powNum);}
const double A = 2.9;
const double B = 6.0;
double sum(double x,double sumterm);
double subtract(double x,double minusterm);
int main(){
double res=0;double x=0;x=1.0;if ((A<B)){ res=sum(x, A);} else { res=subtract(x, B);}write(res);
 return 0; }double sum( double x, double sumterm){ return(x+sumterm);}double subtract( double x, double minusterm){ return((x-minusterm)*minusterm);}