from repository import Repository
from controllers import VentasController
from views import VentasView

def main():
    # Inicializar capas con Repository real que usa SQLite
    repository = Repository()
    controller = VentasController(repository)
    view = VentasView(controller)
    
    # Iniciar la aplicación
    view.run()

if __name__ == "__main__":
    main()
