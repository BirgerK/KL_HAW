/*
First
P2 is the only one who gets an id which is smaller than himself.
*/
EF(
  (Pipe2_4==0 & (Pipe2_1==1 | Pipe2_2==1 | Pipe2_3==1)) &
  (P2_1==1 | P2_2==1 | P2_3==1) &
  ((P2_2==1 & Pipe2_1==1) | (P2_3==1 & (Pipe2_1==1 | Pipe2_2==1))) &
  AX(
    (Pipe3_1==1 & P2_1==1) | (Pipe3_2==1 & P2_2==1) | (Pipe3_3==1 & P2_3==1)
  )
);
/*
Second
P3 is getting a higher id than himself
The 'true'-Statement should be "My Input is equal to my output"
*/
EF(
  (Pipe3_4==0 & (Pipe3_1==1 | Pipe3_2==1 | Pipe3_3==1)) &
  (P3_1==1 | P3_2==1 | P3_3==1) &
  ((P3_2==1 & Pipe3_3==1) | (P3_1==1 & (Pipe3_2==1 | Pipe3_3==1))) &
  AX(
    true
  )
);
/*
Third
P3 is getting a higher id than himself
The 'true'-Statement should be "My Input is equal to myself"
*/
EF(
  (Pipe3_4==0 & (Pipe3_1==1 | Pipe3_2==1 | Pipe3_3==1)) &
  (P3_1==1 | P3_2==1 | P3_3==1) &
  ((P3_2==1 & Pipe3_3==1) | (P3_1==1 & (Pipe3_2==1 | Pipe3_3==1))) &
  AX(
    true
  )
);
/*
Fourth
P2 is getting its own id first
*/
EF(
  (Pipe2_4==0 & (Pipe2_1==1 | Pipe2_2==1 | Pipe2_3==1)) &
  (P2_1==1 | P2_2==1 | P2_3==1) &
  ((P2_1==1 & Pipe2_1==1) | (P2_2==1 & Pipe2_2==1) | (P2_3==1 & Pipe2_3==1)) &
  AX(
    Pipe3_1==0 & Pipe3_2==0 & Pipe3_3==0 & Pipe3_4==1
  )
);
/*
Fifth
P3 is getting check-token first
*/
EF(
  (Pipe3_4==1 & Pipe3_1==0 & Pipe3_2==0 & Pipe3_3==0) &
  (P3_1==1 | P3_2==1 | P3_3==1) &
  AX(
    Pipe1_1==0 & Pipe1_2==0 & Pipe1_3==0 & Pipe1_4==1
  )
);
