import math

print("  PROGRAMA DE DISEÑO A FATIGA - EJE  ")

# SISTEMA DE UNIDADES

sistema = input("Seleccione sistema (SI / IN): ").upper()

# GEOMETRIA

print("\n--- GEOMETRIA ---")
D = float(input("Diametro mayor D: "))
d = float(input("Diametro menor d: "))

r = float(input("Radio de filete r: "))

print(f"\nD/d = {D/d:.4f}")
print(f"r/d = {r/d:.4f}")

# CARGAS

print("\n--- CARGAS ---")
Ma = float(input("Momento alternante Ma: "))
Mm = float(input("Momento medio Mm: "))
Ta = float(input("Torque alternante Ta: "))
Tm = float(input("Torque medio Tm: "))

# MATERIAL

print("\n--- PROPIEDADES DEL MATERIAL ---")
Sut = float(input("Sut: "))
Sy = float(input("Sy: "))
Se = float(input("Se: "))

# CONVERSION DE UNIDADES

if sistema == "IN":
    # pulgadas a metros
    D *= 0.0254
    d *= 0.0254
    r *= 0.0254

    # lb-in a N-m
    Ma *= 0.113
    Mm *= 0.113
    Ta *= 0.113
    Tm *= 0.113

    # ksi a Pa
    Sut *= 6.895e6
    Sy *= 6.895e6
    Se *= 6.895e6

else:
    # mm a metros
    D /= 1000
    d /= 1000
    r /= 1000

    # MPa a Pa
    Sut *= 1e6
    Sy *= 1e6
    Se *= 1e6

# FACTORES DE CONCENTRACION

calcular_k = input("\n¿Desea calcular Kf y Kfs? (s/n): ").lower()

if calcular_k == "s":
    q = float(input("Sensibilidad a la muesca q: "))
    qs = float(input("Sensibilidad a cortante qs: "))
    Kt = float(input("Kt: "))
    Kts = float(input("Kts: "))

    Kf = 1 + q * (Kt - 1)
    Kfs = 1 + qs * (Kts - 1)
else:
    Kf = float(input("Ingrese Kf: "))
    Kfs = float(input("Ingrese Kfs: "))

# ESFUERZOS

# Flexion
sigma_a = Kf * (32 * Ma) / (math.pi * d**3)
sigma_m = Kf * (32 * Mm) / (math.pi * d**3)

# Torsion
tau_a = Kfs * (16 * Ta) / (math.pi * d**3)
tau_m = Kfs * (16 * Tm) / (math.pi * d**3)

# VON MISES

sigma_vm_a = math.sqrt(sigma_a**2 + 3*tau_a**2)
sigma_vm_m = math.sqrt(sigma_m**2 + 3*tau_m**2)
sigma_vm_max = math.sqrt((sigma_a+sigma_m)**2 + 3*(tau_a+tau_m)**2)

# FACTOR DE DISEÑO ESTATICO (VON MISES)

n_vm = Sy / sigma_vm_max

# CRITERIOS DE FATIGA

print("\nSeleccione criterio:")
print("1 - Goodman")
print("2 - Gerber")
print("3 - Soderberg")
print("4 - ASME")
print("5 - Todos")

opcion = int(input("Opcion: "))

print("\n--- RESULTADOS ---")
print(f"Kf = {Kf:.4f}")
print(f"Kfs = {Kfs:.4f}")

print(f"\nEsfuerzo normal alternante = {sigma_a/1e6:.2f} MPa")
print(f"Esfuerzo normal medio = {sigma_m/1e6:.2f} MPa")
print(f"Esfuerzo cortante alternante = {tau_a/1e6:.2f} MPa")
print(f"Esfuerzo cortante medio = {tau_m/1e6:.2f} MPa")

print(f"\nVon Mises alternante = {sigma_vm_a/1e6:.2f} MPa")
print(f"Von Mises medio = {sigma_vm_m/1e6:.2f} MPa")
print(f"Von Mises maximo = {sigma_vm_max/1e6:.2f} MPa")

print(f"\nFactor Von Mises estatico = {n_vm:.3f}")

# CRITERIOS

if opcion == 1 or opcion == 5:
    n_goodman = 1 / ((sigma_vm_a/Se) + (sigma_vm_m/Sut))
    print(f"\nFactor Goodman = {n_goodman:.3f}")

if opcion == 2 or opcion == 5:
    n_gerber = 1 / ((sigma_vm_a/Se) + (sigma_vm_m/Sut)**2)
    print(f"Factor Gerber = {n_gerber:.3f}")

if opcion == 3 or opcion == 5:
    n_soderberg = 1 / ((sigma_vm_a/Se) + (sigma_vm_m/Sy))
    print(f"Factor Soderberg = {n_soderberg:.3f}")

if opcion == 4 or opcion == 5:
    n_asme = 1 / math.sqrt((sigma_vm_a/Se)**2 + (sigma_vm_m/Sy)**2)
    print(f"Factor ASME eliptico = {n_asme:.3f}")