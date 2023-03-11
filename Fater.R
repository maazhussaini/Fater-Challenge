#install.packages("dplyr")

library(dplyr)
library(tidyverse)

redeemingPoints_player <- function(registry, award_info){
  ###
  #  Check which players are redeeming their points
  ###
  redeemingPoints <- merge(registry, award_info, by="id_player")
  
  redeemingPoints_grouped <- redeemingPoints %>%
    group_by(redeemingPoints$id_player) %>%
    dplyr::summarise(puntipremio = sum(redeemingPoints$puntipremio)) %>%
    as.data.frame()
  
  str(redeemingPoints_grouped)
  summary(redeemingPoints_grouped)
  view(redeemingPoints_grouped)
}

redeemingPoints_player(registry=registry, award_info=awards_info)
