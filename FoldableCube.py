import importlib
import pydeation.imports
importlib.reload(pydeation.imports)
from pydeation.imports import *


class FoldableCube(CustomObject):
    """The foldable cube object consists of four individual rectangles forming the front, back, right, and left faces of a cube which can fold away using a specified parameter"""
    
    def __init__(self, color=BLUE, bottom=True, drive_opacity=True, fold_angle=PI/2, **kwargs):
        self.color = color
        self.bottom = bottom
        self.drive_opacity = drive_opacity
        self.fold_angle = fold_angle
        super().__init__(**kwargs)

    def specify_parts(self):
        # Define the rectangles without positions
        self.front_rectangle = Rectangle(z=50, plane="xz", creation=True, color=self.color, name="FrontRectangle")
        self.back_rectangle = Rectangle(z=-50, plane="xz", creation=True, color=self.color, name="BackRectangle")
        self.right_rectangle = Rectangle(x=50, plane="xz", creation=True, color=self.color, name="RightRectangle")
        self.left_rectangle = Rectangle(x=-50, plane="xz", creation=True, color=self.color, name="LeftRectangle")
        
        # Define groups with position attributes for transformations
        self.front_axis = Group(self.front_rectangle, z=50, name="FrontAxis")
        self.back_axis = Group(self.back_rectangle, z=-50, name="BackAxis")
        self.right_axis = Group(self.right_rectangle, x=50, name="RightAxis")
        self.left_axis = Group(self.left_rectangle, x=-50, name="LeftAxis")
        
        # Add all parts to the parts list
        self.parts += [self.front_axis, self.back_axis, self.right_axis, self.left_axis]

        if self.bottom:
            self.bottom_rectangle = Rectangle(plane="xz", creation=True, color=self.color, name="BottomRectangle")
            self.parts.append(self.bottom_rectangle)

    def specify_parameters(self):
        self.fold_parameter = UCompletion(name="Fold", default_value=0)
        self.parameters += [self.fold_parameter]

    def specify_relations(self):
        # Relations for folding the rectangles into position to form the cube sides
        self.front_relation = XRelation(part=self.front_axis, whole=self, desc_ids=[ROT_P],
                                        parameters=[self.fold_parameter], formula=f"PI/2-{self.fold_angle} * (1-{self.fold_parameter.name})")
        self.back_relation = XRelation(part=self.back_axis, whole=self, desc_ids=[ROT_P],
                                        parameters=[self.fold_parameter], formula=f"-(PI/2-{self.fold_angle} * (1-{self.fold_parameter.name}))")
        self.right_relation = XRelation(part=self.right_axis, whole=self, desc_ids=[ROT_B],
                                        parameters=[self.fold_parameter], formula=f"-(PI/2-{self.fold_angle} * (1-{self.fold_parameter.name}))")
        self.left_relation = XRelation(part=self.left_axis, whole=self, desc_ids=[ROT_B],
                                       parameters=[self.fold_parameter], formula=f"PI/2-{self.fold_angle} * (1-{self.fold_parameter.name})")

    def specify_creation(self):
        # Define the creation action for the foldable cube
        if self.drive_opacity:
            movements = [
                Movement(self.fold_parameter, (0, 1), output=(0, 1)),
                Movement(self.front_rectangle.opacity_parameter, (1/3, 1), output=(0, 1), part=self.front_rectangle),
                Movement(self.back_rectangle.opacity_parameter, (1/3, 1), output=(0, 1), part=self.back_rectangle),
                Movement(self.right_rectangle.opacity_parameter, (1/3, 1), output=(0, 1), part=self.right_rectangle),
                Movement(self.left_rectangle.opacity_parameter, (1/3, 1), output=(0, 1), part=self.left_rectangle)
            ]
            if self.bottom:
                movements.append(Movement(self.bottom_rectangle.opacity_parameter, (1/3, 1), output=(0, 1), part=self.bottom_rectangle))
            creation_action = XAction(*movements, target=self, completion_parameter=self.creation_parameter, name="Creation")
        else:
            movements = [
                Movement(self.fold_parameter, (0, 1), output=(0, 1)),
                Movement(self.front_rectangle.creation_parameter, (1/3, 1), output=(0, 1), part=self.front_rectangle),
                Movement(self.back_rectangle.creation_parameter, (1/3, 1), output=(0, 1), part=self.back_rectangle),
                Movement(self.right_rectangle.creation_parameter, (1/3, 1), output=(0, 1), part=self.right_rectangle),
                Movement(self.left_rectangle.creation_parameter, (1/3, 1), output=(0, 1), part=self.left_rectangle)
            ]
            if self.bottom:
                movement.append(Movement(self.bottom_rectangle.creation_parameter, (1/3, 1), output=(0, 1), part=self.bottom_rectangle))
            creation_action = XAction(*movements, target=self, completion_parameter=self.creation_parameter, name="Creation")


if __name__ == "__main__":
    foldable_cube = FoldableCube(creation=True, fold_angle=2*PI, bottom=False, drive_opacity=True)