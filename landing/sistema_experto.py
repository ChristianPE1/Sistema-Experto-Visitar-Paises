from experta import Fact, KnowledgeEngine, Rule, MATCH

class Clima(Fact):
    """Hecho para definir países por clima"""
    pass

class Idioma(Fact):
    """Hecho para definir países por idioma"""
    pass

class AspectoTuristico(Fact):
    """Hecho para definir países por aspectos turísticos"""
    pass

class RecomendacionPais(Fact):
    """Información sobre las características deseadas"""
    pass

class SistemaRecomendaciones(KnowledgeEngine):

    def __init__(self, datos):
        super().__init__()
        self.datos = datos
        self.recomendaciones_clima = []
        self.recomendaciones_idioma = []
        self.recomendaciones_aspectos = []

    def cargar_hechos(self):
        # Declarar hechos basados en la nueva estructura de datos
        for pais, info in self.datos.items():
            if 'clima' in info:
                self.declare(Clima(tipo=info['clima'], pais=pais))
            if 'idioma' in info:
                self.declare(Idioma(idioma=info['idioma'], pais=pais))
            if 'aspectos_turisticos' in info:
                for aspecto in info['aspectos_turisticos']:
                    self.declare(AspectoTuristico(aspecto=aspecto, pais=pais))

    @Rule(RecomendacionPais(clima=MATCH.clima))
    def recomendar_por_clima(self, clima):
        self.recomendaciones_clima = [fact['pais'] for fact in self.facts.values() if isinstance(fact, Clima) and fact['tipo'] == clima]

    @Rule(RecomendacionPais(idioma=MATCH.idioma))
    def recomendar_por_idioma(self, idioma):
        self.recomendaciones_idioma = [fact['pais'] for fact in self.facts.values() if isinstance(fact, Idioma) and fact['idioma'] == idioma]

    @Rule(RecomendacionPais(aspectos=MATCH.aspectos))
    def recomendar_por_aspectos(self, aspectos):
        for aspecto in aspectos:
            aspecto = aspecto.strip()  # Eliminar espacios en blanco alrededor
            self.recomendaciones_aspectos.extend([fact['pais'] for fact in self.facts.values() if isinstance(fact, AspectoTuristico) and fact['aspecto'] == aspecto])

    def priorizar_recomendaciones(self):
        paises_puntuacion = {}
        
        for pais in set(self.recomendaciones_clima + self.recomendaciones_idioma + self.recomendaciones_aspectos):
            puntuacion = 0
            if pais in self.recomendaciones_clima:
                puntuacion += 1
            if pais in self.recomendaciones_idioma:
                puntuacion += 1
            if pais in self.recomendaciones_aspectos:
                puntuacion += 1
            paises_puntuacion[pais] = puntuacion
        
        recomendaciones_ordenadas = sorted(paises_puntuacion.items(), key=lambda x: x[1], reverse=True)
        return [pais for pais, puntuacion in recomendaciones_ordenadas[:4]]
