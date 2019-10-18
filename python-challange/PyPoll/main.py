import os
import csv

filepath = os.path.join("Resources","election_data.csv")

election_candidates = []
num_votes = 0
vote_counts = []

with open(filepath,newline="") as csvfile:
    csvreader = csv.reader(csvfile)

    line = next(csvreader,None)

    for line in csvreader:
        num_votes = num_votes + 1
        candidate = line[2]

        if candidate in election_candidates:
            candidate_index = election_candidates.index(candidate)
            vote_counts[candidate_index] = vote_counts[candidate_index] + 1
        else:
            election_candidates.append(candidate)
            vote_counts.append(1)

percentages = []
max_votes = vote_counts[0]
max_index = 0

for count in range(len(election_candidates)):
    vote_percentage = vote_counts[count]/num_votes*100
    percentages.append(vote_percentage)
    if vote_counts[count] > max_votes:
        max_votes = vote_counts[count]
        print(max_votes)
        max_index = count
winner = election_candidates[max_index]

print("Election Results")
print("--------------------------")
print(f"Total Votes: {num_votes}")

for count in range(len(election_candidates)):
    print(f"{election_candidates[count]}: {round(percentages[count],2)}% ({vote_counts[count]})")

print("---------------------------")
print(f"Winner: {winner}")
print("---------------------------")

write_file = f"pypoll_results.txt"

filewriter = open(write_file, mode = 'w')
filewriter.write("Election Results\n")
filewriter.write("--------------------------\n")
filewriter.write(f"Total Votes: {num_votes}\n")

for count in range(len(election_candidates)):
    filewriter.write(f"{election_candidates[count]}: {round(percentages[count],2)}% ({vote_counts[count]})\n")

filewriter.write("---------------------------\n")
filewriter.write(f"Winner: {winner}\n")
filewriter.write("---------------------------\n")
filewriter.close()