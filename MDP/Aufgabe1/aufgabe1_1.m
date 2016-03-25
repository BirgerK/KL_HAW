clearvars;
h_for_experiments = [0.001, 0.003, 0.004, 0.005];
xend=0.2;

ydiff = @(x,y) 10 - 500*y + 5000*x;
x0 = 0;
y0 = 1;

%Experiment

for i=1:length(h_for_experiments)
    h=h_for_experiments(i);
    figure('name',strcat('h=',num2str(h)));
    
    result_euler = euler(ydiff,x0,y0,h,xend);
    x_euler = result_euler(:,1);
    y_euler = result_euler(:,2);
    result_rk2 = runge_kutta(ydiff,x0,y0,h,xend);
    x_rk2 = result_rk2(:,1);
    y_rk2 = result_rk2(:,2);
    result_analyticSolution = analytic(x0,h,xend);
    x_analyticSolution = result_analyticSolution(:,1);
    y_analyticSolution = result_analyticSolution(:,2);
    
    plot(x_euler,y_euler,x_rk2,y_rk2,x_analyticSolution,y_analyticSolution)
    legend('Explizit Euler','Runge-Kutta','Analytisch');
end