#include <bits/stdc++.h>

using namespace std;

double read()
{
    double d;
    cin >> d;
    return d;
}

double write(double d)
{
    cout << d;
    return 0;
}

double expt(double base, double powNum) { return pow(base, powNum); }

double expt(double powNum) { return exp(powNum); }

const double c = 3.0;

double wavelength(double f);

void main()
{

    double f = 0;
    double w = 0;
    double p = 0;
    f = read();
    w = wavelength(f);
    if ((w < (1.0 / 2.0)))
    {
        p = 0.0;
    }
}
double wavelength(f) { return (c / f) }