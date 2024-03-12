from layout_visualizer.model.bbox import BBox


class TestBBox:
    def test_bounding_box_properties(self):
        bbox = BBox(x1=10, y1=20, x2=30, y2=40)
        assert bbox.x1y1 == (10, 20)
        assert bbox.x1y1x2y2 == (10, 20, 30, 40)
        assert bbox.wh == (20, 20)

    def test_create_bbox_from_x1y1x2y2(self):
        x1y1x2y2 = (10, 20, 30, 40)
        bbox = BBox.from_x1y1x2y2(x1y1x2y2)
        assert bbox.x1 == 10
        assert bbox.y1 == 20
        assert bbox.x2 == 30
        assert bbox.y2 == 40

    def test_create_bbox_from_xywh(self):
        x1y1 = (10, 20)
        wh = (20, 20)
        bbox = BBox.from_xywh(x1y1, wh)
        assert bbox.x1 == 10
        assert bbox.y1 == 20
        assert bbox.x2 == 30
        assert bbox.y2 == 40

    def test_shift_bbox(self):
        bbox = BBox(x1=10, y1=20, x2=30, y2=40)
        shifted_bbox = bbox.shift(x=5, y=10)
        assert shifted_bbox.x1 == 15
        assert shifted_bbox.y1 == 30
        assert shifted_bbox.x2 == 35
        assert shifted_bbox.y2 == 50

    def test_pad_bbox(self):
        bbox = BBox(x1=10, y1=20, x2=30, y2=40)
        padded_bbox = bbox.pad(left=5, top=5, right=5, bottom=5)
        assert padded_bbox.x1 == 10
        assert padded_bbox.y1 == 20
        assert padded_bbox.x2 == 40
        assert padded_bbox.y2 == 50

    def test_collision_detection(self):
        bbox1 = BBox(x1=10, y1=20, x2=30, y2=40)
        bbox2 = BBox(x1=25, y1=35, x2=45, y2=55)
        bbox3 = BBox(x1=40, y1=50, x2=60, y2=70)
        assert bbox1.is_collision(bbox2)  # BBox 1 and BBox 2 overlap
        assert not bbox1.is_collision(bbox3)  # BBox 1 and BBox 3 do not overlap
