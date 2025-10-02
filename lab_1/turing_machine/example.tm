# Программа для инвертирования битов (0->1, 1->0)
initial q0
final q_final

q0 0 -> q0 1 R
q0 1 -> q0 0 R
q0 _ -> q_final _ S

===TAPE===
1011001
