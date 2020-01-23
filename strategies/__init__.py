#!/usr/bin/env python
from strategies.timer import Timer
from strategies.measure import Measure
from strategies.input import ConsoleUserInput, WindowUserInput
from strategies.easy import Random, Greedy, Unselfish, SlowStarter, Table
from strategies.minmax import MinMax1_T, MinMax2_T, MinMax3_T, MinMax4_T, MinMax1_TP, MinMax2_TP, MinMax3_TP, MinMax4_TP, MinMax1_TPO, MinMax2_TPO, MinMax3_TPO, MinMax4_TPO, MinMax2_TPW, MinMax3_TPW, MinMax4_TPW, MinMax1_TPOW, MinMax2_TPOW, MinMax3_TPOW, MinMax4_TPOW
from strategies.negamax import NegaMax1_TPOW, NegaMax2_TPOW, NegaMax3_TPW, NegaMax3_TPOW, NegaMax4_TPOW
from strategies.alphabeta import AlphaBeta1_TPOW, AlphaBeta2_TPOW, AlphaBeta3_TPW, AlphaBeta3_TPOW, AlphaBeta4_TPW, AlphaBeta4_TPOW
from strategies.negascout import NegaScout3_TPW, NegaScout3_TPOW, NegaScout4_TPW, NegaScout4_TPW_O, NegaScout5_TPW_O
from strategies.iterative import AbI_TPOW, AbI_B_TP, AbI_B_TPO, AbI_B_TPW, AbI_BC_TPW, AbI_B_TPOW, AbI_BC_TPOW, AbI_W_BC_TPOW, NsI_B_TPW, NsI_B_TPW_O
from strategies.switch import SwitchNegaScout
from strategies.fullreading import AbIF5_B_TPOW, AbIF7_B_TPOW, AbIF9_B_TPOW, AbIF10_B_TPW, AbIF11_B_TPW, AbIF11_BC_TPW, AbIF12_B_TPW, AbIF13_B_TPW, AbIF11_B_TPOW, AbIF13_B_TPOW, AbIF15_B_TPOW, AbIF7_BC_TPOW, AbIF7_W_BC_TPOW, NsIF10_B_TPW, NsIF11_B_TPW, NsIF12_B_TPW, NsIF10_B_TPW_O, NsIF11_B_TPW_O, NsIF12_B_TPW_O, SwitchNsF11, SwitchNsF12
from strategies.joseki import AbIF11J_B_TPW, AbIF11J_BC_TPW, SwitchNsF11J, SwitchNsF12J
from strategies.montecarlo import MonteCarlo30, MonteCarlo100, MonteCarlo1000
from strategies.proto import MinMax2, NegaMax3, AlphaBeta4, AB_T4, AB_TI
from strategies.randomopening import MinMax3Ro_TPW, MinMax3Ro_TPOW, NegaMax3Ro_TPW, NegaMax3Ro_TPOW, AlphaBeta3Ro_TPW, AlphaBeta3Ro_TPOW, NegaScout3Ro_TPW, NegaScout3Ro_TPOW, AlphaBeta4Ro_TPW, NegaScout4Ro_TPW, NegaScout4Ro_TPW_O, NegaScout5Ro_TPW_O, AB_TIRo, AbIF11JRo_B_TPW, AbIF11JRo_BC_TPW, SwitchNsF12JRo
