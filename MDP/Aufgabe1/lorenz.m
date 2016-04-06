clearvars;

y_origin = @(x,y,z) (40 - z) * x-y;
y_modified = @(x,y,z) (40.000000001 - z) * x-y;

result = lorenz_helper(y_origin);
t = result(:,1);
x_values = result(:,2);
y_values = result(:,3);
z_values = result(:,4);

subplot(2,1,1);
plot(t,x_values)
legend('x(t)');
subplot(2,1,2);
plot(t,z_values)
legend('z(t)');

figure();
subplot(1,1,1);
plot3(x_values,y_values,z_values)
legend('Lorenz Attraktor');

result = lorenz_helper(y_modified);
x1_values = result(:,2);
y1_values = result(:,3);
z1_values = result(:,4);

figure();
subplot(1,1,1);
plot3(x_values,y_values,z_values,x1_values,y1_values,z1_values)
legend('Lorenz Attraktor','Lorenz Attraktor, modified y');

figure('name',strcat('h=0.002'));
plot(t,x_values,t,x1_values)
title('Vergleich x-Simulationen');
legend('y mit 40','y mit 40.0...01');
