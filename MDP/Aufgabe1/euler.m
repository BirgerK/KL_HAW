function result=euler(f0,x0,y0,h,xend)
%EULER calculating DGL by euler method
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
    newy = lasty + h * f0(lastx,lasty);
    
    result = [result ; x newy];
    
    lastx = x;
    lasty = newy;
end
end