#include <bits/stdc++.h>
using namespace std;
double read(){ double d; cin >> d; return d; }
double write(double d){ cout << d; return 0; }
double expt(double base, double powNum){ return pow(base,powNum);}
double expt(double powNum){ return exp(powNum);}
const double E = 2.7;
const double log_2 = 0.6931;
double massdecay(double mass,double time,double halflife);
int main(){
double mass=0;double halflife=0;double time=0;double re=0;mass=read();;halflife=read();;time=read();;re=massdecay(mass, time, halflife);if ((re>(mass/2.0))){ write(mass);} else { write(re);}
 return 0; }double massdecay( double mass, double time, double halflife){ return(mass*expt( E, (((0.0-log_2)/halflife)*time)));}