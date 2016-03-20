function u=euler(f0,x0,y0,h,xend)
%EULER calculating DGL by euler method
% Input :
%   f0 ... Funktion von R x R^n nach R^n (String oder Inline)
%   x0 ... Startpunkt auf der x-Achse, z.B. 0
%   y0 ... Ergebnis von f0(x0) = y0
%   h ... Schritt-Praezision, z.B. 0.001
%   xend ... H?chstwert der x-Achse
% Output:
%   u ... Loesungswerte als Matrix
u=[x0 y0];

firstx = x0+h;
oldy = y0;

for x=firstx:h:xend
    newy = oldy + h * f0(x,oldy);
    
    u = [u ; x newy;];
    
    oldy = newy;
end
