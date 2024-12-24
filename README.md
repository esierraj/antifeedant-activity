# Analysis of the Antifeedant Effect of a Plant-Based Ethanolic Extract on *Spodoptera frugiperda*  

This repository contains Python scripts designed to analyze and visualize data obtained from a choice experiment with *Spodoptera frugiperda* larvae. The experiment aimed to evaluate the antifeedant effect of a plant-based ethanolic extract compared to a negative control and a commercial insecticide.  

## Experimental Context  

The experiment included three treatment groups:  
1. **Negative control**: Maize leaf discs dipped in water with 1% Tween.  
2. **Ethanolic extract**: Leaf discs treated with a 4% plant-based ethanolic extract.  
3. **Insecticide**: Leaf discs treated with lambda-cyhalothrin.  

Each treated disc was placed in a Petri dish containing agar, and one larva was introduced per dish. The following measurements were taken:  
- **Remaining leaf area** at 0 and 48 hours, calculated using the Otsu thresholding method implemented in Python.  
- **Larval weight** at 0 and 48 hours.  
- **Number of leaves consumed** and **number of dead larvae** at 0, 5 min, 30 min, 1 h, 2 h, and 48 h.  

The experiment involved a total of 90 larvae, equally distributed among the three groups (30 larvae per group).  

The collected data were recorded in Excel files and processed using this code to generate descriptive statistics, graphical analyses, and visualizations to interpret the effects of the treatments.  

## Code Features  

- **Statistical calculations**: Averages, standard deviations, and comparative analyses among groups.  
- **Graph generation**: Bar plots, line graphs, and other visualizations to illustrate larval behavior and remaining leaf area over time.  
- **Automated analysis**: Processing of Excel tables to compute key metrics and generate graphical reports.  

## Libraries Used  

The code relies on the following Python libraries for data processing and visualization:  
- **pandas**: For efficient data manipulation and analysis.  
- **openpyxl**: For reading and writing `.xlsx` files.  
- **seaborn**: For creating elegant and statistically-informed graphics.  
- **matplotlib**: For detailed and highly customizable plots.
- **os**: For creating a new directory to save graphics and other files

## Requirements  

- Python 3.8 or later.  

## How to Use This Repository  

1. Download the experimental data in Excel format.  
2. Format the input file according to the script requirements or use the [Lippia_spod.xlsx](Lippia_spod.xlsx) file for testing. 
3. Run the main scripts to generate the desired analyses and visualizations.  

## Objective  

This project aims to streamline data analysis in experimental research on bioinsecticides and agricultural pest control.  
