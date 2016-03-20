clearvars;

ydiff = @(x,y) 10 - 500*y + 5000*x;
x0 = 0;
y0 = 1;

h_for_experiments = [0.001, 0.003, 0.004, 0.005];
xend=0.2;

%Experiments
%   explicit EULER
figure('name','Euler-Method')

for i=1:length(h_for_experiments)
    h=h_for_experiments(i);
    
    result = euler(ydiff,x0,y0,h,xend);
    x_from_result = result(:,1);
    y_from_result = result(:,2);
    
    subplot(2,2,i)
    plot(x_from_result,y_from_result)
    title(strcat('h=',num2str(h)))
end

%   RUNGE-KUTTA
figure('name','Runge-Kutta-Method')

for i=1:length(h_for_experiments)
    h=h_for_experiments(i);
    
    result = runge_kutta(ydiff,x0,y0,h,xend);
    x_from_result = result(:,1);
    y_from_result = result(:,2);
    
    subplot(2,2,i)
    plot(x_from_result,y_from_result)
    title(strcat('h=',num2str(h)))
end