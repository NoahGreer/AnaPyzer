# Import the AnaPyzerModel class
from anapyzermodel import AnaPyzerModel
# Import the AnaPyzerView class
from anapyzerview import AnaPyzerView
# Import the AnaPyzerController class
from anapyzercontroller import AnaPyzerController
from anapyzeranalyzer import AnaPyzerAnalyzer

# Entry point
# If the application is being run directly, rather than from another script
if __name__ == '__main__':
    # Instantiate the main application model object
    model = AnaPyzerModel()
    # Instantiate the main application view object
    view = AnaPyzerView()
    analyzer = AnaPyzerAnalyzer()
    # Instantiate the main application controller object
    controller = AnaPyzerController(model, view, analyzer)
    # Run the main application
    controller.run()
