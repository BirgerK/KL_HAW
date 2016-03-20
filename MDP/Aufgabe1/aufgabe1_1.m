clearvars;

ydiff = @(x,y) 10 - 500*y + 5000*x;
x0 = 0;
y0 = 1;

%EULER
% Versuch 1
h=0.001;
x=0.2;

result = euler(ydiff,x0,y0,h,x);
x_from_result = result(:,1);
y_from_result = result(:,2);

figure
subplot(2,2,1)
plot(x_from_result,y_from_result)
title('h=0.001')

% Versuch 2
h=0.003;
x=0.2;

result = euler(ydiff,x0,y0,h,x);
x_from_result = result(:,1);
y_from_result = result(:,2);

subplot(2,2,2)
plot(x_from_result,y_from_result)
title('h=0.003')

% Versuch 3
h=0.004;
x=0.2;

result = euler(ydiff,x0,y0,h,x);
x_from_result = result(:,1);
y_from_result = result(:,2);

subplot(2,2,3)
plot(x_from_result,y_from_result)
title('h=0.004')

% Versuch 4
h=0.005;
x=0.2;

result = euler(ydiff,x0,y0,h,x);
x_from_result = result(:,1);
y_from_result = result(:,2);

subplot(2,2,4)
plot(x_from_result,y_from_result)
title('h=0.005')