class JogoDaForca:

    def __init__(self, palavra, tema):
        self.palavra = palavra.upper()
        self.tema = tema
        self.letras_corretas = set()
        self.letras_erradas = set()
        self.tentativas_max = 6
        self.tentativas_feitas = 0

    def adivinhar_letra(self, letra):
        if not letra or len(letra) != 1 or not letra.isalpha():
            return None
        letra = letra.upper()
        if letra in self.palavra and letra not in self.letras_corretas:
            self.letras_corretas.add(letra)
            return True
        elif letra not in self.palavra and letra not in self.letras_erradas:
            self.letras_erradas.add(letra)
            self.tentativas_feitas += 1
            return False
    
        return None
    
    def palavra_descoberta(self):
        return ' '.join([letra if letra in self.letras_corretas else '_' for letra in self.palavra])
    
    def verificar_vitoria(self):
        return all(letra in self.letras_corretas for letra in self.palavra)
    
    def verificar_derrota(self):
        return self.tentativas_feitas >= self.tentativas_max
    
    def get_status(self):
        return {
            'palavra': self.palavra,
            'letras_corretas': sorted(self.letras_corretas),
            'letras_erradas': sorted(self.letras_erradas),
            'tentativas_max': self.tentativas_max,
            'tentativas_feitas': self.tentativas_feitas,
            'tema': self.tema,
            'vitoria': self.verificar_vitoria(),
            'derrota': self.verificar_derrota()

        }
    