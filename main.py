from simulador import Simulador

print("inicio programa")

if __name__ == "__main__":
    # aqui se intancia el simulador, el cual dara paso a la simulacion,
    # ademas simulador se encarga de registrar las replicas
    simulador = Simulador()
    simulador.simular_replica()

print("fin programa")
