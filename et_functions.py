import os
import xlsxwriter
import visuals
import perfonitor.calculations


def create_event_tracker_file(final_df_to_add, incidents, component_data, df_all_irradiance, df_all_export, budget_pr,
                              budget_export, budget_irradiance, period_list):

    # <editor-fold desc="Calculate Availability & PR">
    print("Calculating Availability in periods")

    # <editor-fold desc="Calculate availability per period">
    availability_fleet_per_period = {}
    raw_availability_fleet_per_period = {}
    active_hours_fleet_per_period = {}
    incidents_corrected_fleet_period_per_period = {}

    for period in period_list:
        availability_period_df, raw_availability_period_df, activehours_period_df, incidents_corrected_period, date_range = \
            perfonitor.calculations.availability_in_period(incidents, period, component_data, df_all_irradiance,
                                                           df_all_export, budget_pr, irradiance_threshold=20,
                                                           timestamp=15)

        availability_fleet_per_period[period] = availability_period_df
        raw_availability_fleet_per_period[period] = raw_availability_period_df
        active_hours_fleet_per_period[period] = activehours_period_df
        incidents_corrected_fleet_period_per_period[period] = incidents_corrected_period
    # </editor-fold>

    print("Calculating Performance KPIs in periods")
    # <editor-fold desc="Calculate site pr per period">
    performance_fleet_per_period = {}

    for period in period_list:
        incidents_period = incidents_corrected_fleet_period_per_period[period]
        availability_period = availability_fleet_per_period[period]
        raw_availability_period = raw_availability_fleet_per_period[period]

        data_period_df = perfonitor.calculations.pr_in_period(incidents_period, availability_period,
                                                              raw_availability_period,
                                                              period, component_data,
                                                              df_all_irradiance, df_all_export, budget_pr,
                                                              budget_export,
                                                              budget_irradiance, irradiance_threshold=20,
                                                              timestamp=15)

        performance_fleet_per_period[period] = data_period_df.sort_index()
    # </editor-fold>
    # </editor-fold>

    # <editor-fold desc="Create Graphs & Visuals">
    # File Creation - step 2 create graphs & visuals
    print("Creating graphs and visual aids")
    graphs = {}
    for period in period_list:
        period_graph = visuals.availability_visuals(availability_fleet_per_period, period, folder_img)
        graphs[period] = period_graph
    # </editor-fold>

    # <editor-fold desc="Create file">
    # File Creation - step 3 actually create file
    print("Creating file...")

    perfonitor.file_creation.create_event_tracker_file_all(final_df_to_add, dest_file,
                                                           performance_fleet_per_period, site_capacities,
                                                           dict_fmeca_shapes)
    # </editor-fold>


    return