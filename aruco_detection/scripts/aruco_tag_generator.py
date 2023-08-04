#!/usr/bin/env python3
import cv2
import argparse

def generate_single_marker(aruco_dict, marker_size, marker_id):
#    marker_size = int(input("Enter the marker size: "))
#    marker_id = int(input("Enter the marker ID: "))

   marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id,
    marker_size)

   cv2.imwrite("marker_{}.png".format(marker_id), marker_img)

   marker_img = cv2.imread("marker_{}.png".format(marker_id))

   cv2.imshow("Marker", marker_img)

   print("Dimensions:", marker_img.shape)

   cv2.waitKey(0)


def generate_bulk_markers(aruco_dict, marker_size, num_markers):
   marker_size = int(input("Enter the marker size: "))
   num_markers = int(input("Enter the number of markers to generate: "))
   marker_imgs = []

   for marker_id in range(num_markers):
    #    calculate pixel numbers with respect to centimeters when printing
       marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id,
        marker_size)

       cv2.imwrite("marker_{}.png".format(marker_id), marker_img)
       marker_imgs.append(cv2.imread("marker_{}.png".format(marker_id)))

   for marker_img in marker_imgs:
       cv2.imshow("Marker", marker_img)
       print("Dimensions:", marker_img.shape)
       cv2.waitKey(0)


# generate a grid board with aruco markers
def generate_aruco_board(aruco_dict, marker_X, marker_Y, marker_length, marker_separation, margins, border_bits):

    # settings for printing out aruco board
    print_width = marker_X * (marker_length + marker_separation) - marker_separation + 2 * margins
    print_height = marker_Y * (marker_length + marker_separation) - marker_separation + 2 * margins
    imageSize = [print_width, print_height]
    board = cv2.aruco.GridBoard_create(marker_X, marker_Y, marker_length, marker_separation, aruco_dict)
    board_img = cv2.drawPlanarBoard(board, imageSize, 'MarginSize', margins, 'BorderBits', border_bits)
    cv2.imshow(board_img)

    # save image
    # cv2.imwrite(board_img, 'GridBoard.png')


# save aruco board settings to a .yml file
def generate_yml_file(aruco_dict, marker_X, marker_Y, marker_length, marker_separation):
    file_name = input("Please enter the file name for saving a .yml file: ")
    yml_content = [
        "dictionary: " + aruco_dict,
        "marker_x: "+ marker_X,
        "marker_y: "+ marker_Y,
        "marker_length: "+ marker_length,
        "marker_separation: "+ marker_separation
    ]
    with open(file_name+".yml", 'w') as f:
        f.writelines(yml_content)


def main():
   
# aruco dictionary lookup table
   aruco_dict_lookup = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL}
   
   parser = argparse.ArgumentParser(
                    prog='ArucoTagGenerator',
                    description='Generate Aruco tags',
                    epilog='Enjoy the program! :)')
   
   parser.add_argument("-d", "--dictionary", type=str, default="DICT_4X4_50")
   parser.add_argument("-s", "--size", type=int, default=200)
   parser.add_argument("-x", "--x", type=int, default=4)      # numbers of markers in x direction
   parser.add_argument("-y", "--y", type=int, default=3)      # numbers of markers in y direction
   parser.add_argument("-l", "--length", type=int, default=1)    # marker length in centimeters
   parser.add_argument("-sep", "--separation", type=int, default=1)    # separation between markers in centimeters
   parser.add_argument("-ma", "--margins", type=int, default=1)    # margins of the board in centimeters default is 1cm
   parser.add_argument("-bits", "--borderbits", type=int, default=1)    # bits of the board default is 1

   parser.add_argument("-id", "--id", type=int, default=0)
   parser.add_argument("-m", "--mode", type=int, default=3)   # 1 for single marker, 2 for bulk markers, 3 for aruco board
   parser.add_argument("-p", "--printdict", type=bool, default=False)   # print the dictionary options of aruco tags for reference

   args = parser.parse_args()
#    aruco_dict = aruco_dict_lookup[args.dictionary]
   aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_lookup[args.dictionary])
   marker_X = args.x
   marker_Y = args.y
   marker_length = args.length
   marker_separation = args.separation
   marker_size = args.size
   marker_id = args.id
   margins = args.margins
   border_bits = args.borderbits
   marker_mode = args.mode
   need_help = args.printdict
   

   if need_help == False:
        if marker_mode == 1:
            generate_single_marker(aruco_dict, marker_size, marker_id)
        elif marker_mode == 2:
            generate_bulk_markers(aruco_dict, marker_size, num_markers=5)
        elif marker_mode == 3:
            generate_aruco_board(aruco_dict, marker_X, marker_Y, marker_length, marker_separation, margins, border_bits)
            generate_yml_file(aruco_dict, marker_X, marker_Y, marker_length, marker_separation)
        else:
            print("Invalid input. Please try again.")


if __name__ == "__main__":
   main()