random.data <- as.numeric(c(0:20))
random.data
class(random.data)

my.data <-data.frame(c(0:20))
class(my.data)

hist(random.data)

# Use '#' for comments
barplot(height = random.data, 
        col = c("navyblue", "skyblue"), 
        main = "Test barplot", 
        xlab = "x-axis", 
        ylab = "y-axis")
legend(x = "topleft", legend = c("bars", "light bars"), fill = c("navyblue", "skyblue"), ncol = 2)

getwd() # Show me my current working directory
setwd(dir = "~/simulation_projects/") # Tell R what my current working directory should be
getwd()

# Read in file
# Store in 'ms.data'
ms.data <- read.csv(file = "msstats_reps_100_out.txt", 
                    sep = "\t", # Separate columns by tab 
                    header = FALSE) # Don't include header
ms.data

head(ms.data) # View head of ms.data
colnames(ms.data) <- c("Pi", "Pi.values", "SS", "SS.values", "TajD", "TajD.values", "thetaH", "thetaH.values", "H", "Het?") # Set column names
head(ms.data)

barplot(height = ms.data$Pi.values) # Give it dataset and tell it which column you want as your height

barplot(height = ms.data$TajD.values, ylim = c(-5, 3), col = "cyan", main = "Title", ylab = "TajD") # ylim is to control range of values of y-axis
