import uuid

from mmath.linearalgebra.Vector import Vector


class Node:
    def __init__(self, refVec: Vector, error: float):
        self.__id = None
        self.__refVec: Vector = refVec
        self.__error = error

    def getRefVec(self) -> Vector:
        return self.__refVec

    def getError(self) -> float:
        return self.__error

    def updateError(self, updatedError: float) -> None:
        self.__error = updatedError

    def updateRefVec(self, refVec: Vector) -> None:
        self.__refVec = refVec

    def getId(self) -> uuid.UUID:
        return self.__id

    def updateId(self, newId: uuid.UUID) -> None:
        self.__id = newId
