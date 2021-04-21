#Test script for image capture
import requests

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    urls = [
        "http://navigator-c2c.dot.ga.gov/snapshots/ATL-CAM-909.jpg",
        "http://navigator-c2c.dot.ga.gov/snapshots/ATL-CAM-939.jpg",
        "http://navigator-c2c.dot.ga.gov/snapshots/ATL-CAM-085.jpg",
        "http://navigator-c2c.dot.ga.gov/snapshots/ATL-CAM-974.jpg",
        "http://navigator-c2c.dot.ga.gov/snapshots/GDOT-CAM-017.jpg"
    ]
    index = 0
    for url in urls:
        r = requests.get(url)
        #Replace with the directory you want to save the images in. 
        filename = r"C:\Users\user\Documents\ATL Traffic\TestDirectory\March 19, 2021" + chr(92) + r"ATL-CAM-" + str(index) + r".jpg"
        print(filename)
        index += 1
        with open(filename, "wb") as f:
            f.write(r.content)