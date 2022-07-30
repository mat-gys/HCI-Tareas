# TAREA 1
'
Prior to use, install the following packages:
install.packages("ggplot2")
install.packages("tibble")
install.packages("dplyr")
install.packages("gridExtra")
install.packages("Lock5Data")
install.packages("ggthemes")

install.packages("maps")
install.packages("mapproj")
install.packages("corrplot")
install.packages("fun")
install.packages("zoo")

Used datafiles and sources:
a) gapminder.csv - Modified dataset from various datasets available at:
https://www.gapminder.org/data/
b) xAPI-Edu-Data.csv:
https://www.kaggle.com/aljarah/xAPI-Edu-Data/data
c) LoanStats.csv:
Loan Data from Lending Tree - https://www.lendingclub.com/info/download-data.action
d) Lock5Data

'

#Load Libraries
library("ggplot2")
library("tibble")
library("gridExtra")
library("dplyr")
library("Lock5Data")
library("ggthemes")
library("fun")
library("zoo")
library("corrplot")
library("maps")
library("mapproj")
library("plotmath")

#Set pathname for the directory where you have data
setwd("C:\\Users\\Matias\\Documents\\UDESA\\Herramientas computacionales\\Clase 5\\video 1\\Applied-Data-Visualization-with-R-and-ggplot2-master")
#Check working directory
getwd()

#Note: Working directory should be "Beginning-Data-Visualization-with-ggplot2-and-R"

#Load the data files
df <- read.csv("data/gapminder-data.csv")
df3 <- read.csv("data/LoanStats.csv")


################################### Original 1 ###################################

#Activity B:Using faceting to understand data
#"Aquí quiere ver la distribución de las cantidades de los préstamos para diferentes grados de crédito.
# Objetivo: Trazar el monto del préstamo para diferentes grados de crédito usando el faceting.
df3s <- subset(df3,grade %in% c("A","B","C","D","E","F","G"))
pb1<-ggplot(df3s,aes(x=loan_amnt))
pb2<-pb1+geom_histogram(bins=10,fill="cadetblue4")
#Facet_wrap
pb3<-pb2+facet_wrap(~grade) 
pb3

################################### Correccion 1 ###################################
mytheme <-theme(plot.background=element_rect(fill="white"),
                panel.background = element_rect(fill="azure"),
                panel.grid.major = element_line(color="azure2",linetype=1),
                panel.border = element_rect(colour = "antiquewhite4", fill=NA, size=1),
                plot.caption = element_text(hjust = 0))
pb5 <- pb1 + 
  geom_density() + 
  facet_wrap(~grade) +
  ylab("Density") + 
  xlab("Loan Amount") + 
  labs(caption = "Density is in thousands", title="Loan amount density plots by grade") + 
  mytheme + 
  scale_y_continuous(breaks=c(0, 0.00005, 0.0001), labels = c("0", "0.05", "0.1"))
pb5


################################### Original 2 ###################################
dfn <- df3[,c("home_ownership","loan_amnt","grade")]
dfn <- na.omit(dfn) #remove NA y NONE
dfn <- subset(dfn, !dfn$home_ownership %in% c("NONE"))

ggplot(dfn,aes(x=home_ownership,y=loan_amnt))+geom_boxplot(aes(fill=grade))+
  scale_y_continuous(breaks=seq(0,40000,2000))

################################### Correccion 2 ###################################

ggplot(dfn,aes(x=home_ownership,y=loan_amnt)) +
  geom_boxplot(aes(fill=grade)) +
  scale_y_continuous(breaks=seq(0,40000,2000)) +
  annotate("text", x=0.679, y=9400, label= "bold(A)", parse = TRUE, size =4.5) +
  annotate("text", x=0.785, y=13000, label= "bold(B)", parse = TRUE, size =4.5)  +
  annotate("text", x=0.895, y=13100, label= "bold(C)", parse = TRUE, size =4.5) +
  annotate("text", x=1.01, y=13800, label= "bold(D)", parse = TRUE, size =4.5) +
  annotate("text", x=1.113, y=17600, label= "bold(E)", parse = TRUE, size =4.5) +
  annotate("text", x=1.22, y=21300, label= "bold(F)", parse = TRUE, size =4.5) +
  annotate("text", x=1.325, y=21100, label= "bold(G)", parse = TRUE, size =4.5) +
  labs(subtitle="Loan amount by type of home ownership and grade",
       title="Box plot")+ylab("Loan amount") + xlab("Type of home ownership") +
  theme(legend.position="none") + scale_fill_brewer(palette="Oranges", direction = -1)


################################### Original 3 ###################################
pd1 <- ggplot(df,aes(x=BMI_male,y=BMI_female)) +
  geom_point(aes(color=Country),size=2) +
  scale_colour_brewer(palette="Dark2") +
  theme(axis.title=element_text(size=15,
                                color="cadetblue4",
                                face="bold"),
                                plot.title=element_text(color="cadetblue4",size=18,face="bold.italic"),
                                panel.background = element_rect(fill="azure",color="black"),
                                panel.grid=element_blank(),
                                legend.position="bottom",
                                legend.justification="left",
                                legend.title = element_blank(),
                                legend.key = element_rect(color=3,fill="gray97"))+
  xlab("BMI Male")+
  ylab("BMI female")+
  ggtitle("BMI female vs BMI Male")
pd1

################################### Correcion 3 ###################################
mytheme <-theme(plot.background=element_rect(fill="white"),
                panel.background = element_rect(fill="azure"),
                panel.grid.major = element_line(color="azure2",linetype=1),
                panel.border = element_rect(colour = "antiquewhite4", fill=NA, size=1),
                plot.caption = element_text(hjust = 0),
                legend.position = c(0.15, 0.75),
                legend.title = element_text(size = 12),
                legend.text = element_text(size = 11),
                legend.background = element_blank(),
                legend.key = element_blank())
pd1 <- ggplot(df,aes(x=BMI_male,y=BMI_female)) +
  geom_point(aes(shape=Country),size=2)+
  scale_colour_brewer(palette="Dark2") +
  mytheme +
  guides(shape = guide_legend(override.aes = list(size = 3))) +
  xlab("Male")+
  ylab("Female")+
  ggtitle("BMI") +
  scale_shape_manual(values=c(5, 4, 3, 15, 2, 16, 0))
pd1

# TAREA 2: 

x <- c("ggmap", "rgdal", "rgeos", "maptools", "dplyr", "tidyr", "tmap")

install.packages(x) 
lapply(x, library, character.only = TRUE) # load the required packages

setwd("~/Videos/03 - Cursos/05 - Herramientas computacionales/Clase 5 - Data Visualization/Tarea")

library(rgdal)
lnd <- readOGR(dsn = "data/london_sport.shp")

