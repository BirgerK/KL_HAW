function result=imp_euler(f0,x0,y0,h,xend)
%IMPLICITE EUKER calculating DGL by implicit euler method
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
lasty = y0;

    for x=firstx:h:xend
        options = optimset('Display','off');                    %Einstellen der Optionen fuer das f Solve auf keine Ausgabe
        yn1appro = fsolve(@(n)n-lasty-h*f0(x, n), x , options); %Zuweisung des y wertes auf n und definition innerhalb der Funktion
        yn1 = lasty + h * f0(x,yn1appro);                       %Loesen der Gleichung mit Approximiertem Y

        result = [result ; x yn1];
        lasty = yn1;
    end
end
