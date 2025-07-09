"""
Penguin Dashboard App
An interactive web app to explore Palmer Penguins dataset
"""

import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny import render, reactive
import seaborn as sns
import pandas as pd
from palmerpenguins import load_penguins

# Load penguin data
penguins_df = load_penguins()

# Sidebar inputs
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    
    ui.input_selectize(
        "selected_attribute",
        "Select Attribute:",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    )
    
    ui.input_numeric(
        "plotly_bin_count",
        "Plotly Bin Count:",
        20
    )
    
    ui.input_slider(
        "seaborn_bin_count",
        "Seaborn Bin Count:",
        5, 30, 15
    )
    
    ui.input_checkbox_group(
        "selected_species_list",
        "Filter Species:",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True
    )
    
    ui.hr()
    
    ui.a(
        "GitHub",
        href="https://github.com/albertokabore/cintel-03-reactive",
        target="_blank"
    )

# Main title
ui.h1("Palmer Penguins Dashboard")

# First row – Data Table and Grid
with ui.layout_columns():
    @render.data_frame
    def penguins_datatable():
        return filtered_data()

    @render.data_frame
    def penguins_datagrid():
        return render.DataGrid(filtered_data(), filters=True)

# Second row – Histograms
with ui.layout_columns():
    @render_plotly
    def plotly_histogram():
        df = filtered_data().dropna(subset=[input.selected_attribute()])
        fig = px.histogram(
            df,
            x=input.selected_attribute(),
            nbins=input.plotly_bin_count(),
            color="species",
            title="Plotly Histogram"
        )
        return fig

    @render.plot
    def seaborn_histogram():
        df = filtered_data().dropna(subset=[input.selected_attribute()])
        plot = sns.histplot(
            data=df,
            x=input.selected_attribute(),
            bins=input.seaborn_bin_count(),
            hue="species",
            multiple="stack"
        )
        plot.set_title("Seaborn Histogram")
        return plot

# Third row – Scatterplot
with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        df = filtered_data().dropna(subset=[
            "bill_length_mm",
            "bill_depth_mm",
            "body_mass_g",
            "species",
            "island",
            "sex"
        ])
        fig = px.scatter(
            df,
            x="bill_length_mm",
            y="bill_depth_mm",
            color="species",
            size="body_mass_g",
            hover_data=["island", "sex"],
            title="Bill Length vs Bill Depth",
            labels={
                "bill_length_mm": "Bill Length (mm)",
                "bill_depth_mm": "Bill Depth (mm)",
                "body_mass_g": "Body Mass (g)"
            }
        )
        return fig

# --------------------------------------------------------
# Reactive Calculation
# --------------------------------------------------------

@reactive.calc
def filtered_data():
    return penguins_df
