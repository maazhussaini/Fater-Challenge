# Load libraries
library(dplyr)
library(tidyr)
library(caret)
library(ggplot2)

# Load datasets
registry <- read.csv("DataSet/business_game_napoli_csv/anagrafica.csv")
product_loaded <- read.csv("DataSet/business_game_napoli_csv/prodotti_caricati.csv")
product_conversion <- read.csv("DataSet/business_game_napoli_csv/conversione_ean_prodotto.csv")
missions <- read.csv("DataSet/business_game_napoli_csv/missioni_players.csv")
app_accesses <- read.csv("DataSet/business_game_napoli_csv/accessi_app.csv")
awards <- read.csv("DataSet/business_game_napoli_csv/premi_mamme.csv")


# Data cleaning and feature engineering
# 1. Convert dates appropriate format
registry[!is.na(registry)]
sum(is.na(product_loaded))
sum(is.na(product_conversion))
sum(is.na(missions))
sum(is.na(app_accesses))
sum(is.na(awards))

str(registry)
