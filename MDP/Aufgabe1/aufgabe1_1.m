ydiff = @(x,y) 10 - 500*y + 5000*x;
x0 = 0;
y0 = 1;

% Versuch 1
h=0.001;
x=0.2;

result = euler(ydiff,x0,y0,h,x);
X_from_result = result(:,1);
Y_from_result = result(:,2);
plotmatrix(X_from_result,Y_from_result);