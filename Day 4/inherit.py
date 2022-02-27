class Shape():
    def __init__(self, name: str, edge: int, vertice: int):
        self.name = name
        self.edge = edge
        self.vertice = vertice


Shape1 = Shape("Rectangle", 4, 4)
print(Shape1.name)

# Inherit from Shape class
class Shape3d(Shape):
    def __init__(self, name: str, edge: int, vertice: int, faces: int):
        super().__init__(name, edge, vertice)
        self.faces = faces


Shape2 = Shape3d("Cuboid", 12, 8, 6)
print(Shape2.faces)