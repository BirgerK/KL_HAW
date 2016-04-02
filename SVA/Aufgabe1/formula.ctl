(m1 == 1) -> (EF (was_acked_m1 > 0) -> EF (m0 == 1));
(m0 == 1) -> E(send_pipe_m0 > 0  U EG m1 == 1);
