#include <bits/stdc++.h>
using namespace std;
double read(){ double d; cin >> d; return d; }
double write(double d){ cout << d; return 0; }
double expt(double base, double powNum){ return pow(base,powNum);}
double expt(double powNum){ return exp(powNum);}
const double c = 3.0;
double wavelength(double f);
int main(){
double f=0;double w=0;f=read();w=wavelength(f);if ((w<(1.0/2.0))){ w=0.0;} write(w);
 return 0; }double wavelength( double f){ return(c/f);}