import os
import csv

budget_data = os.path.join("Resources","budget_data.csv")

total_months = 0
total_profit_loss = 0
value = 0
change = 0
dates = []
profits = []
with open(budget_data, newline = "") as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ",")
    csv_header = next(csvreader)

    first_row = next(csvreader)
    total_months += 1
    total_profit_loss += int(first_row[1])
    value = int(first_row[1])
    
    for row in csvreader:
        dates.append(row[0])
        change = int(row[1])- value
        profits.append(change)
        value = int(row[1])
        
        total_months += 1

        #Total net amount of "Profit/Losses over entire period"
        total_profit_loss = total_profit_loss + int(row[1])

    greatest_increase = max(profits)
    greatest_index = profits.index(greatest_increase)
    greatest_date = dates[greatest_index]

    greatest_decrease = min(profits)
    worst_index = profits.index(greatest_decrease)
    worst_date = dates[worst_index]

    avg_change = sum(profits)/len(profits)
    

print("Financial Analysis")
print("------------------")
print(f"Total Months: {str(total_months)}")
print(f"Total: ${str(total_profit_loss)}")
print(f"Average Change: ${str(round(avg_change,2))}")
print(f"Greatest Increase in Profits: {greatest_date} (${str(greatest_increase)})")
print(f"Greatest Decrease in Profits: {worst_date} (${str(greatest_decrease)})")


with open('financial_analysis.txt', 'w') as output:
	output.write("Financial Analysis"+"\n")
	output.write("------------------\n")
	output.write(f"Total Months:{str(total_months)}\n")
	output.write(f"Total: ${str(total_profit_loss)}\n")
	output.write(f"Average Change: ${str(round(avg_change,2))}\n")
	output.write(f"Greatest Increase in Profits: {str(greatest_date)} (${str(greatest_increase)})\n")
	output.write(f"Greatest Decrease in Profits: {str(worst_date)} (${str(greatest_decrease)})\n")
	output.close()
	
