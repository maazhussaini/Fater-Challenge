library(dplyr)
library(tidyr)
library(lubridate)
library(ggplot2)

# Importing Data Sets-------------------------------------------------------------------------
#prodotti_caricati <- read.csv("C:/Users/mazam/OneDrive/Desktop/statical data analysis/folder/business_game_napoli_csv/prodotti_caricati.csv", header = T, na.strings = c(" ",""))
#premi_mamme <- read.csv("C:/Users/mazam/OneDrive/Desktop/statical data analysis/folder/business_game_napoli_csv/premi_mamme.csv", header = T, na.strings = c(" ",""))
#missioni_players <- read.csv("C:/Users/mazam/OneDrive/Desktop/statical data analysis/folder/business_game_napoli_csv/missioni_players.csv", header = T, na.strings = c(" ",""))
#conversione_ean_prodotto <- read.csv("C:/Users/mazam/OneDrive/Desktop/statical data analysis/folder/business_game_napoli_csv/conversione_ean_prodotto.csv", header = T, na.strings = c(" ",""))
anagrafica <- read.csv("DataSet/business_game_napoli_csv/anagrafica.csv", header = T, na.strings = c(" ",""))

# Applying Data cleaning of anagraphica------------------------------------------------------
names(anagrafica)<-c("Player_ID","REG_Date_Customer","D.O.B_Child","Child_Age_Today","Child_Age_at_Registration","Province","Province_Initials","Town","Region")

anagrafica$D.O.B_Child <- as.Date(anagrafica$D.O.B_Child, "%Y-%m-%d")

anagrafica$REG_Date_Customer<-strptime(anagrafica$REG_Date_Customer,"%Y-%m-%d")
#anagrafica$D.O.B_Child<-strptime(anagrafica$D.O.B_Child,"%Y-%m-%d")

anagrafica$Child_Age_Today<-as.numeric(anagrafica$Child_Age_Today)
anagrafica$Child_Age_Today<-abs(anagrafica$Child_Age_Today)

anagrafica$Child_Age_at_Registration<-as.numeric(anagrafica$Child_Age_at_Registration)
anagrafica$Child_Age_at_Registration<-abs(anagrafica$Child_Age_at_Registration)


#anagrafica%>%
 # mutate(D.O.B_Child = as.Date(anagrafica$D.O.B_Child))%>%
  #complete(D.O.B_Child = seq.Date(min(D.O.B_Child), max(D.O.B_Child), by="day"))

anagrafica <- anagrafica%>%
  mutate(across(D.O.B_Child, ~replace_na(., max(D.O.B_Child, na.rm = TRUE))))

anagrafica <- anagrafica%>%
  mutate(across(Child_Age_Today, ~replace_na(., mean(Child_Age_Today, na.rm = TRUE))))

anagrafica <- anagrafica%>%
  mutate(across(Child_Age_at_Registration, 
                ~replace_na(., mean(Child_Age_at_Registration, na.rm = TRUE))))


anagrafica$Child_Age_Today <- as.integer(anagrafica$Child_Age_Today)
anagrafica$Child_Age_at_Registration <- as.integer(anagrafica$Child_Age_at_Registration)

#View(anagrafica)

class(anagrafica$Player_ID)
class(anagrafica$REG_Date_Customer)
class(anagrafica$D.O.B_Child)
class(anagrafica$Child_Age_Today)
class(anagrafica$Child_Age_at_Registration)
class(anagrafica$Province)
class(anagrafica$Province_Initials)
class(anagrafica$Town)
class(anagrafica$Region)


sum(is.na(anagrafica$Player_ID))
sum(is.na(anagrafica$REG_Date_Customer))
sum(is.na(anagrafica$D.O.B_Child))
sum(is.na(anagrafica$Child_Age_Today))
sum(is.na(anagrafica$Child_Age_at_Registration))
sum(is.na(anagrafica$Province_Initials))
sum(is.na(anagrafica$Town))
sum(is.na(anagrafica$Region))

summary(anagrafica)

## Outlier Detections
boxplot(anagrafica$D.O.B_Child)
boxplot(anagrafica$Child_Age_at_Registration)
boxplot(head(anagrafica$Child_Age_Today) ~ head(anagrafica$Player_ID))


# Applying Data cleaning / Pre-processing of conversione_ean_prodotto---------------------
names(conversione_ean_prodotto)<-c("EAN","Product_Details","Product_Type","Category_Type","TIER")

conversione_ean_prodotto$TIER<-as.factor(conversione_ean_prodotto$TIER)

View (conversione_ean_prodotto)
class(conversione_ean_prodotto$EAN)
class(conversione_ean_prodotto$Product_Details)
class(conversione_ean_prodotto$Product_Type)
class(conversione_ean_prodotto$Category_Type)
class(conversione_ean_prodotto$TIER)
levels(conversione_ean_prodotto$TIER)



# Applying Data Cleaning / Pre-processing to missioni_players------------------------------
names(missioni_players)<- c("Player_ID", "Mission_Details","Unique_Mission_ID","Type","Sub_Type","Mission_Points","Mission_Date_Time")

missioni_players$Mission_Details<-as.integer(missioni_players$Mission_Details)
missioni_players$Unique_Mission_ID<-as.integer(missioni_players$Unique_Mission_ID)
missioni_players$Mission_Points<-as.integer(missioni_players$Mission_Points)
missioni_players$Mission_Date_Time<-strptime(missioni_players$Mission_Date_Time,"%Y-%m-%d%H:%M:%S")
missioni_players$Sub_Type<-as.factor(missioni_players$Sub_Type)

class(missioni_players$Player_ID)
class(missioni_players$Mission_Details)
class(missioni_players$Unique_Mission_ID)
class(missioni_players$Type)
class(missioni_players$Sub_Type)
levels(missioni_players$Sub_Type)
class(missioni_players$Mission_Points)
class(missioni_players$Mission_Date_Time)
#View (missioni_players)

# Applying Data Cleaning / Pre-processing to premi_mamme------------------------------
names(premi_mamme)<-c("Price_Request_Date","Player_ID","Prize_Name","Required_Points_for_Prize","Prize_Type","Prize_Format","Delivery_Mode")

premi_mamme$Price_Request_Date<-strptime(premi_mamme$Price_Request_Date,"%Y-%m-%d")
premi_mamme$Player_ID<-as.integer(premi_mamme$Player_ID)
premi_mamme$Prize_Type<-as.factor(premi_mamme$Prize_Type)
premi_mamme$Prize_Format<-as.factor(premi_mamme$Prize_Format)
premi_mamme$Delivery_Mode<-as.factor(premi_mamme$Delivery_Mode)

class(premi_mamme$Price_Request_Date)
class(premi_mamme$Player_ID)
class(premi_mamme$Prize_Name) 
class(premi_mamme$Required_Points_for_Prize)
class(premi_mamme$Prize_Type)
levels(premi_mamme$Prize_Type)
class(premi_mamme$Prize_Format)
levels(premi_mamme$Prize_Format)
class(premi_mamme$Delivery_Mode)
levels(premi_mamme$Delivery_Mode)
View (premi_mamme)



# Applying Data Cleaning /Preprocessing to prodotti_caricati-------------------------------------
names(prodotti_caricati)<-c("Player_ID","Mission_Details","Product_Points","Product_Upload_Date","EAN")

prodotti_caricati$Product_Upload_Date<-strptime(prodotti_caricati$Product_Upload_Date,"%Y-%m-%d %H:%M:%S")

class(prodotti_caricati$Player_ID)
class(prodotti_caricati$Mission_Details)
class(prodotti_caricati$Product_Points)
class(prodotti_caricati$Product_Upload_Date)
class(prodotti_caricati$EAN)
View (prodotti_caricati)