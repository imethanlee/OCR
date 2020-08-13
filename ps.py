import cv2


class PS:
    def __init__(self, file_name):
        self.file_name = file_name
        self.img = cv2.imread(None)
        self.rotated_img = cv2.imread(None)
        self.point1 = []
        self.point2 = []
        self.curr_angle = 0
        self.origin_x = 0

    def on_mouse(self, event, x, y, flags, param):
        img2 = self.rotated_img.copy()
        if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
            self.point1 = (x, y)
            cv2.circle(img2, self.point1, 10, (0, 255, 0), 5)
            cv2.imshow('Photoshop Mini', img2)
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
            cv2.rectangle(img2, self.point1, (x, y), (255, 0, 0), 5)
            cv2.imshow('Photoshop Mini', img2)
        elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
            self.point2 = (x, y)
            cv2.rectangle(img2, self.point1, self.point2, (0, 0, 255), 5)
            cv2.imshow('Photoshop Mini', img2)
            min_x = min(self.point1[0], self.point2[0])
            min_y = min(self.point1[1], self.point2[1])
            width = abs(self.point1[0] - self.point2[0])
            height = abs(self.point1[1] - self.point2[1])
            cut_img = self.rotated_img[min_y:min_y + height, min_x:min_x + width]
            # cv2.imwrite("temp.jpg", cut_img)
            cv2.imwrite(self.file_name, cut_img)
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.origin_x = x
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_RBUTTON):
            # 获取旋转角度
            angle = self.get_angle(self.origin_x, x)
            rows, cols, channels = self.img.shape
            rotate = cv2.getRotationMatrix2D((cols * 0.5, rows * 0.5), self.curr_angle + angle, 1)
            self.rotated_img = cv2.warpAffine(self.img, rotate, (cols, rows))
            cv2.imshow('Photoshop Mini', self.rotated_img)
        elif event == cv2.EVENT_RBUTTONUP:
            self.curr_angle = self.curr_angle + self.get_angle(self.origin_x, x)

    def run(self):
        self.img = cv2.imread(self.file_name)
        self.rotated_img = self.img
        cv2.namedWindow('Photoshop Mini')
        cv2.setMouseCallback('Photoshop Mini', self.on_mouse)
        cv2.imshow('Photoshop Mini', self.img)
        cv2.waitKey(0)

    @staticmethod
    def get_angle(old, new):
        return 0.15 * (old - new)


# ps = PS("./test_case/card.jpg")
# ps.run()

# print(sql_query(OCR.BUSINESS_LICENSE, "4105"))

