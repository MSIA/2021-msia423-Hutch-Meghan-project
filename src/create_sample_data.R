library(tidyverse)
tweets <- read.csv("data/external/constructs.csv")

tweets <- head(tweets, 100) %>% 
  select(-X2)

write.csv(tweets, "data/sample/tweets.csv", 
          row.names = FALSE)
