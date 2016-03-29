function result=lorenz_helper(y)
  h_for_experiments = [0.002];
  tend=120;

  x = @(x,y,z) -10 *(x-y);
  z = @(x,y,z) x * y - 2.67 * z;
  x0 = 0.01;
  y0 = 0.01;
  z0 = 0.00;

  %Experiment

  for i=1:length(h_for_experiments)
      h=h_for_experiments(i);
      steps = tend / h;

      result = [0 x0 y0 z0];

      t0 = 0;
      for step=1:1:steps
          t = t0 + step*h;
          next_t = t + h;

          % Runge-Kutta-Verfahren
          current_x = result(step,2);
          current_y = result(step,3);
          current_z = result(step,4);

          k1 = h * x(current_x,current_y,current_z);
          l1 = h * y(current_x,current_y,current_z);
          m1 = h * z(current_x,current_y,current_z);

          k2 = h * x(current_x + k1/2,current_y + l1/2, current_z + m1/2);
          l2 = h * y(current_x + k1/2,current_y + l1/2, current_z + m1/2);
          m2 = h * z(current_x + k1/2,current_y + l1/2, current_z + m1/2);

          next_x = current_x + k2;
          next_y = current_y + l2;
          next_z = current_z + m2;
          result = [result; next_t next_x next_y next_z];
      end
  end
end
