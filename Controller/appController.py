class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def get_list_interfaces(self):
        return self.model.get_list_interfaces()
        
