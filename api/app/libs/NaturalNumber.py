"""
suma_total = (numero_total(numero_total + 1)) / 2
suma_actual = sum(lista)
resultado = suma_total = suma_actual
"""

class NaturalNumber:
    def __init__(self):
        self.numero_natural:int = 100
        self.full_set = list(range( (self.numero_natural - 99),(self.numero_natural + 1)))
        self.suma_total = (self.numero_natural * (self.numero_natural + 1)) / 2
        self.response = {}
        self.encontrados = []

    def mostrar(self):
        print(type(self.full_set))
        return self.full_set
    
    def remover_numero(self, numero: int) -> None:

        if not isinstance(numero, int):
            raise ValueError(f"Error: dato ingresado no es valido")
        
        if numero < (self.numero_natural - 99) or numero > (self.numero_natural):
            raise ValueError(f"Error: el dato ingresado no es permitdo")
        
        if numero not in self.full_set:
            raise ValueError(f"Numero {numero} no encontrado")
        
        self.full_set.remove(numero)
    
    def calcular_faltantes(self) -> int:            
        faltate, n_total, n_encontrados = 0, len(self.full_set), len(self.encontrados)

        if n_total == self.numero_natural:
            raise ValueError("No se tienen ningun faltante")
        
        ## Combinar listas, real vs encontrados
        temp = self.full_set +  self.encontrados
        
        suma_actual = sum(temp)
        faltate = int(self.suma_total - suma_actual)
        self.encontrados.append(faltate)                    
        
        return faltate
    
    def mostrar_encontrados(self):
        return self.encontrados