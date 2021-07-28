import cv2
import numpy as np
import track_line

MIN_LINE_LENGTH = 600  # change this value according to the accuracy of required track length
MIN_LINE_INTERSECTIONS = 15
MAX_LINE_GAP = 10
DRAW_LINE_THICKNESS = 2
DRAW_LINE_COLOR = (255, 255, 255)
SOBEL_MASK_SIZE = 5
DUPLICATE_LINE_DISTANCE_Y_AXIS = 10
HORIZONTAL_LINE_THRESHOLD = 10
KERNEL = np.ones((5, 5), np.uint8)


class WabTecTrack:

    def __init__(self, file_name):
        self.file_name = file_name
        self.img = cv2.imread(self.file_name, cv2.IMREAD_GRAYSCALE)
        self.MIN_LINE_LENGTH = self.img.shape[1] // 6;

    def get_lines(self):
        all_lines = self.__find_all_lines()
        lines = self.__remove_duplicate_lines_and_vertical_lines(all_lines)
        tracks = self.__get__track_lines(lines)
        longest_lines = self.__remove_lines_close_by(tracks)
        return longest_lines

    def __find_all_lines(self):
        LOW_THRESHOLD = 0
        HIGH_THRESHOLD = 10  # LOW_THRESHOLD * 3;
        edges = cv2.Canny(self.img, LOW_THRESHOLD, HIGH_THRESHOLD, apertureSize=SOBEL_MASK_SIZE)

        # rho = 1  # distance resolution in pixels of the Hough grid
        # theta = np.pi / 180  # angular resolution in radians of the Hough grid
        # threshold = 15  # minimum number of votes (intersections in Hough grid cell)
        # min_line_length = 50  # minimum number of pixels making up a line
        # max_line_gap = 20  # maximum gap in pixels between connectable line segments

        lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=MIN_LINE_INTERSECTIONS,
                                lines=np.array([]),
                                minLineLength=MIN_LINE_LENGTH, maxLineGap=MAX_LINE_GAP)

        return lines

    def __remove_duplicate_lines_and_vertical_lines(self, lines):
        duplicate_list = []
        for i in range(0, lines.shape[0]):
            for j in range((i + 1), lines.shape[0]):
                # if (abs(lines[i][0][1] - lines[j][0][3]) < DUPLICATE_LINE_DISTANCE_Y_AXIS):
                #   duplicate_list.append(j)
                if (abs(lines[j][0][1] - lines[j][0][3]) > HORIZONTAL_LINE_THRESHOLD):  # not a horizontal line
                    duplicate_list.append(j)

        duplicate_list = sorted(duplicate_list, reverse=True)

        for j in duplicate_list:  # remove duplicate lines
            if (j < lines.shape[0]):
                lines = np.delete(lines, j, axis=0)

        return lines

    def __remove_lines_close_by(self, line_list):

        line_list.sort(key=lambda x: x.y1, reverse=False)

        filter_list = [[]]
        prev_obj = track_line.TrackLine(0, 0, 0, 0)
        next_obj = track_line.TrackLine(0, 0, 0, 0)
        cluster_no = 0

        for i in range(len(line_list)):
            if i == 0:
                filter_list[cluster_no].append(line_list[i])
                prev_obj = line_list[i]
            else:
                next_obj = line_list[i]
                if abs(next_obj.y1 - prev_obj.y1) > DUPLICATE_LINE_DISTANCE_Y_AXIS:
                    cluster_no = cluster_no + 1
                    filter_list.append([])

                filter_list[cluster_no].append(line_list[i])
                prev_obj = next_obj
                # next_obj = line_list[i]

        list_longest_lines = []

        for cluster in filter_list:
            list_cluster_lines = []
            longest = cluster[0]

            for i in range(1, len(cluster)):
                if longest.get_length() < cluster[i].get_length():
                    longest = cluster[i]

            list_longest_lines.append(longest)

        return list_longest_lines

    def draw_lines(self, lines, out_file, is_new_image=True):
        updated_image = np.zeros((self.img.shape[0], self.img.shape[1]), np.uint8)

        if not is_new_image:
            updated_image = self.img  # update the same image

        for ln in lines:
            cv2.line(updated_image, (ln.x1, ln.y1), (ln.x2, ln.y2), DRAW_LINE_COLOR, DRAW_LINE_THICKNESS, cv2.LINE_AA)

        cv2.imwrite(out_file, updated_image)

    def __get__track_lines(self, lines):
        line_list = []
        for i in range(0, lines.shape[0]):
            ln = track_line.TrackLine(lines[i][0][0], lines[i][0][1], lines[i][0][2], lines[i][0][3])
            line_list.append(ln)

        return line_list

    def __print_lines(lines):
        for i in range(0, lines.shape[0]):
            print('(x1:', str(lines[i][0][0]), ', y1:', str(lines[i][0][1]), '), (x2:', str(lines[i][0][2]), ', y2:',
                  str(lines[i][0][3]), ')')
