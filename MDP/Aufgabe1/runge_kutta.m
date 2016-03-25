function result=runge_kutta(f0,x0,y0,h,xend)
%RUNGE KUTTA calculating DGL by runge-kutta method
% Input :
%   f0 ... Funktion von R x R^n nach R^n (String oder Inline)
%   x0 ... Startpunkt auf der x-Achse, z.B. 0
%   y0 ... Ergebnis von f0(x0) = y0
%   h ... Schritt-Praezision, z.B. 0.001
%   xend ... Hoechstwert der x-Achse
% Output:
%   result ... Loesungswerte als Matrix
result=[x0 y0];

firstx = x0+h;
lastx = x0;
lasty = y0;

for x=firstx:h:xend
    k1 = h * f0(lastx,lasty);
    k2 = h * f0(lastx + h/2, lasty + k1/2);
    
    newy = lasty + k2;
    
    result = [result ; x newy];
    
    lastx = x;
    lasty = newy;
end
