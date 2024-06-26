# Fuzzy y-axis.py

from common import model_sort_order

SPLIT_BOUNDARY_GROUPS = True  # flag attribute
BOUNDARY_SEPARATOR = True  # flag attribute
BOUNDARY_ORIENTATION = 'horizontal'  # flag attribute

ONE_LINER_DESCRIPTION = 'APs sorted by: floor, model, y-axis in rows, x-axis value'

BOUNDARY_SEPARATOR_TOOLTIP = ('Dynamic Rows divides the map into horizontal rows.\n'
                              'The Boundary Separator value defines the height in pixels of the rows\n'
                              'APs within each row are sorted and numbered from left to right')

SHORT_DESCRIPTION = f"""Intended for simulated APs

Sorts APs by:
    floor name,
    model,
    y-axis in rows,
    x-axis value

AP-001, AP-002, AP-003..."""

LONG_DESCRIPTION = f"""This renaming function works by:
placing all project APs into a list

initially sorting the list by:
    floor name,
    y-axis value

the APs are then iterated through and assigned to a group
based on their x-axis value
the first AP in the list defines the start of the first group
subsequent APs with an x-axis value within the threshold
are also assigned to the first group
when an AP with an x-axis value greater than the threshold is found
a new group is started
the assessment of APs continues
eventually all APs are assigned to a group
    
the list is re-sorted by:
    floor name,
    model,
    y-axis in 'rows',
    x-axis value
    
the sorted list is iterated through and a new AP Name is assigned
AP numbering starts at 1, with:

resulting AP names will look like:
    AP-001, AP-002, AP-003...
"""


def sort_logic(access_points_list, floor_plans_dict, y_axis_threshold, output_boundaries=False):
    # First, sort APs by floor name (via floorPlanId) and then by y-coordinate.
    access_points_list_sorted = sorted(access_points_list, key=lambda ap: (
                                    floor_plans_dict.get(ap['location']['floorPlanId']).get('name', ''),
                                    ap['location']['coord']['y']))

    # Initialize variables for grouping.
    y_coordinate_group = 1
    current_group_start_y = None
    current_floor_id = None
    boundaries = []

    for ap in access_points_list_sorted:
        ap_floor_id = ap['location']['floorPlanId']  # Get the current AP's floor ID.

        if current_floor_id is None:
            # First AP in the list defines the start of the first group and floor.
            current_floor_id = ap_floor_id

        elif current_floor_id != ap_floor_id:
            # Floor has changed, reset the group counter and update current floor ID.
            y_coordinate_group = 1
            current_group_start_y = None  # Reset group start Y coordinate.
            current_floor_id = ap_floor_id

        if current_group_start_y is None:
            # This is either the first AP or the first AP of a new floor.
            current_group_start_y = ap['location']['coord']['y']
            boundaries.append(current_group_start_y)

        elif (ap['location']['coord']['y'] - current_group_start_y) > y_axis_threshold:
            while (ap['location']['coord']['y'] - current_group_start_y) > y_axis_threshold:
                # Current AP's y-coordinate is outside the threshold of the current group; start a new group.
                y_coordinate_group += 1
                current_group_start_y += y_axis_threshold
                boundaries.append(current_group_start_y)

        # Assign group ID to the AP.
        ap['location']['coord']['y_group'] = y_coordinate_group

    # Final sorting by group ID, then x-coordinate within each group.
    access_points_list_sorted = sorted(access_points_list_sorted,
                                       key=lambda i: (floor_plans_dict.get(i['location']['floorPlanId']).get('name'),
                                                      model_sort_order.get(i['model'], i['model']),
                                                      i['location']['coord']['y_group'],
                                                      i['location']['coord']['x']))

    if output_boundaries:
        # Calculate the center for the last group.
        return access_points_list_sorted, boundaries, 'horizontal'

    return access_points_list_sorted
