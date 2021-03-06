# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the LGPLv3 or higher.

from UM.Scene.SceneNode import SceneNode

from . import Operation

##  An operation that moves a scene node.
#
#   This has nothing to do with languages. It is a linear transformation on
#   geometry.
class TranslateOperation(Operation.Operation):
    ##  Initialises this TranslateOperation.
    #
    #   \param node The node to translate.
    #   \param translation A translation matrix to transform the node by.
    #   \param set_position: Whether to change the position (True) or add the
    #   positions, making a relative move (False).
    def __init__(self, node, translation, set_position = False):
        super().__init__()
        self._node = node
        self._old_transformation = node.getLocalTransformation() # To restore the transformation to in case of an undo.
        self._translation = translation
        self._set_position = set_position

    ##  Undoes the translate operation, restoring the old transformation.
    def undo(self):
        self._node.setTransformation(self._old_transformation)

    ##  Re-applies the translate operation.
    def redo(self):
        if self._set_position: # Change the position to the new position.
            self._node.setPosition(self._translation, SceneNode.TransformSpace.World)
        else: # Add the translation to the current position.
            self._node.translate(self._translation, SceneNode.TransformSpace.World)

    ##  Merges this operation with another translate operation.
    #
    #   This prevents the user from having to undo multiple operations if they
    #   were not his operations.
    #
    #   You should ONLY merge this operation with an older operation. It is NOT
    #   symmetric.
    #
    #   \param other The older translate operation to merge this operation with.
    def mergeWith(self, other):
        if type(other) is not TranslateOperation:
            return False
        if other._node != self._node: # Must be moving the same node.
            return False

        op = TranslateOperation(self._node, self._translation + other._translation)
        op._old_transformation = other._old_transformation # Use the oldest transformation of the two to restore if we undo.
        return op

    ##  Returns a programmer-readable representation of this operation.
    #
    #   \return A programmer-readable representation of this operation.
    def __repr__(self):
        return "TranslateOperation(node = {0}, translation={1})".format(self._node, self._translation)
