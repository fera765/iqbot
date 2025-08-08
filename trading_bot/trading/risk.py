# Funções utilitárias para gerenciamento de risco

def check_stop_win(profit, stop_win):
    return profit >= stop_win

def check_stop_loss(profit, stop_loss):
    return abs(profit) >= stop_loss