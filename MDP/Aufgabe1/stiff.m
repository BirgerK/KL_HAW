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
    
    % Calculate y-values by every given method
    result_euler = euler(ydiff,x0,y0,h,xend);
    x = result_euler(:,1);
    y_euler = result_euler(:,2);
    
    result_rk2 = runge_kutta(ydiff,x0,y0,h,xend);
    y_rk2 = result_rk2(:,2);
    
    result_analyticSolution = analytic(x0,h,xend);
    y_analyticSolution = result_analyticSolution(:,2);
    
    subplot(2,1,1);
    plot(x,y_euler,x,y_rk2,x,y_analyticSolution)
    title('Ergebnis des Verfahrens');
    legend('Explizit Euler','Runge-Kutta','Analytisch');
    
    % Calculate difference of every given method to analytic-solution
    euler_diff=[];
    rk2_diff=[];
    for x_i=1:length(x)
        euler_diff=[euler_diff; x(x_i) y_analyticSolution(x_i)-y_euler(x_i)];
        rk2_diff=[rk2_diff; x(x_i) y_analyticSolution(x_i)-y_rk2(x_i)];
    end
    y_euler_diff = euler_diff(:,2);
    y_rk2_diff = rk2_diff(:,2);
    
    subplot(2,1,2);
    plot(x,y_euler_diff,x,y_rk2_diff)
    title('Differenz des Verfahrens zur Analytischen L?sung');
    legend('Explizit Euler','Runge-Kutta');
end