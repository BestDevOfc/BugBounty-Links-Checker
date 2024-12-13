#!/bin/bash

# Input and output file names
input_file="domains.txt"
output_file="results.txt"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
  echo "Error: File '$input_file' not found!"
  exit 1
fi

# Clear the output file if it already exists
echo "" > "$output_file"

# Loop through each domain in the input file
while IFS= read -r domain; do
  # Skip empty lines
  if [ -z "$domain" ]; then
    continue
  fi

  # Get the IP address of the domain
  ip=$(dig +short "$domain" | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -n 1)
  
  # Check if an IP was found
  if [ -n "$ip" ]; then
    echo "${ip}: ${domain}" >> "$output_file"
    echo "Resolved $domain to $ip"
  else
    echo "Failed to resolve $domain"
  fi

done < "$input_file"

# Completion message
echo "All domains processed. Results saved in '$output_file'."
