# Load necessary libraries
library(dplyr)
library(ggplot2)
library(stats)
library(effsize)

# Load your dataset
# Create a list of CSV file names
file_names <- list.files("runtables", pattern = "^run_table.*\\.csv$", full.names = TRUE)

# Initialize an empty data frame to store the combined data
data <- data.frame()

# Loop through the file names and append data to the combined_data data frame
for (file in file_names) {
  data1 <- read.csv(file)
  data <- rbind(data, data1)
}

data$energy <- data$avg_power * data$time

install.packages("tidyr")
library(tidyr)

# Understanding the Data
results_dict <- list(
  "Central Tendency - Mean" = list(
    "avg_cpu" = mean(as.numeric(data$avg_cpu)),
    "avg_memory" = mean(as.numeric(data$avg_mem)),
    "avg_energy" = mean(as.numeric(data$energy)),
    "avg_power" = mean(as.numeric(data$avg_power))
  ),
  "Central Tendency - Median" = list(
    "avg_cpu" = median(as.numeric(data$avg_cpu)),
    "avg_memory" = median(as.numeric(data$avg_mem)),
    "avg_energy" = median(as.numeric(data$energy)),
    "avg_power" = median(as.numeric(data$avg_power))
  ),
  "Dispersion - Standard Deviation" = list(
    "avg_cpu" = sd(as.numeric(data$avg_cpu)),
    "avg_memory" = sd(as.numeric(data$avg_mem)),
    "avg_energy" = sd(as.numeric(data$energy)),
    "avg_power" = sd(as.numeric(data$avg_power))
  ),
  "Dispersion - Variance" = list(
    "avg_cpu" = var(as.numeric(data$avg_cpu)),
    "avg_memory" = var(as.numeric(data$avg_mem)),
    "avg_energy" = var(as.numeric(data$energy)),
    "avg_power" = var(as.numeric(data$avg_power)) 
  )
)

results_central <- as.data.frame(results_dict)

# Clean the data frame to remove non-numeric characters
results_central_cleaned <- lapply(results_central, function(x) as.numeric(gsub(",", "", x, fixed = TRUE)))

# Transpose the data frame for the desired format
results_central_cleaned <- t(results_central_cleaned)

# Rename the columns with the correct number of names
colnames(results_central_cleaned) <- c("avg_cpu", "avg_memory", "avg_energy", "avg_power")

# Customize the row names
rownames(results_central_cleaned) <- c("Mean", "Median", "Standard Deviation", "Variance")

print(results_central_cleaned)

# Format the table using kable
formatted_table_central <- results_central_cleaned %>%
  kable("html", escape = FALSE, format = "html") %>%
  kable_styling("striped", full_width = FALSE) %>%
  column_spec(1, bold = TRUE)


# Box plots for Linux Governor and Workload
box_plot_governor <- ggplot(data, aes(x = Linux_Governor, y = energy)) +
  geom_boxplot()
box_plot_workload <- ggplot(data, aes(x = Workload, y = energy)) +
  geom_boxplot()

# Save box plots to files
ggsave("box_plot_governor.png", plot = box_plot_governor)
ggsave("box_plot_workload.png", plot = box_plot_workload)

#qqplot for energy

qqplot_for_energy_data <- rnorm(data$energy)  

png("qqplot.png", width = 800, height = 600)
qqnorm(qqplot_for_energy_data, main = "Q-Q Plot Energy", xlab = "", ylab = "")
dev.off()

#qqplot for power
qqplot_for_power_data <- rnorm(data$avg_power)  

png("qqplotpower.png", width = 800, height = 600)
qqnorm(qqplot_for_power_data, main = "Q-Q Plot Power", xlab = "", ylab = "")
dev.off()

#qqplot for CPU
qqplot_for_CPU_data <- rnorm(data$avg_cpu)  

png("qqplotCPU.png", width = 800, height = 600)
qqnorm(qqplot_for_CPU_data, main = "Q-Q Plot CPU", xlab = "", ylab = "")
dev.off()

#qqplot for memory
qqplot_for_memory_data <- rnorm(data$avg_mem)  

png("qqplotmemory.png", width = 800, height = 600)
qqnorm(qqplot_for_memory_data, main = "Q-Q Plot Memory", xlab = "", ylab = "")
dev.off()

install.packages("knitr")
install.packages("kableExtra")
install.packages("webshot")
library(knitr)
library(kableExtra)
library(webshot)

#shapior for all dependent variables 
data_list <- list(data$energy, data$avg_power, data$avg_cpu, data$avg_mem)

# labels foe each dependent variables
labels <- c("Energy", "Power", "CPU", "Memory")

# Perform Shapiro-Wilk tests for each dataset
shapiro_tests <- lapply(data_list, shapiro.test)

# Create a data frame to store the results
results_df <- data.frame(
  Dataset = labels, 
  Statistic = sapply(shapiro_tests, function(x) x$statistic),
  P_Value = sapply(shapiro_tests, function(x) x$p.value),
  Normality = sapply(shapiro_tests, function(x) ifelse(x$p.value < 0.05, "Not Normal", "Normal"))
)

formatted_table <- results_df %>%
  kable("html", escape = FALSE) %>%
  kable_styling("striped", full_width = FALSE) %>%
  column_spec(1, bold = TRUE)

# Print the formatted table (for display in RStudio)
print(formatted_table)

# Histograms
histogram_cpu <- ggplot(data, aes(x = avg_cpu)) +
  geom_histogram(binwidth = 1, fill = "blue", color = "black") +
  labs(title = "Histogram of avg_cpu", x = "avg_cpu", y = "Frequency")

histogram_memory <- ggplot(data, aes(x = avg_mem)) +
  geom_histogram(binwidth = 1, fill = "green", color = "black") +
  labs(title = "Histogram of avg_memory", x = "avg_memory", y = "Frequency")

histogram_energy <- ggplot(data, aes(x = energy)) +
  geom_histogram(binwidth = 1000, fill = "red", color = "black") +
  labs(title = "Histogram of energy", x = "energy", y = "Frequency")

histogram_power <- ggplot(data, aes(x = avg_power)) +
  geom_histogram(binwidth = 1, fill = "yellow", color = "black") +
  labs(title = "Histogram of power", x = "power", y = "Frequency")

# Save histograms to files
ggsave("histogram_cpu.png", plot = histogram_cpu)
ggsave("histogram_memory.png", plot = histogram_memory)
ggsave("histogram_energy.png", plot = histogram_energy)
ggsave("histogram_power.png", plot = histogram_power)

# Scatter plots with regression lines
g_scatter_avg_cpu <- ggplot(data, aes(x = avg_cpu, y = avg_power)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE, color = "red") +  # Add regression line
  labs(title = "Scatter Plot of avg_cpu vs. Energy", x = "avg_cpu", y = "Power")

g_scatter_avg_mem <- ggplot(data, aes(x = avg_mem, y = avg_power)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE, color = "blue") +  # Add regression line
  labs(title = "Scatter Plot of avg_mem vs. Energy", x = "avg_mem", y = "Power")

# Save the scatter plots with regression lines to files
ggsave("scatter_plot_cpu.png", plot = g_scatter_avg_cpu)
ggsave("scatter_plot_mem.png", plot = g_scatter_avg_mem)

# Spearman Correlation
correlation_result_cpu_energy <- cor.test(data$avg_cpu, data$energy, method = "spearman")
correlation_result_memory_energy <- cor.test(data$avg_mem, data$energy, method = "spearman")
correlation_result_cpu_power <- cor.test(data$avg_cpu, data$avg_power, method = "spearman")
correlation_result_memory_power <- cor.test(data$avg_mem, data$avg_power, method = "spearman")

# Print the correlation results
cat("Spearman Correlation Test Result for CPU and Energy:\n")
cat("Correlation coefficient (rho):", correlation_result_cpu_energy$estimate, "\n")
cat("P-value:", correlation_result_cpu_energy$p.value, "\n\n")

cat("Spearman Correlation Test Result for Memory and Energy:\n")
cat("Correlation coefficient (rho):", correlation_result_memory_energy$estimate, "\n")
cat("P-value:", correlation_result_memory_energy$p.value, "\n\n")

cat("Spearman Correlation Test Result for CPU and Power:\n")
cat("Correlation coefficient (rho):", correlation_result_cpu_power$estimate, "\n")
cat("P-value:", correlation_result_cpu_power$p.value, "\n\n")

cat("Spearman Correlation Test Result for Memory and Power:\n")
cat("Correlation coefficient (rho):", correlation_result_memory_power$estimate, "\n")
cat("P-value:", correlation_result_memory_power$p.value, "\n\n")


# Mann-Whitney Test
mann_whitney_results <- data %>%
  group_by(Linux_Governor, Workload) %>%
  summarise(
    mw_p_value_memory = wilcox.test(avg_mem ~ factor(Linux_Governor), data = ., alternative = "two.sided", exact = FALSE)$p.value,
    mw_p_value_cpu = wilcox.test(avg_cpu ~ factor(Linux_Governor), data = ., alternative = "two.sided", exact = FALSE)$p.value,
    mw_p_value_energy = wilcox.test(energy ~ factor(Linux_Governor), data = ., alternative = "two.sided", exact = FALSE)$p.value,
    mw_p_value_power = wilcox.test(avg_power ~ factor(Linux_Governor), data = ., alternative = "two.sided", exact = FALSE)$p.value
  )

# Print the results
print("Mann-Whitney Test Results:")
print(mann_whitney_results)

# Effect Size
print("Calculate Effect Size")
cliffs_delta_cpu_energy <- cliff.delta(data$avg_cpu, data$energy, conf.level = 0.95)
cliffs_delta_memory_energy <- cliff.delta(data$avg_mem, data$energy, conf.level = 0.95)

print("Cliff's Delta for CPU and Energy:")
print(cliffs_delta_cpu_energy)

print("Cliff's Delta for Memory and Energy:")
print(cliffs_delta_memory_energy)
