from repository import VentasRepository
from controllers import VentasController
from views import VentasView

def main():
    # Inicializar capas
    repository = VentasRepository()
    controller = VentasController(repository)
    view = VentasView(controller)
    
    # Iniciar la aplicación
    view.run()

if __name__ == "__main__":
    main() 