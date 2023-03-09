#!/usr/bin/env python3

"""
Created by Nick Turner (@nickjvturner)


"""

import os
import zipfile
import json
import shutil
import time
from pathlib import Path
from PIL import Image, ImageDraw
from pprint import pprint


def main():
    def create_directory(new_dir):
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
            return f'Directory {new_dir} Created'
        else:
            return f'Directory {new_dir} already exists'

    nl = '\n'

    # Get filename and current working directory
    print(f'{nl}{Path(__file__).name}')
    print(f'working_directory: {Path.cwd()}{nl}')

    # Get local file with extension .esx
    for file in sorted(Path.cwd().iterdir()):
        # ignore files in directory containing _re-zip
        if (file.suffix == '.esx') and (not('re-zip' in file.stem)):
            proceed = input(f'Proceed with file: {str(file.name)}? (YES/no)')
            if proceed == 'no':
                continue

            print('filename:', file.name)

            # Define the project name
            project_name = file.stem
            print('project_name:', project_name)

            # Unzip the .esx project file into folder named {project_name}
            with zipfile.ZipFile(file.name, 'r') as zip_ref:
                zip_ref.extractall(project_name)
            print('project successfully unzipped')

            # Load the floorPlans.json file into the floorPlansJSON Dictionary
            with open(Path(project_name) / 'floorPlans.json') as json_file:
                floorPlans = json.load(json_file)
            # pprint(floorPlans)

            # Create an intermediary dictionary to lookup floor names
            floorPlansDict = {}

            # Populate the intermediary dictionary with {floorId: floor name}
            for floor in floorPlans['floorPlans']:
                floorPlansDict[floor['id']] = floor['name']
            # pprint(floorPlansDict)

            def floorPlanGetter(floorPlanId):
                # print(floorPlansDict.get(floorPlanId))
                return floorPlansDict.get(floorPlanId)

            # Load the simulatedRadios.json file into the simulatedRadios dictionary
            with open(Path(project_name) / 'simulatedRadios.json') as json_file:
                simulatedRadios = json.load(json_file)
            # pprint(simulatedRadios)

            # Create an intermediary dictionary to lookup AP radio parameters
            apDirectionDict = {}

            # Populate the intermediary dictionary
            for radio in simulatedRadios['simulatedRadios']:
                # print(radio)
                # print(radio['accessPointId'])
                # print(radio['antennaDirection'])
                apDirectionDict[radio['accessPointId']] = radio['antennaDirection']
            # pprint(apDirectionDict)

            def apDirectionGetter(accessPointId):
                # print(floorPlansDict.get(floorPlanId))
                return apDirectionDict.get(accessPointId)

            # Load the accessPoints.json file into the accessPoints dictionary
            with open(Path(project_name) / 'accessPoints.json') as json_file:
                accessPoints = json.load(json_file)
            # pprint(accessPoints)

            create_directory(Path.cwd() / 'OUTPUT')

            # Plain floor plan destination
            plain_floorplan_destination = Path.cwd() / 'OUTPUT' / 'blank'
            create_directory(plain_floorplan_destination)

            zoomed_AP_destination = Path.cwd() / 'OUTPUT' / 'zoomed-APs'
            create_directory(zoomed_AP_destination)


            # Import custom icons
            arrow = Image.open('arrow.png')
            spot = Image.open('spot.png')

            # Resize icons if necessary (default size is 350x350 px)
            icon_resize = 200

            arrow = arrow.resize((icon_resize, icon_resize))
            spot = spot.resize((icon_resize, icon_resize))

            # Define the centre point of the icons
            icon_centre = (arrow.width // 2, arrow.height // 2)

            crop_size = 1200

            for floor in floorPlans['floorPlans']:
                # Extract floorplans
                # print(floor['id'])
                shutil.copy((Path(project_name) / ('image-' + floor['imageId'])), Path(plain_floorplan_destination / floor['name']).with_suffix('.png'))
                shutil.copy((Path(project_name) / ('image-' + floor['imageId'])), floor['imageId'])

                # Open the image file
                image = Image.open(floor['imageId'])

                for ap in accessPoints['accessPoints']:
                    # print(ap['location']['floorPlanId'])
                    if ap['location']['floorPlanId'] == floor['id']:

                        # establish x and y
                        x, y = (ap['location']['coord']['x'], ap['location']['coord']['y'])

                        print(f"[[ {ap['name']} [{ap['model']}]] from: {floorPlanGetter(ap['location']['floorPlanId'])} ]"
                              f"has coordinates {x}, {y} {nl}")

                        # Calculate the top-left corner of the icon based on the center point and the location
                        top_left = (int(x) - icon_centre[0], int(y) - icon_centre[1])

                        angle = apDirectionGetter(ap['id'])
                        print(angle)

                        if angle != 0.0:
                            rotated_arrow = arrow.rotate(angle, expand=True)
                            image.paste(rotated_arrow, top_left, mask=rotated_arrow)

                        else:
                            # Paste the arrow onto the floorplan at the calculated location
                            image.paste(spot, top_left, mask=spot)

                        # Calculate the crop box for the new image
                        crop_box = (x - crop_size // 2, y - crop_size // 2, x + crop_size // 2, y + crop_size // 2)

                        # Crop the image
                        cropped_image = image.crop(crop_box)

                        # Save the cropped image with a new filename
                        cropped_image.save(Path(zoomed_AP_destination / (ap['name'] + '-zoomed')).with_suffix('.png'))

                # Remove raw floorplan source files
                os.remove(floor['imageId'])

                # Annotated floor plan destination
                annotated_floorplan_destination = Path.cwd() / 'OUTPUT' / 'annotated'
                create_directory(annotated_floorplan_destination)

                # Save the modified image
                image.save(Path(annotated_floorplan_destination / floor['name']).with_suffix('.png'))

            try:
                shutil.rmtree(project_name)
                print(f'Temporary project contents directory removed{nl}')
            except Exception as e:
                print(e)


if __name__ == "__main__":
    start_time = time.time()
    main()
    run_time = time.time() - start_time
    print(f'** Time to run: {round(run_time, 2)} seconds **')
