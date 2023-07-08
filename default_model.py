"""

Default Model: a dummy model composed by just 1 Square
which will be used by the force animation loading

Copyright (C) 2023 DooMMetaL

"""

class DefaultModel:
    def __init__(self, number_objects):
        self.self = DefaultModel
        self.number_objects = number_objects
        self.create_objects(number_objects=number_objects)
    
    def create_objects(self, number_objects):

        global number_of_objects
        number_of_objects = number_objects[0]
        global number_of_primitives
        number_of_primitives = [1] * number_of_objects

        global warning_load
        warning_load = f'LOADING DUMMY Model...'

        global vertices_created
        global normals_created
        global primitives_created

        vertices_created = []
        normals_created = []
        primitives_created = []

        for creation in range(0, number_of_objects):
            vertices = [[-500, 500, 0], [500, 500, 0], [500, -500, 0], [-500, -500, 0]]
            normals = [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]
            primitives = [{
                f'r0': 95, f'g0': 121, f'b0': 53, f'mode_val': b'\x00\x00', 
                f'normal0': 0, f'vertex0': 3, 
                f'normal1': 1, f'vertex1': 0, 
                f'normal2': 2, f'vertex2': 2,
                f'normal3': 3, f'vertex3': 1}]
            vertices_created.append(vertices)
            normals_created.append(normals)
            primitives_created.append(primitives)