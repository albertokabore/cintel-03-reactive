"""
Penguin Dashboard App
An interactive web app to explore Palmer Penguins dataset
"""

import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny import render
import seaborn as sns
import pandas as pd
from palmerpenguins import load_penguins

# Load penguin data
penguins_df = load_penguins()

# Create sidebar for user inputs
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    
    # Dropdown to select attribute
    ui.input_selectize(
        "selected_attribute",
        "Select Attribute:",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    )
    
    # Numeric input for Plotly bins
    ui.input_numeric(
        "plotly_bin_count",
        "Plotly Bin Count:",
        20
    )
    
    # Slider for Seaborn bins
    ui.input_slider(
        "seaborn_bin_count",
        "Seaborn Bin Count:",
        5, 30, 15
    )
    
    # Checkbox group for species selection
    ui.input_checkbox_group(
        "selected_species_list",
        "Filter Species:",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True
    )
    
    ui.hr()
    
    # GitHub link
    ui.a(
        "GitHub",
        href="https://github.com/yourusername/cintel-02-data",
        target="_blank"
    )

# Main content area
ui.h1("Palmer Penguins Dashboard")

# First row with data tables
with ui.layout_columns():
    @render.data_frame
    def penguins_datatable():
        return penguins_df

    @render.data_frame
    def penguins_datagrid():
        return render.DataGrid(penguins_df, filters=True)

# Second row with histograms
with ui.layout_columns():
    @render_plotly
    def plotly_histogram():
        filtered_df = penguins_df[penguins_df["species"].isin(input.selected_species_list())]
        fig = px.histogram(
            filtered_df,
            x=input.selected_attribute(),
            nbins=input.plotly_bin_count(),
            color="species",
            title="Plotly Histogram"
        )
        return fig

    @render.plot
    def seaborn_histogram():
        filtered_df = penguins_df[penguins_df["species"].isin(input.selected_species_list())]
        plot = sns.histplot(
            data=filtered_df,
            x=input.selected_attribute(),
            bins=input.seaborn_bin_count(),
            hue="species",
            multiple="stack"
        )
        plot.set_title("Seaborn Histogram")
        return plot

# Third row with scatterplot in full-screen card
with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")
    
    @render_plotly
    def plotly_scatterplot():
        filtered_df = penguins_df[penguins_df["species"].isin(input.selected_species_list())]
        fig = px.scatter(
            filtered_df,
            x="bill_length_mm",
            y="bill_depth_mm",
            color="species",
            size="body_mass_g",
            hover_data=["island", "sex"],
            title="Bill Length vs Bill Depth"
        )
        return fig
