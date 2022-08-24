### REPLICA FIGURA 3 "Is murder bad for business? Evidence from Colombia"

#install.packages('haven')
#install.packages('ggpubr')
#install.packages('data.table')

# Working directory
setwd("C:\\Users\\Matias\\Documents\\UDESA\\Herramientas computacionales\\HCI-Tareas\\Trabajo Final\\dataverse_files")

# Abrolibrerias
library('haven')
library('dplyr')
library('ggthemes')
library('ggplot2')
library('ggpubr')
library("tidyverse")
library("data.table")
library("wesanderson")

################# Figura 3 #################

df <- read_dta('figures1_3_4_data.dta')

# Defino variable que toma valor 1 si el municipio tuvo un share de votos por Uribe mayor o igual a 0.5
df$yes_02 <- as.integer(df$s_uribe_02>=0.5)
df$yes_02[ is.na(df$yes_02) ] <- 1 # código en STATA pone 1 en los NA's de s_uribe_02, R no. Lo hago manualmente

# Definovariable que toma valor 1 si el municipio tuvo un share de votos por Uribe menor a 0.5
df$no_02 <- as.integer(df$s_uribe_02<0.5)
df$no_02[ is.na(df$no_02) ] <- 1

# Variable que toma valor 1 si share de votos por uribe en 2006 es mayor o igual a 0.5 y si también lo fue en 2002
df$yes_02_y <-as.integer(df$s_uribe_06>=0.5 & df$yes_02 == 1)
df$yes_02_y[ is.na(df$yes_02_y) ] <- 1

# Calculo, agrupado por año, la media de homicidios en lugares que votaron mayoritariamente por Uribe en 2002 y en 2006
df <- df %>% group_by(year) %>% mutate( m_yes_02_y = mean( hom_r[yes_02_y== 1], na.rm = T) ) 
df$m_yes_02_y[df$yes_02_y == 0] <- NA # me aseguro que no hay valores cuando yes_02_y == 0

# Variable que toma valor 1 si share de votos por uribe en 2006 es menor a 0.5 y si fue mayor o igual en 2002
df$yes_02_n <-as.integer( df$s_uribe_06<0.5 & df$yes_02 == 1 )
df$yes_02_y[ is.na(df$yes_02_y) ] <- 1

# Calculo, agrupado por año, la media de homicidios en lugares que votaron mayoritariamente por Uribe en 2002 y no en 2006
df <- df %>% group_by(year) %>% mutate( m_yes_02_n = mean( hom_r[yes_02_n== 1], na.rm = T) ) 
df$m_yes_02_n[ df$yes_02_n == 0 ] <- NA

# Variable que toma valor 1 si share de votos por uribe en 2006 es mayor o igual a 0.5 y si fue menor en 2002
df$no_02_y <- as.integer( df$s_uribe_06>=0.5 & df$no_02 == 1 )
df$no_02_y[ is.na(df$no_02_y) ] <- 0 

# Calculo, agrupado por año, la media de homicidios en lugares que no votaron mayoritariamente por Uribe en 2002 y si en 2006
df <- df %>% group_by(year) %>% mutate( m_no_02_y = mean( hom_r[no_02_y== 1], na.rm = T) )
df$m_no_02_y[ df$no_02_y == 0 ] <- NA

# Variable que toma valor 1 si share de votos por uribe en 2006 es menor a 0.5 y si tambien lo fue en 2002
df$no_02_n <- as.integer( df$s_uribe_06<0.5 & df$no_02 == 1 )
df$no_02_n[ is.na(df$no_02_n) ] <- 0 

# Calculo, agrupado por año, la media de homicidios en lugares que no votaron mayoritariamente por Uribe en 2002 y tampoco en 2006
df <- df %>% group_by(year) %>% mutate( m_no_02_n = mean( hom_r[no_02_n== 1], na.rm = T) )
df$m_no_02_n[ df$no_02_n == 0 ] <- NA

# Seteo los themes (uno por lugar del gráfico)
lefttheme <-theme(plot.background=element_rect(fill="white"),
                panel.background = element_rect(fill="aliceblue"),
                panel.grid.major = element_line(color="azure2",linetype=1),
                panel.border = element_rect(colour = "antiquewhite4", fill=NA, size=1),
                plot.caption = element_text(hjust = 0),
                plot.title = element_text(size = 10),
                legend.position = "top",
                legend.title = element_text(size = 12),
                legend.text = element_text(size = 10),
                legend.background = element_blank(),
                legend.key = element_blank(),
                legend.key.width = unit(2.4, 'cm'))

righttheme <-theme(plot.background=element_rect(fill="white"),
                 panel.background = element_rect(fill="aliceblue"),
                 panel.grid.major = element_line(color="azure2",linetype=1),
                 panel.border = element_rect(colour = "antiquewhite4", fill=NA, size=1),
                 plot.caption = element_text(hjust = 0),
                 plot.title = element_text(size = 10),
                 legend.position = "top",
                 legend.title = element_text(size = 12),
                 legend.text = element_text(size = 10),
                 legend.background = element_blank(),
                 legend.key = element_blank(),
                 axis.ticks.y = element_blank(),
                 axis.text.y = element_blank())



## Panel A

# Cambio el formato de los datos, lo guardo en una nueva base. Creo una variable llamada winloss que toma como valores las variables (10, 12, 14, 16) de la base original, es decir, las variables de las medias. Los valores de estas pasan a otra variable llamada mean_hom_rate
df2 <- df %>% gather("winloss", "mean_hom_rate", c(10, 12, 14,16) )

# Me quedo con los años antes de 2002. Agrupo por winloss y año, creo una nueva variable que calcula la media. Es decir, calculo la media por año y winloss para los años antes de 2002
df2 <- df2 %>% filter(year <=2001) %>% group_by(winloss,year) %>% summarise( "mean_hom_rate" = mean(mean_hom_rate, na.rm=T) )


panela <- ggplot( df2, aes(x = year, y = mean_hom_rate, linetype = winloss, color = winloss) ) +
  # Geomas
  geom_line(lwd = 2)  +
  # Para leyenda, seteo los colores y los tipos de linea deseados, junto a los labers de cada elemento y pongo que no tenga titulo
  scale_color_manual( name = "", values = c( "orange", "darkgreen", "bisque3", "darkslateblue"), labels = c("Always lost", "Lost 1- Won 2", "Won 1- Lost 2", "Always Won") )+
  scale_linetype_manual( name = "", values = c("dashed", "dotdash", "11", "solid"), labels = c("Always lost", "Lost 1- Won 2", "Won 1- Lost 2", "Always Won") ) +
  # Theme
  lefttheme + 
  # Titulos de eje y de grafico
  xlab("")+
  ylab("")+
  ggtitle("(A) Before Uribe") +
  # Limites de los ejes
  ylim(20,100) +
  xlim(1994, 2002) +
  # Cambio orden de leyenda
  guides(linetype = guide_legend(reverse=T), color = guide_legend(reverse = TRUE))

panela



## Panel B

df2 <- df %>% gather("winloss", "mean_hom_rate", c(10, 12, 14,16))

df2 <- df2 %>% filter(year >2001) %>% group_by(winloss,year) %>% summarise( "mean_hom_rate" = mean(mean_hom_rate, na.rm=T) )


panelb <- ggplot(df2, aes(x = year, y = mean_hom_rate, color = winloss, linetype = winloss) ) +
  geom_line(lwd = 2)  +
  scale_color_manual(name = "", values = c( "orange", "darkgreen", "bisque3", "darkslateblue"), labels = c("Always lost", "Lost 1- Won 2", "Won 1- Lost 2", "Always Won") )+
  scale_linetype_manual( values = c("dashed", "dotdash", "11", "solid"), labels = NULL ) +
  righttheme +
  xlab("")+
  ylab("")+
  ylim(20,100) +
  ggtitle("(B) After") +
  # Que no ponga leyenda
  guides(linetype = "none", colour = "none")

panelb



# Hago lo mismo para la muestra restringida, es decir, cuando manu_sample == 1
df <- df %>% group_by(year) %>% mutate( m_yes_02_y = mean(hom_r[yes_02_y== 1 & manu_sample == 1], na.rm = T) )
df$m_yes_02_y[df$yes_02_y == 0 | is.na(df$manu_sample)] <- NA

df <- df %>% group_by(year) %>% mutate( m_yes_02_n = mean(hom_r[yes_02_n== 1 & manu_sample == 1], na.rm = T) )
df$m_yes_02_n[df$yes_02_n == 0 | is.na(df$manu_sample)] <- NA

df <- df %>% group_by(year) %>% mutate( m_no_02_y = mean(hom_r[no_02_y== 1 & manu_sample == 1], na.rm = T) )
df$m_no_02_y[df$no_02_y == 0 | is.na(df$manu_sample)] <- NA

df <- df %>% group_by(year) %>% mutate( m_no_02_n = mean(hom_r[no_02_n== 1 & manu_sample == 1], na.rm = T) )
df$m_no_02_n[df$no_02_n == 0 | is.na(df$manu_sample)] <- NA



## Panel C

df2 <- df %>% gather("winloss", "mean_hom_rate", c(10, 12, 14,16))

df2 <- df2 %>% filter(year <=2001) %>% group_by(winloss,year) %>% summarise( "mean_hom_rate" = mean(mean_hom_rate, na.rm=T) )


panelc <- ggplot(df2, aes(x = year, y = mean_hom_rate, color = winloss, linetype = winloss) ) +
  geom_line(lwd = 2)  +
  scale_color_manual( name = "", values = c( "orange", "darkgreen", "bisque3", "darkslateblue"), labels = c("Always lost", "Lost 1- Won 2", "Won 1- Lost 2", "Always Won") )+
  scale_linetype_manual( values = c("dashed", "dotdash", "11", "solid"), labels = NULL ) +
  lefttheme + 
  xlab("Year")+
  ylab("")+
  ylim(20,100) +
  xlim(1994, 2002)+
  ggtitle("(C)") +
  guides(linetype = "none", colour = "none")

panelc



## Panel D
df2 <- df %>% gather("winloss", "mean_hom_rate", c(10, 12, 14,16))
df2 <- df2 %>% filter(year >2001) %>% group_by(winloss,year) %>% summarise( "mean_hom_rate" = mean(mean_hom_rate,na.rm=T) )
paneld <- ggplot( df2, aes(x = year, y = mean_hom_rate, color = winloss, linetype = winloss) ) +
  geom_line(lwd = 2)  +
  scale_color_manual( name = "", values = c( "orange", "darkgreen", "bisque3", "darkslateblue"), labels = c("Always lost", "Lost 1- Won 2", "Won 1- Lost 2", "Always Won") )+
  scale_linetype_manual( values = c("dashed", "dotdash", "11", "solid"), labels = NULL ) +
  righttheme + 
  xlab("Year")+
  ylab("")+
  ylim(20,100) +
  ggtitle("(D)") + 
  guides(linetype = "none", colour = "none")

paneld


# FIGURE 3

# Junto panela y panelb, establezco que ponga solo 1 leyenda, le agrego texto arriba
top <- ggarrange( panela, panelb, ncol = 2, common.legend = TRUE ) %>% annotate_figure( top = text_grob("All municipalities", face = "bold", size = 12 ) )

# Mismo con panelc y paneld
bot <- ggarrange( panelc, paneld, ncol = 2 ) %>% 
  annotate_figure( plot, top = text_grob( "Municipalities with firm data available", face = "bold", size = 12 ) )

# Junto ambos, agregando titulo de grafico
# CORRIENDO TODO JUNTO ESTA IMAGEN PUEDEN NO APARECER, CORRER LINEA POR SEPARADO EN CASO DE QUE PASE
ggarrange( NULL, top, bot, nrow = 3, heights = c(0.08, 1, 1) ) %>%  annotate_figure( fig.lab.pos = "top.left", fig.lab = "Mean homicide rates by vote share in first and second presidential election", fig.lab.face = "bold", fig.lab.size = 15 )


################# Figura 4 #################

df <- read_dta('figures1_3_4_data.dta')

# Copio s_uribe_02 en nueva variable
df$d1 <- df$s_uribe_02

# Le pongo cero si año < 2002
df$d1[ df$year<2002 ] <- 0

# Calculo la diferencia de homicidios entre 2010 y 2002, lo guardo en nueva variable
df <- df %>% group_by(muncod) %>% mutate( d10_02 = ( hom_r[year == 2010] - shift(hom_r, 8)))
df$d10_02[df$year != 2010] <- NA

# Creo una variable en base al share de votos que recibio Uribe en 2002
df <- df %>% mutate(indicator = case_when( (d1 <= 0.1) ~ 1, (d1 > 0.1 & d1 <= 0.2) ~ 2, (d1 > 0.2 & d1 <= 0.3) ~ 3, (d1 > 0.3 & d1 <= 0.4) ~ 4, (d1 > 0.4 & d1 <= 0.5) ~ 5, (d1 > 0.5 & d1 <= 0.6) ~ 6, (d1 > 0.6 & d1 <= 0.7) ~ 7, (d1 > 0.7 & d1 <= 0.8) ~ 8, (d1 > 0.8 & d1 <= 0.9) ~ 9, (d1 > 0.9 & d1 <= 1) ~ 10) )

# La divido por 10, guardandola en otra variable
df$ind <- df$indicator / 10
df$ind[ df$year != 2010 ] <- NA

# Elimino la original
df <- df %>% subset( select = -indicator )

# Calculo la media de la diferencia de homicidios en grupos segun ind
df <- df %>% group_by(ind) %>% mutate( m_d10_02 = mean(d10_02[year == 2010], na.rm = T) )
df$m_d10_02[ df$year != 2010 ] <- NA


## Panel B

panelb <- df %>% ggplot( aes(ind, m_d10_02) ) + 
  geom_smooth( method = "lm", aes( fill = "95% CI", color = "Linear fit"), formula = y ~ x) +
  geom_point(size = 2, aes( shape = "Mean values") ) +
  # Establezco los breaks, los labels y los limites
  # CUIDADO: limits tambien afecta los datos elegidos, no solo los esconde del grafico
  scale_x_continuous( breaks = seq(0, 1, 0.2), labels = c("0", ".2", ".4", ".6", ".8", "1"), limits = c(0, 1) )  + scale_y_continuous( breaks = seq(-80, 20, 20), limits =   c(-82, 22.5) ) +
  righttheme +
  ylab("") +
  xlab("") +
  scale_shape_manual( name = "", values = c("Mean values" = 19) ) +
  scale_fill_manual( NULL, values = wes_palette(n=4, name="BottleRocket1") ) +
  scale_color_manual( NULL, values = 'black' ) +
  guides(
    color = "none",
    fill = "none",
    shape = "none" ) + 
  ggtitle("(B) After (2010-2022)")

panelb

## Panel A

# Sort de la base de acuerdo a muncod e year
df <- df[ order( df$muncod, df$year ), ]

# Muevo 9 posiciones adelante la variable ind, lo guardo en una nueva variable
df <- df %>% group_by(muncod) %>% mutate( ind1 = shift( ind, 9 , type = "lead") )

# Calculo la diferencia de homicide rate entre 2001 y 1995 agrupado por muncod
df <- df %>% group_by(muncod) %>% mutate( d01_95 = (hom_r[year == 2001] - shift(hom_r, 6) ) )
df$d01_95[df$year != 2001] <- NA

# Calculo la media de la diferencia segun ind1
df <- df %>% group_by(ind1) %>% mutate( m_d01_95 = mean(d01_95, na.rm = T) )
df$m_d01_95[df$year != 2001] <- NA

panela <- df %>% ggplot( aes(ind1, m_d01_95) ) + 
  geom_smooth( method = "lm", aes( fill = "95% CI", color = "Linear fit"), formula = y ~ x) + geom_point(size = 2, aes( shape = "Mean values") ) +
  scale_x_continuous( breaks = seq(0, 1, 0.2), labels = c("0", ".2", ".4", ".6", ".8", "1"), limits = c(0, 1) )  + scale_y_continuous( breaks = seq(-80, 20, 20), limits =   c(-82, 22.5) ) +
  lefttheme + ylab("") + xlab("") +
  scale_shape_manual( name = "", values = c("Mean values" = 19) ) +
  scale_fill_manual( NULL, values = wes_palette(n=4, name="BottleRocket1") ) +
  scale_color_manual( NULL, values = 'black' ) +
  # Que no aparezca el relleno en el linear fit, ni la linea en el relleno, también le pongo orden
  guides(
    color=guide_legend( override.aes = list(fill=NA), order=2 ),
    fill=guide_legend( override.aes = list(color=NA), order=1 )
  ) +
  ggtitle("(A) Change before Uribe (2001-1995)")

panela

# Lo mismo para muestra restringida, es decir, cuando manu_sample ==1

## Panel D

df <- df %>% group_by(ind) %>% mutate( m_d10_02 = mean(d10_02[year == 2010 & manu_sample == 1], na.rm = T))
df$m_d10_02[df$year != 2010 | is.na(df$manu_sample)] <- NA  

paneld <- df %>% ggplot( aes(ind, m_d10_02) ) + 
  geom_smooth( method = "lm", aes( fill = "95% CI", color = "Linear fit"), formula = y ~ x) + geom_point(size = 2, aes( shape = "Mean values") ) +
  scale_x_continuous( breaks = seq(0, 1, 0.2), labels = c("0", ".2", ".4", ".6", ".8", "1"), limits = c(0, 1) )  + scale_y_continuous( breaks = seq(-80, 20, 20), limits =   c(-82, 22.5) ) +
  righttheme + xlab("% Votes for Uribe 1st Election") + ylab("") +
  scale_shape_manual( name = "", values = c("Mean values" = 19) ) +
  scale_fill_manual( NULL, values = wes_palette(n=4, name="BottleRocket1") ) +
  scale_color_manual( NULL, values = 'black' ) +
  guides(
    color = "none",
    fill = "none",
    shape = "none" ) +
  ggtitle("(D)")

paneld

## Panel C

df <- df %>% group_by(ind1) %>% mutate( m_d01_95 = mean( d01_95[ year == 2001 & manu_sample == 1 ], na.rm = T ) )
df$m_d01_95[df$year != 2001 | is.na(df$manu_sample)] <- NA   

panelc <- df %>% ggplot( aes(ind1, m_d01_95) ) + 
  geom_smooth( method = "lm", aes( fill = "95% CI", color = "Linear fit"), formula = y ~ x) + geom_point(size = 2, aes( shape = "Mean values") ) +
  scale_x_continuous( breaks = seq(0, 1, 0.2), labels = c("0", ".2", ".4", ".6", ".8", "1"), limits = c(0, 1) )  + scale_y_continuous( breaks = seq(-80, 20, 20), limits =   c(-82, 22.5) ) +
  lefttheme + ylab("") + xlab("% Votes for Uribe 1st Election") +
  scale_shape_manual( name = "", values = c("Mean values" = 19) ) +
  scale_fill_manual( NULL, values = wes_palette(n=4, name="BottleRocket1") ) +
  scale_color_manual( NULL, values = 'black' ) +
  guides(
    color = "none",
    fill = "none",
    shape = "none" ) +
  ggtitle("(C)")

panelc

# FIGURE 4

top <- ggarrange(panela, panelb, ncol = 2, common.legend = TRUE) %>% annotate_figure( top = text_grob("All municipalities", face = "bold", size = 12) )

bot <- ggarrange( panelc, paneld, ncol = 2 ) %>% 
  annotate_figure( plot, top = text_grob( "Municipalities with firm data available", face = "bold", size = 12 ) )

# CORRIENDO TODO JUNTO ESTA IMAGEN PUEDEN NO APARECER, CORRER LINEA POR SEPARADO EN CASO DE QUE PASE
ggarrange( NULL, top, bot, nrow = 3, heights = c(0.08, 1, 1) ) %>%  annotate_figure( fig.lab.pos = "top.left", fig.lab = "Mean change in homicide rates for Uribe's Supporters", fig.lab.face = "bold", fig.lab.size = 15 )
