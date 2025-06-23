if __name__ == '__main__':
    from gui.app import MainApp
    app = MainApp()
    app.run()



"""
Todo:
-qrc files for images (q resource)
-figure out drag and drop
-writing all functionality while not editing the .ui
-consider converting .ui to .py (seems to be most common practice)
-for component classes: Lower level component class define parameters and what is conmnected to,
higher level gui class that inherits component and does gui manipulation
-create network class that holds all components and does the logic of the network
-should source include switching or should it be external? - what kind of multiplexing?
-related to above: bipartite entanglement source or multipartite (could get complicated)

"""