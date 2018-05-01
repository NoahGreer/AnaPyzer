# Import the AnaPyzerModel class
from anapyzermodel import *
# Import the AnaPyzerView class
from anapyzerview import *
# Import the AnaPyzerController class
from anapyzercontroller import *

# Entry point
# If the application is being run directly, rather than from another script
if __name__ == '__main__':
    # Instatiate the main application view object
    view = AnaPyzerView()
    # Instatiate the main application model object
    model = AnaPyzerModel()
    # Instantiate the main application controller object
    controller = AnaPyzerController(view, model)
    # Run the main application
    controller.run()
