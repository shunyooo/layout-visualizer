from pydantic import BaseModel

numeric = int | float


class BBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def x1y1(self) -> tuple[float, float]:
        return (self.x1, self.y1)

    @property
    def x1y1x2y2(self) -> tuple[float, float, float, float]:
        return (self.x1, self.y1, self.x2, self.y2)

    @property
    def wh(self) -> tuple[float, float]:
        return (self.x2 - self.x1, self.y2 - self.y1)

    @staticmethod
    def from_x1y1x2y2(x1y1x2y2: tuple[numeric, numeric, numeric, numeric]) -> "BBox":
        """Create BBox from tuple (x1, y1, x2, y2)"""
        x1, y1, x2, y2 = [float(v) for v in x1y1x2y2]
        return BBox(x1=x1, y1=y1, x2=x2, y2=y2)

    @staticmethod
    def from_xywh(x1y1: tuple[numeric, numeric], wh: tuple[numeric, numeric]) -> "BBox":
        """Create BBox from tuple (x1, y1) and (w, h)"""
        x1, y1, w, h = [float(v) for v in x1y1 + wh]
        return BBox(x1=x1, y1=y1, x2=x1 + w, y2=y1 + h)

    def shift(self, x: float = 0, y: float = 0) -> "BBox":
        """Shift BBox"""
        return BBox(
            x1=self.x1 + x,
            y1=self.y1 + y,
            x2=self.x2 + x,
            y2=self.y2 + y,
        )

    def pad(
        self,
        left: float = 0,
        top: float = 0,
        right: float = 0,
        bottom: float = 0,
    ) -> "BBox":
        """Add padding to BBox"""
        return BBox(
            x1=self.x1,
            y1=self.y1,
            x2=self.x2 + left + right,
            y2=self.y2 + top + bottom,
        )

    def is_collision(self, other: "BBox") -> bool:
        """Check collision with other BBox"""
        return not (
            self.x2 < other.x1
            or self.x1 > other.x2
            or self.y2 < other.y1
            or self.y1 > other.y2
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(x1={self.x1}, y1={self.y1},"
            f" x2={self.x2}, y2={self.y2})"
        )
