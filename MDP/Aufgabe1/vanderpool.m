clearvars;
h_for_experiments = [0.001, 0.02];
xend=31;

ydiff1 = @(y1,y2) 6 * (1 - y2*y2) * y1 - y2;
ydiff2 = @(y1,y2) y1;
x0 = 0;

%Experiment

for i=1:length(h_for_experiments)
    h=h_for_experiments(i);
    steps = xend / h;
    
    result_euler_1 = [0 1];
    result_euler_2 = [0 0];
    
    result_rk2_1 = [0 1];
    result_rk2_2 = [0 0];
    
    for step=1:1:steps
        current_x = x0 + step*h;
        next_x = current_x + h;
        
        % Euler-Verfahren
        current_euler_1 = result_euler_1(step,2);
        current_euler_2 = result_euler_2(step,2);
        next_euler_1 = current_euler_1 + h * ydiff1(current_euler_1,current_euler_2);
        next_euler_2 = current_euler_2 + h * ydiff2(current_euler_1,current_euler_2);
        result_euler_1 = [result_euler_1; next_x next_euler_1];
        result_euler_2 = [result_euler_2; next_x next_euler_2];
        
        % Runge-Kutta-Verfahren
        current_rk2_1 = result_rk2_1(step,2);
        current_rk2_2 = result_rk2_2(step,2);
        
        k1_y1 = h * ydiff1(current_rk2_1,current_rk2_2);
        k1_y2 = h * ydiff2(current_rk2_1,current_rk2_2);
        k2_y1 = h * ydiff1(current_rk2_1 + k1_y1/2,current_rk2_2 + k1_y2/2);
        k2_y2 = h * ydiff2(current_rk2_1 + k1_y1/2,current_rk2_2 + k1_y2/2);
        
        next_rk2_1 = current_rk2_1 + k2_y1;
        next_rk2_2 = current_rk2_2 + k2_y2;
        result_rk2_1 = [result_rk2_1; next_x next_rk2_1];
        result_rk2_2 = [result_rk2_2; next_x next_rk2_2];
    end
    figure('name',strcat('h=',num2str(h)));
    
    % Calculate y-values by every given method
    x = result_euler_1(:,1);
    y_euler_1 = result_euler_1(:,2);
    y_euler_2 = result_euler_2(:,2);
    y_rk2_1 = result_rk2_1(:,2);
    y_rk2_2 = result_rk2_2(:,2);
    
%     result_rk2 = runge_kutta(ydiff,y1,y2,h,xend);
%     y_rk2 = result_rk2(:,2);
    
%     plot(x,y_euler,x,y_rk2)
    plot(x,y_euler_1,x,y_euler_2,x,y_rk2_1,x,y_rk2_2)
    title('Ergebnis der Verfahren');
%     legend('Explizit Euler','Runge-Kutta');
legend('Explizit Euler y1','Explizit Euler y2','Runge-Kutta y1','Runge-Kutta y2');
end